# -*- coding: utf-8 -*-

# Copyright(C) 2019      nguyen
#
# This file is part of a weboob module.
#
# This weboob module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This weboob module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this weboob module. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals


from weboob.tools.backend import Module, BackendConfig
from weboob.tools.value import ValueBackendPassword, Value
from weboob.capabilities.bank import CapBank

from .browser import Fakebankv3Browser


__all__ = ['Fakebankv3Module']


class Fakebankv3Module(Module, CapBank):
    NAME = 'fakebankv3'
    DESCRIPTION = 'fakebankv3 website'
    MAINTAINER = 'nguyen'
    EMAIL = 'manhcuongeic@gmail.com'
    LICENSE = 'LGPLv3+'
    VERSION = '1.5'

    BROWSER = Fakebankv3Browser

    CONFIG = BackendConfig(Value('login', label='Username', regexp='.+', default='pi'),
                           ValueBackendPassword('password', label='Password', default='314159'),
                           )


    def create_default_browser(self):
        return self.create_browser(self.config['login'].get(), self.config['password'].get())

    def iter_accounts(self):
        for account in self.browser.get_accounts_list():
            yield account

    def iter_history(self, account):
        return self.browser.get_history(account)


