from pathlib import Path
p=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/native/resource-client/src/transport.rs');s=p.read_text();start=s.index('fn paid_public_relay_and_observer_share_current_private_host_gate()');end=s.index('\n    struct ',start) if '\n    struct ' in s[start:] else len(s);chunk=s[start:end]
old='''            assert_eq!(invoke(&socket,&config,request[0],&request[1..]).unwrap(),
                vec![request[0],count]);'''
new='''            let reply = invoke(&socket,&config,request[0],&request[1..]);
            if crate::client_consent::plan_operation(request[0]) {
                // Transport admission is not permission to sign the fake
                // operator's one-byte plan: direct callers must check consent.
                assert!(reply.is_err(), "direct plan caller bypassed local consent");
            } else {
                assert_eq!(reply.unwrap(), vec![request[0],count]);
            }'''
assert chunk.count(old)==2;chunk=chunk.replace(old,new);p.write_text(s[:start]+chunk+s[end:])
