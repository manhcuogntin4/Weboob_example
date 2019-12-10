
import weboob.browser.filters.standard as OLD

# can't import *, __all__ is incomplete...
for attr in dir(OLD):
    globals()[attr] = getattr(OLD, attr)


try:
    __all__ = OLD.__all__
except AttributeError:
    pass


class Coalesce(MultiFilter):
    """
    Returns the first value that is not falsy,
    or default if all values are falsy.
    """
    @debug()
    def filter(self, values):
        for value in values:
            if value:
                return value
        return self.default_or_raise(FilterError('All falsy and no default.'))


class MapIn(Filter):
    """
    Map the pattern of a selected value to another value using a dict.
    """

    def __init__(self, selector, map_dict, default=_NO_DEFAULT):
        """
        :param selector: key from `map_dict` to use
        """
        super(MapIn, self).__init__(selector, default=default)
        self.map_dict = map_dict

    @debug()
    def filter(self, txt):
        """
        :raises: :class:`ItemNotFound` if key pattern does not exist in dict
        """
        for key in self.map_dict:
            if key in txt:
                return self.map_dict[key]

        return self.default_or_raise(ItemNotFound('Unable to handle %r on %r' % (txt, self.map_dict)))
