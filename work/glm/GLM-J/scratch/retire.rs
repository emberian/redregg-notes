//! RETIREMENT driven by real members over `nd` (KERNEL-70, journey §RT): an owner ends an object
//! with `retire CELL`; a member that does not own it is refused `notOwner` before anything is
//! signed; a parent holding a row is not retired (`rowsRemain`, the writer's answer); once its
//! relation is empty the retirement admits, the id stays a tombstone and every read under it names
//! the missing cell. The board is the rows' own one-slot package (`Protocol.slot`: `post` inserts a
//! row, `clear` retracts it), so the journey's RT1, RT4–RT7 and RT9's member view run against the
//! same package the conformance rows drive. Every verdict here is Lean's; nd moves bytes and signs.
#![allow(clippy::unwrap_used, clippy::panic)] // a plant that cannot set up is a failed plant
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};

use nanodregg_client::generated::command_exit;
use nanodregg_devtools::{Supervisor, mkdirs};

fn line<'a>(out: &'a str, key: &str) -> &'a str {
    out.lines()
        .find_map(|l| l.strip_prefix(key).map(str::trim))
        .unwrap_or_else(|| panic!("no `{key}` line in:\n{out}"))
}

fn text(o: &Output) -> String {
    String::from_utf8_lossy(&o.stdout).into_owned()
}

fn err(o: &Output) -> String {
    String::from_utf8_lossy(&o.stderr).into_owned()
}

fn supervise(sock: &Path, ws: &Path, store: &Path, args: &[&str]) -> Supervisor {
    let sup = Path::new(env!("CARGO_BIN_EXE_nd-supervise"));
    nanodregg_devtools::supervise_host(sup, sock, ws, store, args)
}

/// A founder: its workspace, its holding and the writer's socket (as `doc.rs`'s members).
struct Founder {
    ws: PathBuf,
    holding: PathBuf,
    host_sock: PathBuf,
}

impl Founder {    fn nd(&self, args: &[&str]) -> Output {
        Command::new(env!("CARGO_BIN_EXE_nd"))
            .env("ND_WORKSPACE", &self.ws)
            .env("ND_HOLDING", &self.holding)
            .env("ND_HOST_SOCK", &self.host_sock)
            .args(args)
            .output()
            .unwrap()
    }
    fn ok(&self, args: &[&str]) -> String {
        let o = self.nd(args);
        assert!(o.status.success(), "nd {args:?}: {}{}", text(&o), err(&o));
        text(&o)
    }
    /// (stderr, stdout) of a command the member's own follow refused.
    fn refused(&self, args: &[&str]) -> (String, String) {
        let o = self.nd(args);
        assert_eq!(
            o.status.code(),
            Some(i32::from(command_exit::REFUSED)),
            "nd {args:?}: {}{}",
            text(&o),
            err(&o)
        );
        (err(&o), text(&o))
    }
}

