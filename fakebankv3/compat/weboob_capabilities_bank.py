
import weboob.capabilities.bank as OLD
from weboob.capabilities.base import StringField
from weboob.capabilities.date import DateField

# can't import *, __all__ is incomplete...
for attr in dir(OLD):
    globals()[attr] = getattr(OLD, attr)


try:
    __all__ = OLD.__all__
except AttributeError:
    pass


# can't create a subclass because of CapBank.iter_resources reimplementations:
# modules will import our subclass, but boobank will call iter_resources with the OLD class
Account._fields['ownership'] = StringField('Relationship between the credentials owner (PSU) and the account')
Loan._fields['ownership'] = StringField('Relationship between the credentials owner (PSU) and the account')


Transaction._fields['bdate'] = DateField('Bank date, when the transaction appear on website (usually extracted from column date)')


class RecipientInvalidOTP(AddRecipientError):
    code = 'invalidOTP'


class TransferInvalidOTP(TransferError):
    code = 'invalidOTP'


class AccountOwnership(object):
    """
    Relationship between the credentials owner (PSU) and the account
    """
    OWNER = u'owner'
    """The PSU is the account owner"""
    CO_OWNER = u'co-owner'
    """The PSU is the account co-owner"""
    ATTORNEY = u'attorney'
    """The PSU is the account attorney"""


AccountOwnerType.ASSOCIATION = u'ASSO'


try:
    __all__ += ['AccountOwnership', 'RecipientInvalidOTP', 'TransferInvalidOTP']
except NameError:
    pass
