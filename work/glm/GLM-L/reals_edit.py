import pathlib
p = pathlib.Path("/home/hbox/nd-land/glm-l/client/tests/real.rs")
s = p.read_text()

old = """    ok(&["rotate"]);
    let rotated = text(&nd(&["--keys"]));"""
new = """    // The workspace as it stands: the copy an old backup (or a thief) would hold.
    let (old_seed, old_next) = (
        std::fs::read(ws.join("seed")).unwrap(),
        std::fs::read(ws.join("next.pub")).unwrap(),
    );
    ok(&["rotate"]);
    let rotated = text(&nd(&["--keys"]));"""
assert s.count(old) == 1, "rotate anchor not found"
s = s.replace(old, new)

old = """    drop(_o);
    drop((_h, _f));
    std::fs::remove_dir_all(&root).unwrap();
}"""
new = """    // A copy of the old workspace (a restored backup, or a thief's copy of the file): the call its
    // nd signs names the key its custody reports, which is no longer the member's, and the writer
    // refuses it BY NAME (unknownKey). The member's own custody is untouched and still writes.
    // The kernel's mirror: KERNEL-60's stale for calls already in flight, the rotate row's
    // notPrecommitted for a thief trying to rotate (the client test for the MEMBER.md section).
    let (new_seed, new_next) = (
        std::fs::read(ws.join("seed")).unwrap(),
        std::fs::read(ws.join("next.pub")).unwrap(),
    );
    for (name, bytes) in [("seed", &old_seed), ("next.pub", &old_next)] {
        std::fs::write(ws.join(name), bytes).unwrap();
    }
    let stale = nd(&["write", &obj, "6", "the old key"]);
    assert_eq!(
        stale.status.code(),
        Some(1),
        "the old key's write: {}{}",
        text(&stale),
        String::from_utf8_lossy(&stale.stderr)
    );
    assert!(
        String::from_utf8_lossy(&stale.stderr).contains("refused unknownKey"),
        "the old key's write is refused by name: {}",
        String::from_utf8_lossy(&stale.stderr)
    );
    for (name, bytes) in [("seed", &new_seed), ("next.pub", &new_next)] {
        std::fs::write(ws.join(name), bytes).unwrap();
    }
    ok(&["write", &obj, "6", "the new key"]);

    drop(_o);
    drop((_h, _f));
    std::fs::remove_dir_all(&root).unwrap();
}"""
assert s.count(old) == 1, "test end anchor not found"
s = s.replace(old, new)

# the doc comment at the top names the round trip; add the stale-key step
old = """//! (the member's own fold), both confined (CLIENT-9), on two Stores made by `host genesis` from
//! custody's own public keys. create → write → read → a failing expectation → rotate → write under
//! the rotated key → read."""
new = """//! (the member's own fold), both confined (CLIENT-9), on two Stores made by `host genesis` from
//! custody's own public keys. create → write → read → a failing expectation → rotate → write under
//! the rotated key → read → a copy of the old workspace's write refused `unknownKey` by name."""
assert s.count(old) == 1, "header anchor not found"
s = s.replace(old, new)

p.write_text(s)
print("real.rs edited")
