"""Independent synthetic boundary cases for the v0.1.0 audit."""
import json
import unittest

from test_review import r


class AuditBoundaries(unittest.TestCase):
    def test_cpm_parallel_paths_and_disconnected_terminal(self):
        tasks = [
            {'id': 'T001', 'duration_days': 2, 'predecessors': []},
            {'id': 'T002', 'duration_days': 3, 'predecessors': ['T001']},
            {'id': 'T003', 'duration_days': 3, 'predecessors': ['T001']},
            {'id': 'T004', 'duration_days': 1, 'predecessors': ['T002', 'T003']},
            {'id': 'T005', 'duration_days': 2, 'predecessors': []},
        ]
        result = r.schedule(tasks)
        self.assertEqual(result['duration_days'], 6)
        self.assertEqual([x['id'] for x in result['tasks'] if x['critical']],
                         ['T001', 'T002', 'T003', 'T004'])
        self.assertEqual(result['tasks'][4]['total_float'], 4)

    def test_evm_half_up_from_unrounded_values(self):
        result = r.evm({'currency': 'BRL', 'bac': 3, 'pv': 2, 'ev': 2, 'ac': 1})
        self.assertEqual((result['cpi'], result['spi'], result['eac_cpi']),
                         ('2.0000', '1.0000', 2))
        self.assertEqual((result['etc_cpi'], result['vac_cpi']), (1, 1))

    def test_evm_zero_and_maximum(self):
        result = r.evm({'currency': 'USD', 'bac': r.MAX_CENTS, 'pv': 0,
                        'ev': 1, 'ac': r.MAX_CENTS})
        self.assertIsNone(result['spi'])
        self.assertEqual(result['eac_cpi'], r.MAX_CENTS ** 2)
        self.assertEqual(result['cpi'], '0.0000')

    def test_risk_threshold_is_inclusive(self):
        result = r.risks({'high_threshold': 15, 'items': [
            {'id': 'R001', 'probability': 3, 'impact': 5, 'response_assigned': False},
            {'id': 'R002', 'probability': 2, 'impact': 5, 'response_assigned': False}]})
        self.assertTrue(result[0]['response_missing'])
        self.assertFalse(result[1]['high'])

    def test_raci_multiple_accountable_and_duplicate_role(self):
        assignments = [{'role_id': 'U001', 'code': 'RA'},
                       {'role_id': 'U002', 'code': 'A'}]
        self.assertTrue(r.raci([{'task_id': 'T001', 'assignments': assignments}])[0]['needs_review'])
        assignments[1]['role_id'] = 'U001'
        with self.assertRaisesRegex(r.Invalid, 'DUPLICATE_ID'):
            r.raci([{'task_id': 'T001', 'assignments': assignments}])

    def test_duplicate_keys_nested_and_escaped(self):
        with self.assertRaisesRegex(r.Invalid, 'DUPLICATE_JSON_KEY'):
            r.parse(b'{"x":{"a":1,"\\u0061":2}}')

    def test_opaque_id_can_still_encode_sensitive_information(self):
        # Shape validation cannot determine whether an identifier is sensitive.
        self.assertEqual(r.identifier('P123456', 'P'), 'P123456')


if __name__ == '__main__':
    unittest.main()
