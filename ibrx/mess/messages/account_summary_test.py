import unittest

from ibrx.mess.messages import account_summary
from rx import empty


class AccountSummaryTest(unittest.TestCase):

    def test_collect_account_summary_empty(self):
        obs = account_summary.collect_account_summary(empty(), 0)

        self.assertEqual(obs.run(), account_summary.AccountSummary())


if __name__ == '__main__':
    unittest.main()
