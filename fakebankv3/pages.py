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
from weboob.tools.json import json
from weboob.browser.filters.json import Dict
from lxml import etree
from weboob.browser.pages import LoggedPage, HTMLPage, JsonPage, pagination
from weboob.browser.filters.html import Attr
from weboob.capabilities.bank import Account, Transaction
from weboob.browser.elements import method, TableElement, ItemElement, DictElement, ListElement
from weboob.browser.filters.html import Link, TableCell
from weboob.browser.filters.standard import CleanText, Date, Regexp, Type, CleanDecimal
from weboob.browser.filters.html import CSS
import re
from .compat.weboob_tools_captcha_virtkeyboard import MappedVirtKeyboard, VirtKeyboardError
from io import BytesIO

__all__ = ['ListPage', 'LoginPage']


class FakeVirtKeyboard(MappedVirtKeyboard):
    symbols = {'0': '4f7c8559e3dabb6950527a983694f66c',
               '1': 'cece24d00dba36b35bcaa2c0e8094de9',
               '2': '4d7577cdc572f806b1dd1d3022b19101',
               '3': '6cd32273aa90e91aeec86baa542b357e',
               '4': '3dd448a00c12a122b42edec3967d760b',
               '5': '3751af466952710edf5389d952a3ede3',
               '6': '2b8edf4fbaccca7dbfe9bad523dbf935',
               '7': '93a660a777e3beec47f7b5a31b5265e3',
               '8': '8bbc7f53d0076d32898060a35c475986',
               '9': '788e0743e06bfac78dfebd74a10df7d6'
               }

    color = (0, 0, 0)

    def __init__(self, page):
        img = page.doc.find('//img[@usemap="#vkmap"]')
        res = page.browser.open(img.attrib['src'])
        MappedVirtKeyboard.__init__(self, BytesIO(res.content), page.doc, img, self.color, convert='RGB',
                                    map_attr='href')
        self.check_symbols(self.symbols, None)

    def check_color(self, pixel):
        return pixel[0] < 100

    def get_symbol_coords(self, coords):
        x1, y1, x2, y2 = coords
        return MappedVirtKeyboard.get_symbol_coords(self, (x1 + 10, y1 + 10, x2 - 10, y2 - 10))

    def get_symbol_code(self, md5sum):
        m = re.search('(\d+)', MappedVirtKeyboard.get_symbol_code(self, md5sum))
        if m:
            return m.group(1)

    def get_string_code(self, string):
        code = ''
        for c in string:
            code += self.get_symbol_code(self.symbols[c]) + ','
        return code


class LoginPage(HTMLPage):
    def do_login(self, username, password):

        psdo_password = self.get_password(password)
        form = self.get_form(xpath='/html/body/fieldset/form')
        print("form", form)
        form['login'] = username
        form['code'] = psdo_password
        form.submit()
        print("do_login", username, psdo_password)

    def get_password(self, password):
        vk_passwd = None

        try:
            vk = FakeVirtKeyboard(self)
            vk_passwd = vk.get_string_code(password)
        except VirtKeyboardError as e:
            self.logger.error(e)
            raise

        return vk_passwd


class ListPage(LoggedPage, HTMLPage):
    @method
    class iter_accounts(ListElement):
        item_xpath = '/html/body/div/div'
        class item(ItemElement):
            klass = Account
            obj_id=Regexp(Attr('./a', 'onclick'), r'(\d+)')
            obj_label = CleanText('./a/text()')
            obj_balance = CleanDecimal('.//text()', replace_dots=True)

class HistoryPage(LoggedPage, HTMLPage):
    @pagination
    @method
    class iter_history(TableElement):
        item_xpath = '/html/body/div/table/tbody/tr'
        '''
        def next_page(self):
            next_page = self.el.xpath('//a[text()="▶"]')
            if next_page:
                return Attr(next_page, 'href')(self)
        '''
        class item(ItemElement):
            klass = Transaction

            obj_date = Date(CleanText('./td[1]'), dayfirst=True)
            obj_label = CleanText('./td[2]')
            def obj_amount(self):
                credit = CleanDecimal('./td[3]', replace_dots=True, default=None)(self)
                #debit = CleanDecimal('./td[4]', replace_dots=True, default=None)(self)

                return credit


