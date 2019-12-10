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
from weboob.browser.pages import HTMLPage, LoggedPage, pagination
from weboob.browser.pages import LoggedPage, HTMLPage
from weboob.browser.filters.html import Attr
from weboob.browser.filters.standard import CleanDecimal, CleanText, Regexp, Date, Env, TableCell
from weboob.capabilities.bank import Account, Transaction
from weboob.capabilities.base import Field, NotAvailable
from weboob.browser.elements import method, TableElement, ItemElement, ListElement
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
    class get_accounts(ListElement):
        item_xpath = '/html/body/table/tbody/tr'

        class item(ItemElement):
            klass = Account

            obj_label = CleanText('.//a')

            def obj_id(self):
                return Regexp(self.obj_label, r'(\d+)')(self)

            obj_balance = CleanDecimal('./td[2]', replace_dots=True)


class HistoryPage(LoggedPage, HTMLPage):
    @pagination
    @method
    class iter_history(ListElement):
        item_xpath = '/html/body/table/tbody/tr'

        def next_page(self):
            next_page = self.el.xpath('//a[text()="▶"]')
            if next_page:
                return Attr(next_page, 'href')(self)

        class item(ItemElement):
            klass = Transaction

            obj_date = Date(CleanText('./td[1]'), dayfirst=True)
            obj_label = CleanText('./td[2]')

            def obj_amount(self):
                credit = CleanDecimal('./td[3]', replace_dots=True, default=None)(self)
                debit = CleanDecimal('./td[4]', replace_dots=True, default=None)(self)

                if credit is None:
                    return debit
                else:
                    return credit

