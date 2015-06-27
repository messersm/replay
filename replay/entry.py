"""Module that defines different types of replay entries.

ReplayCall    - represents a function call
ReplayComment - represents a comment
"""

# standard imports
from collections import namedtuple

ReplayCall = namedtuple('ReplayCall', ['call', 'result'])
ReplayComment = namedtuple('ReplayComment', ['comment'])
