p="native/resource-client/objective-activity-native-acceptance.py"
s=open(p).read()
old="""    value = turn(label, workspace, body, expect, detail)
    return value.get('transaction')
"""
new="""    value = turn(label, workspace, body, expect, detail)
    LAST['value'] = value
    return value.get('transaction')
"""
assert old in s
s=s.replace(old,new,1)
s=s.replace("""def birth(label, workspace, name, deposit, expect,""","""LAST = {}


def birth(label, workspace, name, deposit, expect,""",1)
old="""tx3 = birth('birth-exact-deposit', sponsor, 'tally-three', PAIR, 'installed')
f1 = state('tally-three', 'funding-born', tx3)"""
new="""# A yield reserves the fee pair AND the storage deposit of the record it commits
# (storageRate * |record|); the Host's own refusal quotes both, so the exact deposit is learned from it.
birth('birth-deposit-quote', sponsor, 'tally-three', PAIR, 'refused', 'underfunded')
quote = re.search(r'underfunded (\\d+) (\\d+)', unhex(LAST['value'].get('detail', '')))
NEED = int(quote.group(2)) if quote else 0
check('deposit-reserves-pair-and-storage', quote is not None and int(quote.group(1)) == PAIR and NEED > PAIR,
      {'pair': PAIR, 'quote': quote.groups() if quote else None})
tx3 = birth('birth-exact-deposit', sponsor, 'tally-three', NEED, 'installed')
f1 = state('tally-three', 'funding-born', tx3)"""
assert old in s
s=s.replace(old,new,1)
old="""f2['purse'] == PAIR - PRICE + 10000,"""
new="""f2['purse'] == NEED - PRICE + 10000,"""
assert old in s
s=s.replace(old,new,1)
s=s.replace("""  funding       a tally whose deposit is exactly one fee pair: its second yield
                cannot reserve the pair (awaitsFunding: parked); a top-up; the""","""  funding       a tally whose deposit is exactly one fee pair plus its record's
                storage deposit: its second yield cannot reserve the pair
                (awaitsFunding: parked); a top-up; the""",1)
if "\nimport re" not in s and "import re\n" not in s:
    s=s.replace("import json","import json\nimport re",1)
open(p,"w").write(s)
