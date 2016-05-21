#!/usr/bin/env python
# coding=utf-8
"""
# nhspy : Implementation of cui

Summary :
    <summary of module/class being implemented>
Use Case :
    As a <actor> I want <outcome> So that <justification>

Testable Statements :
    Can I <Boolean statement>
    ....
"""

__version__ = "0.1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '21 May 2016'

from datetime import datetime
from numbers import Real
from collections import Callable

import re

class _Core(object):
    """ _Core mixin - a place for common cui functionality
        All Cui Data types must inherit from _Core
    """
    fmt_spec = re.compile(
        r"""
         (?x)                           # Allow Verbose
         (
            (?P<fill>.?)                # Optional Fill Character
            (?P<align>[<>^]?)           # Optional Align Character
         )
         (?P<width>\d*?)                # Optional Width specifier
         v                              # Format type is v
          """)

    def __format__(self, format_spec):
        raise NotImplemented("All cui data types must implement their own __format__ method if their other baseclass does not support it")


    def _split_format_spec(self, format_spec):
        pass

class DateTime(datetime, _Core):
    """Date class - supports all the normal date/tme functions, and nhs cui formatting"""

    def __new__(cls, initial=None):
        """ Create a CUI compliant DateTime Object, from the initial value
            initial : Either
                    numeric - a timestamps of seconds since 1970-01-01 00:00
                    datetime - a value derived from the datetime module
                    string - a text value in nhs standard format (e.g. 01-Jan-1970 01:20)
                    callable - a function to be called on construction (so a date time can be used as a default)
                            The Callable can return None, numeric, String, or datetime as above
                if initial is not provided - defaults to now()
        """

        initial_date = None

        if isinstance(initial, Callable):
            initial = initial()

        if initial is None:
            initial_date = datetime.now()

        if isinstance(initial, Real):
            initial_date = datetime.utcfromtimestamp(initial)

        if isinstance(initial, basestring):
            initial_date = datetime.strptime( initial, '%d-%b-%Y %H:%M')

        if isinstance(initial, datetime):
            initial_date = initial

        if initial_date is None:
            raise ValueError('Invalid value for initial argument - must be a numeric, string, datetime, Callable or None')

        return datetime.__new__(cls, initial_date.year, initial_date.month, initial_date.day,
                            initial_date.hour, initial_date.minute, initial_date.second, initial_date.microsecond,
                            initial_date.tzinfo)

    def __format__(self, format_spec):
        """ Magic method to implement customised formatting"""
        if not format_spec: # No format spec - always return the ISO format
            return str(self)

        fmt_match = DateTime.fmt_spec.match(format_spec)
        if fmt_match:
            val, fmt = self.strftime('%d-%b-%Y %H:%M'),  format_spec[:-1] + "s"
            return "{val:{fmt}}".format(fmt = fmt, val=val)
        else:
            val, fmt  = self,  format_spec
            return "{val:{fmt}}".format(fmt = fmt, val=datetime(val))

class NHSNumber(str, _Core):
    def __init__(self, number):
        """ Create a CUI compliant NHSNumber - basically a string with customised formatting

        :param number: The intial number - with or without separators
        """

    def __format__(self, format_spec):
        """ Magic method to implement customised formatting"""
        pass


class Name(_Core):
    def __init__(self, last_name='', first_name=''):
        """ Create a CUI compliant NHSNumber - basically a string with customised formatting

            :param last_name : The person's last name
            :param first_name : The person's first name
        """
        pass


    def __format__(self, format_spec):
        """ Magic method to implement customised formatting"""
        pass
