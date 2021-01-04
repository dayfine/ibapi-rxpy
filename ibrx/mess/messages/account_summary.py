import dataclasses
from typing import List, NewType, Optional, Set

from ibapi import account_summary_tags
from rx.core.typing import Observable
from rx import operators as _

from ibrx.mess.message import IbApiMessageType, IbApiMessage

AccountSummaryTag = NewType('AccountSummaryTag', str)

_ValidAccountSummaryTags: Set[AccountSummaryTag] = {
    tag for tag in account_summary_tags.AccountSummaryTags.AllTags.split(',')
}


@dataclasses.dataclass
class AccountSummary(object):

    @dataclasses.dataclass
    class Value(object):
        tag: AccountSummaryTag
        value: float
        currency: str

    account: str = None
    values: List[Value] = dataclasses.field(default_factory=list)


def collect_account_summary(messages: Observable[IbApiMessage],
                            request_id: int) -> Observable[AccountSummary]:
    return messages.pipe(
        _.filter(
            lambda m: _is_account_summary(m) or _is_account_summary_end(m)),
        _.take_while(lambda m: not _is_account_summary_end(m)),
        _.filter(lambda m: _account_summary_request_id(m) == request_id),
        _.map(_unpack_account_summary),
        _.reduce(lambda summary, data: _add_data_to_summary(data, summary),
                 AccountSummary()))


def _is_account_summary(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.ACCOUNT_SUMMARY


def _is_account_summary_end(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.ACCOUNT_SUMMARY_END


@dataclasses.dataclass
class AccountSummaryData(object):
    account: str
    tag: AccountSummaryTag
    value: float
    currency: str


def _add_data_to_summary(data: AccountSummaryData,
                         summary: AccountSummary) -> AccountSummary:
    res = dataclasses.replace(summary)  # Make a copy
    if not res.account:
        res.account = data.account
    if res.account != data.account:
        raise ValueError(
            'Data has different account than Summary. Data: {}; Summary: {}'.
            format(data, summary))
    res.values.append(
        AccountSummary.Value(tag=data.tag,
                             value=data.value,
                             currency=data.currency))
    return res


def _account_summary_request_id(m: IbApiMessage) -> int:
    return m.payload[0]


def _unpack_account_summary(m: IbApiMessage) -> AccountSummaryData:
    if not _is_account_summary(m):
        raise TypeError(
            'Trying to unpack a message as account summary, but message is of type: {}'
            .format(m.type.name))

    _, account, tag, value, currency = m.payload
    if tag not in _ValidAccountSummaryTags:
        raise ValueError('Invalid account summary tag: {}'.format(tag))
    return AccountSummaryData(account=account,
                              tag=tag,
                              value=float(value),
                              currency=currency)
