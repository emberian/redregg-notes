from pathlib import Path
import hashlib,json,difflib
root=Path('/home/hbox/workbox/codex-unified-integration-20261003/src/native/resource-client/src');out=Path('/home/hbox/workbox/codex-client-consent-20261003');rows=[];patch=[]
for name in ['participant_enrollment.rs','session_enrollment.rs']:
 p=root/name;s=p.read_text();before=s
 needle='"installed" | "replayed"';assert s.count(needle)==1;s=s.replace(needle,'"installed" | "replayed" | "recoveredAfterUncertainResponse"',1)
 if name=='participant_enrollment.rs':
  anchor='fn result(directory:';assert anchor in s
  helper='''fn confirmed_lookup(value: &Value) -> Result<()> {
    confirmed(value)?;
    if field(value, "confirmation")? != "replayed" {
        return Err("enrollment lookup did not confirm historical acceptance".into());
    }
    Ok(())
}

''';s=s.replace(anchor,helper+anchor,1)
  start=s.index('fn lookup_exact(');end=s.index('\nfn submit(',start);chunk=s[start:end];assert '    confirmed(&value)?;' in chunk;chunk=chunk.replace('    confirmed(&value)?;','    confirmed_lookup(&value)?;',1);s=s[:start]+chunk+s[end:]
  s=s.replace('fn installed_and_replayed_receipts_have_one_stable_result()', 'fn installed_replayed_and_recovered_receipts_have_one_stable_result()',1)
  needle='        result(&root, &pin, &replayed).unwrap();';add='''
        let mut recovered = installed.clone();
        recovered["confirmation"] = json!("recoveredAfterUncertainResponse");
        result(&root, &pin, &recovered).unwrap();
        assert!(confirmed_lookup(&installed).is_err());
        assert!(confirmed_lookup(&recovered).is_err());
        assert!(confirmed_lookup(&replayed).is_ok());
        for name in ["transactionId", "eventId", "acceptedCount", "worldRoot"] {
            let mut changed = recovered.clone();
            changed[name] = json!("9");
            assert!(result(&root, &pin, &changed).is_err(), "{name}");
        }
''';assert needle in s;s=s.replace(needle,needle+add,1)
 else:
  needle='''        value["acceptedCount"] = json!("0");''';add='''        let expected = receipt(&value).unwrap();
        value["confirmation"] = json!("recoveredAfterUncertainResponse");
        assert_eq!(receipt(&value).unwrap(), expected);
        for name in ["transactionId", "eventId", "acceptedCount", "worldRoot"] {
            let mut missing = value.clone();
            missing.as_object_mut().unwrap().remove(name);
            assert!(receipt(&missing).is_err(), "{name}");
        }
''';assert needle in s;s=s.replace(needle,add+needle,1)
 p.write_text(s);rows.append({'path':str(p),'before':hashlib.sha256(before.encode()).hexdigest(),'sha256':hashlib.sha256(s.encode()).hexdigest()});patch.extend(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile='a/native/resource-client/src/'+name,tofile='b/native/resource-client/src/'+name))
(out/'confirmed-receipts.patch').write_text(''.join(patch));(out/'CONFIRMED-RECEIPTS-SOURCE.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
