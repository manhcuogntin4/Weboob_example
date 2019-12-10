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


from weboob.browser import LoginBrowser, URL, PagesBrowser
from weboob.exceptions import BrowserIncorrectPassword

from .pages import LoginPage, ListPage, HistoryPage
from weboob.browser import need_login




class Fakebankv3Browser(LoginBrowser, PagesBrowser):
    BASEURL = 'https://people.lan.budget-insight.com'

    login = URL(r'/~ntome/fake_bank.wsgi/v3/login', LoginPage)
    accounts = URL(r'/~ntome/fake_bank.wsgi/v3/app', ListPage)
    history_page=URL(r'/~ntome/fake_bank.wsgi/v3/app', HistoryPage)

    def do_login(self):
        self.login.stay_or_go()
        #print(self.page.content)
        if not self.page.do_login(self.username, self.password) or self.login.is_here():
            print("login page check errror")


    @need_login
    def get_accounts_list(self):
        form = {'action': 'accounts'}
        self.accounts.go(data=form)
        print(self.page.content)
        return self.page.iter_accounts()

    @need_login
    def get_history(self, account):
        self.history_form={}
        self.history_form['action'] = 'history'
        self.history_form['account_id'] = account.id
        self.history_form['page'] = '1'
        self.history_page.go(data=self.history_form)
        print(account.id)
        print(self.page.content)
        for transaction in self.page.iter_history():
            yield transaction

