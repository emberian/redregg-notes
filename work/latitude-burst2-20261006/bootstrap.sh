#!/usr/bin/env bash
# burst2-20261006 bootstrap. Run as root: bootstrap.sh <role> [box-name]  (role: metal | e2e; box-name burst2-a adds /srv/build-slot-mk)
# Holds no secrets. Idempotent enough to re-run.
set -euo pipefail
role=${1:?role}
box=${2:-}
LOG=/var/log/burst-bootstrap.log
exec > >(tee -a "$LOG") 2>&1
echo "== bootstrap $role $(date -Is)"
export DEBIAN_FRONTEND=noninteractive

# --- second NVMe -> /srv (metal only; instant deploy forbids RAID) ---
if [ "$role" = metal ] && ! mountpoint -q /srv; then
  rootdisk=$(lsblk -no PKNAME "$(findmnt -no SOURCE /)")
  data=""
  for d in $(lsblk -dno NAME,TYPE | awk '$2=="disk"{print $1}'); do
    [ "$d" = "$rootdisk" ] && continue
    [ -z "$(lsblk -no MOUNTPOINT /dev/$d | tr -d '[:space:]')" ] && [ "$(lsblk -no NAME /dev/$d | wc -l)" = 1 ] && { data=$d; break; }
  done
  [ -n "$data" ] || { echo "no blank data disk found"; exit 1; }
  echo "data disk: /dev/$data (root on $rootdisk)"
  mkfs.ext4 -q -F -L srv /dev/$data
  mkdir -p /srv
  echo "LABEL=srv /srv ext4 defaults,noatime 0 2" >> /etc/fstab
  mount /srv
fi
mkdir -p /srv

# --- packages ---
apt-get update -q
apt-get install -y -q build-essential git curl python3 python3-venv cmake pkg-config libssl-dev \
  unzip zstd jq rsync earlyoom clang lld htop tmux libpam-systemd dbus-user-session \
  file sqlite3 age time
systemctl enable --now earlyoom

# --- user ember ---
id ember >/dev/null 2>&1 || useradd -m -s /bin/bash ember
install -d -m 700 -o ember -g ember /home/ember/.ssh
src_keys=/home/ubuntu/.ssh/authorized_keys; [ -f "$src_keys" ] || src_keys=/root/.ssh/authorized_keys
install -m 600 -o ember -g ember "$src_keys" /home/ember/.ssh/authorized_keys
echo 'ember ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/90-ember; chmod 440 /etc/sudoers.d/90-ember
loginctl enable-linger ember

# --- capnp 1.5.0 from source, sha256 pinned (Homebrew formula's checksum for this tag) ---
if ! command -v capnp >/dev/null || [ "$(capnp --version)" != "Cap'n Proto version 1.5.0" ]; then
  t=$(mktemp -d); cd "$t"
  curl -fsSL -o capnp.tar.gz https://github.com/capnproto/capnproto/archive/refs/tags/v1.5.0.tar.gz
  echo "d5ebdf858e9885c33d4b3f765006d68bd66e9b002bf4d607ff4317ef9c1aac6a  capnp.tar.gz" | sha256sum -c -
  tar xzf capnp.tar.gz; cd capnproto-1.5.0/c++
  cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF >/dev/null
  cmake --build build -j"$(nproc)" >/dev/null
  cmake --install build >/dev/null; ldconfig
  cd /; rm -rf "$t"
fi
capnp --version

if [ "$role" = metal ]; then
# --- swarm-build (hbox contract: SWARM_MEM_MAX per build, shared swarm.slice cap) ---
cat > /usr/local/bin/swarm-build <<'SB'
#!/usr/bin/env bash
# swarm-build — run a build under an ENFORCED memory cap (burst2-20261006 boxes).
# Same name and contract as hbox: per-build cap SWARM_MEM_MAX (default 24G) and a
# shared swarm.slice cap (~/.config/systemd/user/swarm.slice.d/50-memcap.conf) that
# bounds the SUM of all concurrent swarm-builds. No taskset: the box is ours.
#   usage: swarm-build lake build Foo   |   SWARM_MEM_MAX=16G swarm-build lake build Foo
set -euo pipefail
if [ -n "${SWARM_BUILD_INNER:-}" ]; then
  echo 0 > /proc/self/oom_score_adj 2>/dev/null || true
  exec nice -n 10 "$@"
fi
export SWARM_BUILD_INNER=1
exec systemd-run --user --scope --slice=swarm.slice --quiet \
  -p MemoryMax="${SWARM_MEM_MAX:-24G}" -p MemorySwapMax=0 \
  -- "$0" "$@"
SB
chmod 755 /usr/local/bin/swarm-build
install -d -o ember -g ember /home/ember/.config /home/ember/.config/systemd /home/ember/.config/systemd/user /home/ember/.config/systemd/user/swarm.slice.d
printf '[Slice]\nMemoryMax=112G\nMemorySwapMax=0\n' > /home/ember/.config/systemd/user/swarm.slice.d/50-memcap.conf
chown ember:ember /home/ember/.config/systemd/user/swarm.slice.d/50-memcap.conf

fi

# --- build slots (flock files; 4 per box at 24G; burst2-a reserves slot-1 for the merge gate) ---
for i in 1 2 3 4; do install -m 666 /dev/null /srv/build-slot-$i; done
if [ "$box" = burst2-a ]; then install -m 666 /dev/null /srv/build-slot-mk; fi

# --- /srv layout ---
install -d -o ember -g ember /srv/mini /srv/mini-logs /srv/lanes /srv/warm-base

# --- user toolchains + repo (as ember) ---
sudo -iu ember bash -s <<'U'
set -euo pipefail
cd ~
[ -x ~/.elan/bin/elan ] || curl -fsSL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --default-toolchain none
[ -x ~/.cargo/bin/rustup ] || curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal
[ -x ~/.bun/bin/bun ] || curl -fsSL https://bun.sh/install | bash -s "bun-v1.3.11"
source ~/.elan/env; source ~/.cargo/env; export PATH=$HOME/.bun/bin:$PATH
grep -q '^# burst PATH' ~/.bashrc || { printf '# burst PATH (before the interactive guard)\nexport PATH=$HOME/.bun/bin:$HOME/.elan/bin:$HOME/.cargo/bin:$PATH\n' | cat - ~/.bashrc > ~/.bashrc.new && mv ~/.bashrc.new ~/.bashrc; }
grep -q 'bun/bin' ~/.profile || echo 'export PATH=$HOME/.bun/bin:$HOME/.elan/bin:$HOME/.cargo/bin:$PATH' >> ~/.profile
git config --global user.name "ember arlynx"; git config --global user.email "cmrx64@gmail.com"; git config --global commit.gpgsign false
[ -d /srv/mini/.git ] || git clone -q https://github.com/emberian/minidregg.git /srv/mini
cd /srv/mini
elan toolchain install "$(cat lean-toolchain)"
rustup toolchain install "$(sed -n 's/^channel *= *"\(.*\)"/\1/p' rust-toolchain.toml)" --profile minimal -c clippy -c rustfmt
echo "user: lean $(lean --version | head -1); $(rustc --version); bun $(bun --version); head $(git rev-parse HEAD)"
U
echo "== bootstrap $role DONE $(date -Is)"
