# _*_ coding: utf-8 _*_
__author__ = 'nislam <connect2nazrul@gmail.com>'
import re
from wtforms.validators import ValidationError


class EmailProviders(object):

    def __init__(self, message=None):
        if message is None:
            message = u'We are only accept Gmail or Yahoo or AOL or Outlook'
        self.message = message
        self.pattern = r'@(gmail|yahoo|aol|aim|outlook|live|hotmail)\.(com|net|org)'

    def __call__(self, form, field):
        if re.search(self.pattern, field.data) is None:
            raise ValidationError(self.message)

