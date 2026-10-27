# M6GRAIN-HBOX log (cv 01a13c42-dcb6)
Lane: hbox /tank/dregg-build/claude-lanes/m6grain-hbox/src, branch lane/m6grain-hbox at a63c33ff (next 0125b224 + inputs-hbox + hermes-bwrap).
## events
- start: read SAFETY-BLOCK, INPUTS-HBOX-LOG m6grain, HERMES-BWRAP-LOG m6grain note. uid 1001 free on hbox; hbox has (ALL:ALL) NOPASSWD: ALL already (so the hbox->operator rule is a scope declaration, not new power).
- design: operator = new user `mini-operator` uid 1001 (not `ember`: a service account, named for its role). Row runs the journey as the operator
  via `sudo -n -u $MINI_OPERATOR_NAME -- <script>` when the runner is not the operator; run root under /run/user/<op>/ (the runner's RUN is /run/user/1000, 0700);
  evidence mirrored back into $RUN/g by the runner's root tar, operator run root removed after. Operator needs root only for install-user-world
  (the installer itself writes the per-store helper rule `#<uid> ALL=(root) NOPASSWD: <helper>`).
- BOX CHANGES (root, hbox, 2026-10-14 ~17:50Z), each with its undo:
  1. `sudo useradd --uid 1001 --user-group --create-home --home-dir /home/mini-operator --shell /usr/sbin/nologin --comment "Mini SPK operator (m6grain two-world journey)" mini-operator`
     -> uid/gid 1001, subuid+subgid mini-operator:165536:65536 (useradd auto-allocated). UNDO: `sudo loginctl disable-linger mini-operator; sudo userdel -r mini-operator` (then check `grep mini-operator /etc/subuid /etc/subgid` is empty; else `sudo usermod --del-subuids 165536-231071 --del-subgids 165536-231071 mini-operator` before userdel).
  2. `sudo loginctl enable-linger mini-operator` -> Linger=yes, user@1001 active. UNDO: `sudo loginctl disable-linger mini-operator`.
  3. `sudo setfacl -m u:mini-operator:r-x /usr/local/libexec/mini-grain-bwrap`. UNDO: `sudo setfacl -x u:mini-operator /usr/local/libexec/mini-grain-bwrap`.
     MEASURED: the briefed `--x` does NOT work: an exec-only (unreadable) binary makes the process non-dumpable, /proc/self/uid_map is then root-owned, and bwrap dies "setting up uid map: Permission denied" (as mini-operator: --x rc=1, r-x rc=0; hbox via group r-x rc=0). Same r-x as the existing mini-hbox-app-00 entry.
  4. `/etc/sudoers.d/mini-operator` root:root 0440 (visudo -cf OK): hbox -> (mini-operator) NOPASSWD only `…/journeys/.trees/*/scripts/spk-platform/two-world-journey.sh` and `…/claude-lanes/*/src/scripts/spk-platform/two-world-journey.sh`, env_keep MINI_OPERATOR_UID MINI_OPERATOR_NAME; mini-operator -> (root) NOPASSWD only the matching `deploy/spk-host/install-user-world` paths. `sudo -l -U mini-operator /usr/bin/id` refused. UNDO: `sudo rm /etc/sudoers.d/mini-operator`.
     Note: hbox already holds (ALL:ALL) NOPASSWD: ALL, so the hbox line declares scope; it grants nothing new.
- 21:56Z box.env += MINI_OPERATOR_UID=1001 MINI_OPERATOR_NAME=mini-operator MINI_TEST_SPK=<pipeline/inputs/spk/sntfy-bc424d5f….spk 0444, fetched by fetch-test-spk.sh, sha verified> (before: box.env.before-m6grain-hbox; UNDO: cp it back). m6grain single row launched (run-row.sh, pid file run-row.pid) vs next, results pipeline/runs/m6grain-hbox/.
- 21:56Z VERDICT m6grain UNCONFIGURED 1 s (single row, next 7ffd6524, lane runner; runs/m6grain-hbox/): "missing input: /usr/bin/newuidmap (uidmap)".
  Passed before it: operator account mini-operator/1001, linger, sudo -n, both scoped sudo rules (probed as 98), product_userns. hbox has no `uidmap` package
  (apt candidate 1:4.15.3-3ubuntu2); installing setuid-root newuidmap/newgidmap is outside this lane's root grant -> NOT installed; ROOT/Ember decide.
- absent-inputs.tsv: m6grain NOT removed (it did not run); regex now `^missing input: (operator uid 1001 |/usr/bin/newuidmap \(uidmap\)$)` (old form = sets predating this lane), reason rewritten. Previous: absent-inputs.tsv.before-m6grain-hbox.
- box-changes.md created at /tank/dregg-build/pipeline/box-changes.md (entries 1-5 with undo).
- also fixed: row's post-run custody check `[ ! -e ]` on /etc/sudoers.d/mini-spk-* and /run/user/1001/... was vacuous for a non-root runner; now `sudo -n test -e`.
- committed c7fa4840 on lane/m6grain-hbox (a63c33ff + 1), pushed to mirror; GitHub: hbox has no key -> ROOT.
- NEXT once uidmap is installed: `cd /tank/dregg-build/claude-lanes/m6grain-hbox && RUNTAG=-r1 setsid nohup bash run-row.sh >run-row-r1.out 2>&1 </dev/null & echo $! > run-row.pid`; on a run (PASS or FAIL), remove m6grain from absent-inputs.tsv.
- ROOT installed uidmap and relaunched (runs/m6grain-hbox-r1). VERDICT m6grain FAIL 460 s: "m6grain evidence-a/start-a exit 1: spk-host: grain refused: resident unit mini-spk-s6e19679e931bdd63-a9101-g2.service is failed before START completion".
  Unit journal: "spk-host: resident bootstrap refused: namespace empty groups refused after gid mapping: Operation not permitted". Kernel audit 18:08:16: userns_create transitioning profile -> unprivileged_userns; apparmor="DENIED" operation="capable" profile="unprivileged_userns" comm="spk-host" capname="setgid".
  i.e. spk-host's OWN unshare(CLONE_NEWUSER) (native/spk-host/src/namespace_identity.rs enter) is not covered by an AppArmor profile; the operator path itself worked end to end (sudo run, mirror, cleanup: both ROOT CLEANUP lines, `cleanup original=1 removal_assertions=0`, no /run/user/1001/m6g-* left). cv 01a13d9c-8a9d.
- absent-inputs.tsv: m6grain REMOVED (it runs). Previous absent-inputs.tsv.before-m6grain-hbox-r1. required-rows lists m6grain -> hbox landings exit 13 until a known-red line or the fix lands (ROOT).
- committed bb993cc9 (docs), pushed mirror + GitHub directly from hbox (lane/m6grain-hbox = bb993cc9). DONE.
