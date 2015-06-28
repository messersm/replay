"""Module that provides different replay file protocols."""

# standard imports
import json

# import StringIO, since we need it for doctests
import sys
if sys.version_info[0] > 2:
    from io import StringIO
else:
    from StringIO import StringIO

# local imports
from .entry import ReplayCall, ReplayComment

# ignore the pylint no-self-use warning
# pylint: disable=R0201
class ReadableProtocol(object):
    """A ReplayProtocol that uses json to produce human-readable
    und -editable replay files.
    """

    def unhash(self, line):
        """Return a replay entry from the given line.

        For function calls only the results are decoded from json.

        Examples:
        >>> p = ReadableProtocol()
        >>> p.unhash('# This is a comment.')
        ReplayComment(comment='This is a comment.')
        >>> p.unhash('#This is a comment too.    ')
        ReplayComment(comment='This is a comment too.')
        >>> p.unhash('pow(2, 3) = 8')
        ReplayCall(call='pow(2, 3)', result=8)
        >>> p.unhash('sorted([3, 6], reverse=true) = [6, 3]')
        ReplayCall(call='sorted([3, 6], reverse=true)', result=[6, 3])
        """
        if line.startswith('#'):
            return ReplayComment(line[1:].strip())
        else:
            call, result_h = line.split(' = ')
            result = json.loads(result_h)
            return ReplayCall(call, result)

    def hashcall(self, func, *args, **kwargs):
        """Return a hash that looks (nearly) like a python function call.

        Conversion is done using the json module, so some special values
        like booleans won't exactly look like python code.

        Examples:
        >>> p = ReadableProtocol()
        >>> p.hashcall(pow, 2, 5)
        'pow(2, 5)'
        >>> p.hashcall(sorted, [5, 2, 3], reverse=True)
        'sorted([5, 2, 3], reverse=true)'
        """

        call_h = func.__name__ + '('
        argcount = 0
        for i, arg in enumerate(args):
            if i > 0:
                call_h += ', '
            call_h += json.dumps(arg, sort_keys=True)
            argcount += 1

        # be careful: we use 'i' from above!
        for j, key in enumerate(sorted(kwargs.keys())):
            if argcount + j > 0:
                call_h += ', '
            value_h = json.dumps(kwargs.get(key), sort_keys=True)
            call_h += '%s=%s' % (key, value_h)

        call_h += ')'

        return call_h

    def hashresult(self, result):
        """Hash the given result object using json.

        Examples:
        >>> p = ReadableProtocol()
        >>> p.hashresult(34.5)
        '34.5'
        >>> p.hashresult({ 'b' : 20, 'a' : 15 })
        '{"a": 15, "b": 20}'
        >>> p.hashresult({ 'a' : 15, 'b' : 20 })
        '{"a": 15, "b": 20}'
        """

        return json.dumps(result, sort_keys=True)

    def load(self, replayfile):
        r"""Return a list of replay entries from replayfile.

        replayfile can be a filename or file-like object.

        Example:
        >>> f = StringIO()
        >>> p = ReadableProtocol()
        >>> entries = []
        >>> entries.append(ReplayComment(comment='This is a comment.'))
        >>> entries.append(ReplayCall(call='random()', result=0.7))
        >>> n = f.write('# This is a comment.\n')
        >>> n = f.write('random() = 0.7\n')
        >>> n = f.seek(0)
        >>> p.load(f) == entries
        True
        """
        if isinstance(replayfile, str):
            with open(replayfile) as f:
                return self._load_from_fileobject(f)
        else:
            return self._load_from_fileobject(replayfile)

    def _load_from_fileobject(self, f):
        """Internal method: Load entries from file-like replayfile."""
        entries = []

        for line in f.readlines():
            line = line.strip()
            # ignore empty lines
            if len(line) == 0:
                pass
            else:
                entries.append(self.unhash(line))

        return entries

    def save(self, entries, replayfile):
        r"""Save a list of replay entries to replayfile.

        replayfile can be a filename or file-like object.

        Example:
        >>> f = StringIO()
        >>> p = ReadableProtocol()
        >>> entries = []
        >>> entries.append(ReplayComment(comment='This is a comment.'))
        >>> entries.append(ReplayCall(call='random()', result=0.7))
        >>> p.save(entries, f)
        >>> n = f.seek(0)
        >>> result = json.dumps(0.7)
        >>> f.read() == '# This is a comment.\nrandom() = %s\n' % result
        True
        """
        
        # NOTE: The above code makes sure, that python 2.6 doesn't
        # fail this test. (0.7 == 0.69999999999999996)
        
        if isinstance(replayfile, str):
            with open(replayfile, 'w') as f:
                self._save_to_fileobject(entries, f)
        else:
            self._save_to_fileobject(entries, replayfile)

    def _save_to_fileobject(self, entries, f):
        """Internal method: Save entries to file-like replayfile."""
        for entry in entries:
            if isinstance(entry, ReplayComment):
                f.write('# %s\n' % entry.comment)
            elif isinstance(entry, ReplayCall):
                result_h = self.hashresult(entry.result)
                f.write('%s = %s\n' % (entry.call, result_h))
            else:
                raise TypeError(
                    'Unknown entry type: %s' % type(entry).__name__)
