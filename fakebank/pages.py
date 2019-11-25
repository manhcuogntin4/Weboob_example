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

from weboob.browser.pages import HTMLPage

from weboob.browser.pages import LoggedPage, HTMLPage
from weboob.browser.filters.html import Attr
from weboob.browser.filters.standard import CleanDecimal, CleanText, Regexp
from weboob.capabilities.bank import Account
from weboob.browser.elements import method, TableElement, ItemElement
from weboob.browser.filters.html import Link, TableCell
from weboob.browser.filters.html import CSS


class LoginPage(HTMLPage):
    def login(self, username, password):
        form = self.get_form()
        form['login'] = username
        form['password'] = password
        form.submit()


class AccountPage(LoggedPage, HTMLPage):
    @method
    class get_accounts(TableElement):
        head_xpath = '//html/body/table/thead/tr/th'
        item_xpath = '//html/body/table/tbody/tr'
        col_label = [u'Nom du compte', u'Solde']

        class item(ItemElement):
            klass = Account

            obj_id = Regexp(Attr('.//a', 'href'), r'(\d+)')  # & Type(type=int)
            obj_label = CleanText('./td[1]')
            obj_balance = CleanDecimal('./td[2]', replace_dots=True)
            #obj_label = CleanText(TableCell('label'))
