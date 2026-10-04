from pathlib import Path
r=Path('/Users/ember/dev/redregg/work/client-consent-20261003');p=r/'ClientConsentSession.lean';s=p.read_text();reader=(r/'reader.lean').read_text()
start=reader.index('  | 7 =>',reader.index('def dispatch'));end=reader.index('  | 91 =>',start)
code=reader[start:end]
code=code.replace('return (7, ← RequestRefusal.clientBytes (SourceAgreementJson.author kind json (some config)))','return ← RequestRefusal.clientBytes (SourceAgreementJson.author kind json (some config))')
code=code.replace('return (8, value.compress.toUTF8.toList)','return value.compress.toUTF8.toList')
code=code.replace('return (9, ← RequestRefusal.clientBytes (SourceAgreementJson.signatures json))','return ← RequestRefusal.clientBytes (SourceAgreementJson.signatures json)')
code=code.replace('return (10, NativeObservationCodec.signedCodec.encode signed)','return NativeObservationCodec.signedCodec.encode signed')
code=code.replace('return (11, callCodec.encode call)','return callCodec.encode call')
new='''def codec (config : NativeHost.Config) (operation : UInt8) (payload : List UInt8) : IO (List UInt8) := do
  match operation with
'''+code+'''  | _ => throw (IO.userError "not a local codec operation")

'''
idx=s.index('/-- The retained proof');s=s[:idx]+new+s[idx:]
s=s.replace('let answer ← try pure (operation, ← consent config updated operation (body.toList.drop 1))','''let answer ← try pure (operation, ← if operation ≥ 7 && operation ≤ 11 then
      codec config operation (body.toList.drop 1)
    else consent config updated operation (body.toList.drop 1))''')
p.write_text(s)
