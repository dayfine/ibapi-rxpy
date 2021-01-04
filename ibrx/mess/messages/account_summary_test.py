import dataclasses
import unittest

from hamcrest import assert_that, calling, equal_to, raises
from ibapi import account_summary_tags
from rx import create, empty, from_iterable

from ibrx.mess.message import IbApiMessageType, IbApiMessage
from ibrx.mess.messages import account_summary

_AccountSummary = account_summary.AccountSummary
_AccountSummaryValue = account_summary.AccountSummary.Value
_Tags = account_summary_tags.AccountSummaryTags


class AccountSummaryTest(unittest.TestCase):

    _MESSAGES = [
        IbApiMessage(type=IbApiMessageType.ACCOUNT_SUMMARY,
                     payload=(0, 'DU12345', 'TotalCashValue', '1001872.67',
                              'USD')),
        IbApiMessage(type=IbApiMessageType.ACCOUNT_SUMMARY,
                     payload=(0, 'DU12345', 'NetLiquidation', '1001872.67',
                              'USD')),
    ]

    def _expected_account_summary(self):
        """AccountSummary built from self._MESSAGES"""
        return _AccountSummary(
            account='DU12345',
            values=[
                _AccountSummaryValue(tag=_Tags.TotalCashValue,
                                     value=1001872.67,
                                     currency='USD'),
                _AccountSummaryValue(tag=_Tags.NetLiquidation,
                                     value=1001872.67,
                                     currency='USD'),
            ])

    def test_empty_observable(self):
        obs = account_summary.collect(empty(), 0)

        assert_that(obs.run(), equal_to(_AccountSummary()))

    def test_collect_works(self):
        obs = account_summary.collect(from_iterable(self._MESSAGES), 0)

        assert_that(obs.run(), equal_to(self._expected_account_summary()))

    def test_completes_on_account_summary_end(self):
        messages = self._MESSAGES[:1] + [
            IbApiMessage(type=IbApiMessageType.ACCOUNT_SUMMARY_END,
                         payload=(0,))
        ] + self._MESSAGES[1:]

        obs = account_summary.collect(from_iterable(messages), 0)

        assert_that(
            obs.run(),
            equal_to(
                _AccountSummary(account='DU12345',
                                values=[
                                    _AccountSummaryValue(
                                        tag=_Tags.TotalCashValue,
                                        value=1001872.67,
                                        currency='USD'),
                                ])))

    def test_ignores_messages_of_different_request_id(self):
        messages = self._MESSAGES[:1] + [
            IbApiMessage(type=IbApiMessageType.ACCOUNT_SUMMARY_END,
                         payload=(1,))
        ] + self._MESSAGES[1:]

        obs = account_summary.collect(from_iterable(messages), 0)

        assert_that(obs.run(), equal_to(self._expected_account_summary()))

    def test_ignores_irelevant_messages_types(self):
        messages = self._MESSAGES + [
            IbApiMessage(type=IbApiMessageType.ERROR, payload=()),
            IbApiMessage(type=IbApiMessageType.ACCOUNT_SUMMARY_END,
                         payload=(0,))
        ]

        obs = account_summary.collect(from_iterable(messages), 0)

        assert_that(obs.run(), equal_to(self._expected_account_summary()))

    def test_does_not_complete(self):

        def test_observable(observer, scheduler):
            for msg in self._MESSAGES:
                observer.on_next(msg)
            # Does not complete

        source = create(test_observable)
        obs = account_summary.collect(source, 0)

        obs.subscribe(
            on_next=None,
            on_error=lambda: self.fail('Should not error'),
            on_completed=lambda: self.fail('Should not complete'),
        )

    def test_mismatched_request_id(self):
        obs = account_summary.collect(from_iterable(self._MESSAGES), 1999)

        assert_that(obs.run(), equal_to(_AccountSummary()))

    def test_invalid_message(self):
        message2 = dataclasses.replace(self._MESSAGES[1])  # Make a copy
        message2.payload = message2.payload[:2]
        messages = self._MESSAGES[:1] + [message2]

        obs = account_summary.collect(from_iterable(messages), 0)

        assert_that(calling(obs.run), raises(ValueError))


if __name__ == '__main__':
    unittest.main()
