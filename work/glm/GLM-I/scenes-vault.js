// scenes-vault.js — the Vault: value under a grade (LANG-89) and rows that hold value (LANG-90).
// The package is the journey's own (Lang/Journey/Holds.lean, the §HV rows): the kernel ships its
// text (kernel:vault) and the menu of outcomes the scene must meet (tg_holds, K.holds — read off
// the journey's package and the kernel's own checkers, never written here). This file only adds the
// demo to `demos`; it is loaded by one line in index.html, and the gate runs it
// (scenes-vault-run.mjs).
import { demos } from './demos.js';

// The commands follow the journey's §HV0 setup: issue the denomination, create the vault (its owner
// bob), open the accounts, fund the depositor 50 from the well, grant the VAULT OBJECT the right to
// move from her account. Each step's result prints inline beside the command (no dialogs); the
// account windows opened on the way keep showing the balances, refreshed after every command.
demos.vault = {
  title: 'Value under a grade: a vault that must pay for what it holds',
  texts: { vault: 'kernel:vault' },
  steps: [
    { who: 'alice', say: 'alice installs the Vault, the journey\'s own package. Every method that moves value declares how much it may move (a grade). The relation vault holds value: each row names a leg the object holds.', argv: (v) => ['install', v.text.vault], bind: 'pkg' },
    { who: 'alice', say: 'alice issues 100 of a new denomination. The well is the issuer\'s account of it.', argv: () => ['issue', '100'], bind: 'well' },
    { who: 'alice', say: 'alice creates the vault object. Its state names the denomination and the owner: bob.', argv: (v) => ['create', '--pkg', v.pkg, `(record (asset #${v.well}) (owner #${v.bob}))`], bind: 'V', open: 'V' },
    { who: 'alice', say: 'the vault needs an account of the denomination to hold what is deposited. alice opens it, then her own.', argv: (v) => ['account', v.well, '--owner', v.V], bind: 'acctV', open: 'acctV' },
    { who: 'alice', argv: (v) => ['account', v.well], bind: 'acctA', open: 'acctA' },
    { who: 'alice', say: 'alice funds her account with 50 from the well.', argv: (v) => ['transfer', `well:${v.well}`, `of:${v.alice}:${v.well}`, '50'] },
    { who: 'alice', say: 'alice grants the vault object the right to move up to 100 from her account. A deposit acts through this grant.', argv: (v) => ['grant', `of:${v.alice}:${v.well}`, v.V, 'transfer:100'], bind: 'g' },
    { who: 'alice', argv: (v) => ['read', v.V, '?'], method: { deposit: 'deposit', depositUnpaid: 'depositUnpaid', withdraw: 'withdraw' } },
    { who: 'alice', say: 'alice deposits: row 0 names a leg of 10, and the same run moves 10 from her account into the vault. Admitted: the row is paid for.', argv: (v) => ['invoke', v.V, v.deposit, `(record (amount 10) (grant #${v.g}) (n 0) (pay 10))`], check: 'deposit' },
    { who: 'alice', say: 'the row, read back:', argv: (v) => ['read', v.V, 'vault', '1'] },
    { who: 'alice', say: 'a withdraw past the grade: 1001 under a grade of 1000. Refused (effectExceeded). Nothing moved: the balances and the row stay as they were.', argv: (v) => ['invoke', v.V, v.withdraw, '(record (amount 1001) (n 0))', '--pin', 'vault', '(record (n 0))'], expect: 'refused', check: 'withdrawPastGrade' },
    { who: 'alice', say: 'the row is still there, and the account windows still show 10 and 40:', argv: (v) => ['read', v.V, 'vault', '2'] },
    { who: 'alice', say: 'an unpaid deposit: row 1 would name a leg of 10 that no transfer moves in. Refused (legUnfunded). No row appears.', argv: (v) => ['invoke', v.V, v.depositUnpaid, '(record (amount 10) (n 1))'], expect: 'refused', check: 'depositUnpaid' },
    { who: 'alice', say: 'row 1 never landed; only row 0 is there:', argv: (v) => ['read', v.V, 'vault', '2'] },
  ],
};
