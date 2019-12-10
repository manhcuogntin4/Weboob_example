
import weboob.exceptions as OLD

# can't import *, __all__ is incomplete...
for attr in dir(OLD):
    globals()[attr] = getattr(OLD, attr)


try:
    __all__ = OLD.__all__
except AttributeError:
    pass


class BrowserInteraction(Exception):
    pass


class BrowserQuestion(BrowserInteraction):
    """
    When raised by a browser,
    """
    def __init__(self, *fields):
        self.fields = fields


class DecoupledValidation(BrowserInteraction):
    def __init__(self, message='', resource=None, *values):
        super(DecoupledValidation, self).__init__(*values)
        self.message = message
        self.resource = resource

    def __str__(self):
        return self.message


class AppValidation(DecoupledValidation):
    pass


class NeedInteractive(Exception):
    pass


class NeedInteractiveForRedirect(NeedInteractive):
    """
    An authentication is required to connect and credentials are not supplied
    """
    pass
        
            
class NeedInteractiveFor2FA(NeedInteractive):
    """
    A 2FA is required to connect, credentials are supplied but not the second factor
    """
    pass

