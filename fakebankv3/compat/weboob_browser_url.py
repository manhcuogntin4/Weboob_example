import weboob.browser.url as OLD

# can't import *, __all__ is incomplete...
for attr in dir(OLD):
    globals()[attr] = getattr(OLD, attr)


try:
    __all__ = OLD.__all__
except AttributeError:
   pass


class BrowserParamURL(URL):
    """A URL that automatically fills some params from browser attributes.

    URL patterns having groups named "browser_*" will pick the relevant
    attribute from the browser. For example:

        foo = BrowserParamURL(r'/foo\?bar=(?P<browser_token>\w+)')

    The browser is expected to have a `.token` attribute and it will be passed
    automatically when just calling `foo.go()`, it's equivalent to
    `foo.go(browser_token=browser.token)`.

    Warning: all `browser_*` params will be passed, having multiple patterns
    with different groups in a `BrowserParamURL` is risky.
    """

    def build(self, **kwargs):
        prefix = 'browser_'

        for arg in kwargs:
            if arg.startswith(prefix):
                raise ValueError('parameter %r is reserved by URL pattern')

        for url in self.urls:
            for groupname in re.compile(url).groupindex:
                if groupname.startswith(prefix):
                    attrname = groupname[len(prefix):]
                    kwargs[groupname] = getattr(self.browser, attrname)

        return super(BrowserParamURL, self).build(**kwargs)

