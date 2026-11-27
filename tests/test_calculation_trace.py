import unittest

from test_review import r


class CalculationTraceTests(unittest.TestCase):
    def test_schedule_trace_keeps_dependencies_and_duration(self):
        task = r.schedule([{'id': 'T001', 'duration_days': 4, 'predecessors': []}])['tasks'][0]
        self.assertEqual(task['calculation']['duration_days'], 4)
        self.assertEqual(task['calculation']['predecessors'], [])

    def test_evm_trace_preserves_exact_ratio_and_rounding_warning(self):
        result = r.evm({'currency': 'BRL', 'bac': 100000, 'pv': 100000,
                        'ev': 1, 'ac': 100000})
        self.assertEqual(result['cpi'], '0.0000')
        self.assertEqual(result['calculation']['cpi'], {'numerator': 1, 'denominator': 100000,
                                                       'rounded_to_zero': True})
        self.assertEqual(result['calculation']['spi']['numerator'], 1)

    def test_risk_trace_preserves_operands_and_threshold(self):
        result = r.risks({'high_threshold': 15, 'items': [{'id': 'R001', 'probability': 3,
                          'impact': 5, 'response_assigned': False}]})[0]
        self.assertEqual(result['calculation'], {'probability': 3, 'impact': 5,
                                                 'high_threshold': 15,
                                                 'response_assigned': False})
