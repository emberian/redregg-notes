import unittest
from sweep import audit

class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.row = dict(id='doc-join', outcome='one installed append after lost reply',
                        owner='receiver', consumer='resident', coordinator='product',
                        state='ready', next_action='receive retained signed request',
                        acceptance='one append and four readbacks',
                        progress_evidence='signed fixture source ready')

    def codes(self, rows, inactive=()):
        return {finding[1] for finding in audit(rows, set(inactive))}

    def test_stopped_ready_owner_needs_explicit_wakeup(self):
        self.assertIn('WAKE_OWNER', self.codes([self.row], ['receiver']))

    def test_component_pass_cannot_close_native_join(self):
        self.assertIn('INVALID_CLOSE', self.codes([{**self.row, 'state': 'integrated'}]))

    def test_sleeping_required_producer_is_not_a_valid_wait(self):
        row = {**self.row, 'state': 'waiting', 'waits_for': [dict(
            owner='builder', deliverable='matched native host',
            next_action='repair and compile', ready=False)]}
        self.assertIn('WAKE_PRODUCER', self.codes([row], ['builder']))

    def test_receiving_evidence_and_consumer_ack_close_record(self):
        row = {**self.row, 'state': 'integrated', 'receiving_evidence': 'actual log',
               'consumer_ack': dict(owner='resident', evidence='actual matching readback')}
        self.assertFalse(self.codes([row]))

    def test_empty_registry_cannot_pass(self):
        self.assertIn('INVALID', self.codes([]))

    def test_nonexistent_consumer_cannot_receive_a_handoff(self):
        findings = audit([self.row], set(), {'receiver', 'product'})
        self.assertIn(('doc-join', 'UNKNOWN_AGENT', 'consumer: resident'), findings)
        self.assertFalse(audit([self.row], set(), {'receiver', 'resident', 'product'}))

if __name__ == '__main__':
    unittest.main()
