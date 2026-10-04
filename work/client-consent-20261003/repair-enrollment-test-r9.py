from pathlib import Path
p=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/native/resource-client/src/participant_enrollment.rs');s=p.read_text();s=s.replace('fn possession_signs_only_its_own_key_at_the_named_home_subject()', 'fn possession_checks_identity_and_refuses_noncanonical_offered_command()',1)
start=s.index('fn possession_checks_identity_and_refuses_noncanonical_offered_command()');end=s.index('\n    #[test]',start);chunk=s[start:end]
needle='        let wrong_subject = possess_at('
insert='''        retain_exact(&root.join("command.bin"), &[0xab, 0xcd]).unwrap();
        save_json(&root.join("config.json"), &json!({})).unwrap();
'''
assert needle in chunk;chunk=chunk.replace(needle,insert+needle,1)
old='''        possess_at(&root, &root.join("owner.key"), "7", &root.join("c.sig")).unwrap();
        let signature: [u8; 64] = fs::read(root.join("c.sig")).unwrap().try_into().unwrap();
        SigningKey::from_bytes(&secret)
            .verifying_key()
            .verify(&[1, 2], &ed25519_dalek::Signature::from_bytes(&signature))
            .unwrap();
        assert!(possess_at(&root, &root.join("owner.key"), "7", &root.join("c.sig")).is_err());'''
new='''        // A matching key/subject and operator JSON do not authorize the raw
        // two-byte header. A real canonical native command is required too.
        assert!(possess_at(&root, &root.join("owner.key"), "7", &root.join("c.sig")).is_err());
        assert!(!root.join("c.sig").exists());
        assert!(!root.join("possession-acceptance.json").exists());'''
assert old in chunk;chunk=chunk.replace(old,new);p.write_text(s[:start]+chunk+s[end:])