/// The rows' one-slot board, as `install` reads it (`Protocol.slot`, printed by LANG's printer).
fn board() -> String {
    std::fs::read_to_string(Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/retire/Board"))
        .unwrap()
}

#[test]
fn a_member_retires_an_object_it_owns() {
    let host = nanodregg_devtools::lean_bin("host");
    let root = nanodregg_devtools::scratch(&format!("ndretire-{}", std::process::id()));
    for d in ["holding", "holding-b", "stores"] {
        mkdirs(&root.join(d)).unwrap();
    }
    let root = root.canonicalize().unwrap();
    let (ws, holding, holding_b) = (root.join("ws"), root.join("holding"), root.join("holding-b"));
    for h in [&holding, &holding_b] {
        std::fs::set_permissions(h, PermissionsExt::from_mode(0o700)).unwrap();
    }
    let nd = |ws: &Path, holding: &Path, args: &[&str]| -> Output {
        Command::new(env!("CARGO_BIN_EXE_nd"))
            .env("ND_WORKSPACE", ws)
            .env("ND_HOLDING", holding)
            .args(args)
            .output()
            .unwrap()
    };
    assert!(nd(&ws, &holding, &["--init"]).status.success());
    assert!(nd(&root.join("ws-b"), &holding_b, &["--init"]).status.success());
    let a_keys = text(&nd(&ws, &holding, &["--keys"]));
    let b_keys = text(&nd(&root.join("ws-b"), &holding_b, &["--keys"]));
    let (ak, an) = (line(&a_keys, "key "), line(&a_keys, "next "));
    let (bk, bn) = (line(&b_keys, "key "), line(&b_keys, "next "));

    // One genesis, two founders: alice writes, bob does not own what she creates.
    let (w, fa, fb) = (
        root.join("stores/W"),
        root.join("stores/FA"),
        root.join("stores/FB"),
    );
    let g = {
        let o = Command::new(&host)
            .arg("genesis")
            .arg(&w)
            .arg("nano")
            .args([&ak, &an, &bk, &bn])
            .output()
            .unwrap();
        assert!(o.status.success(), "genesis: {}", err(&o));
        text(&o)
    };
    let (alice_member, alice_grant) = {
        let f = line(&g, "founder 0 member ");
        let (m, gr) = f.split_once(" grant ").unwrap();
        (m.to_owned(), gr.to_owned())
    };
    let (bob_member, bob_grant) = {
        let f = line(&g, "founder 1 member ");
        let (m, gr) = f.split_once(" grant ").unwrap();
        (m.to_owned(), gr.to_owned())
    };
    let host_sock = ws.join("host.sock");
    let _w = supervise(&host_sock, &ws, &w, &["serve", w.to_str().unwrap()]);
    let _fa = supervise(
        &ws.join("follow.sock"),
        &ws,
        &fa,
        &["follow", fa.to_str().unwrap(), &alice_member, &alice_grant],
    );
    let _fb = supervise(
        &root.join("ws-b/follow.sock"),
        &root.join("ws-b"),
        &fb,
        &["follow", fb.to_str().unwrap(), &bob_member, &bob_grant],
    );
    let alice = Founder {
        ws: ws.clone(),
        holding,
        host_sock: host_sock.clone(),
    };
    let bob = Founder {
        ws: root.join("ws-b"),
        holding: holding_b,
        host_sock: host_sock.clone(),
    };    let _ = bob.nd(&["sync"]); // bob's follow catches up before it is asked to refuse

    let pkg = line(&alice.ok(&["install", &board()]), "id ").to_owned();
    let obj = line(
        &alice.ok(&["create", "--pkg", &pkg, "(record)"]),
        "id ",
    )
    .to_owned();

    // RT1: bob does not own the board; his follow refuses before his key signs anything.
    let (e, o) = bob.refused(&["retire", &obj]);
    assert_eq!(e, "refused notOwner\n");
    assert!(o.is_empty(), "{o}");
    // RT4: a row stands under the board.
    alice.ok(&["invoke", &obj, "1", "(record (k 1) (text \"first\"))"]);
    let rows = alice.ok(&["read", &obj, "posts", "8"]);
    assert!(rows.contains("first"), "{rows}");
    // RT5: a parent holding a row is not retired; the writer declines the call.
    let (e, _) = alice.declined(&["retire", &obj]);
    assert!(e.contains("rowsRemain"), "{e}");
    // RT6: the row retracts; the relation is empty.
    alice.ok(&["invoke", &obj, "0", "(record (k 1))"]);
    assert_eq!(alice.ok(&["read", &obj, "posts", "8"]).lines().count(), 0);
    // RT7: the empty board retires; the id stays a tombstone.
    alice.ok(&["retire", &obj]);
    // RT9's member view: every read under it names the missing cell.
    let (e, _) = alice.refused(&["read", &obj]);
    assert_eq!(e, "refused missingCell\n");
    let (e, _) = alice.refused(&["read", &obj, "posts", "8"]);
    assert_eq!(e, "refused missingCell\n");
    // A second retirement of the same id is the same missing cell.
    let (e, _) = alice.refused(&["retire", &obj]);
    assert_eq!(e, "refused missingCell\n");

    // RT2's shape: a plain cell, retired by its owner.
    let cell = line(&alice.ok(&["create"]), "id ").to_owned();
    alice.ok(&["write", &cell, "0", "gone soon"]);
    alice.ok(&["retire", &cell]);
    let (e, _) = alice.refused(&["read", &cell]);
    assert_eq!(e, "refused missingCell\n");
}
