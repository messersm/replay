"""Module that provides the Replay object."""

import copy

# local imports
from .entry import ReplayCall, ReplayComment
from .protocol import ReadableProtocol

class Replay(object):
    """Object that represents a replay of function calls."""

    def __init__(self, filename=None, protocol=ReadableProtocol()):
        self.filename = filename
        self.protocol = protocol

        self.entries = []
        self.replayed = []

        self.load(self.filename)

    def __call__(self, func, *args, **kwargs):
        # Search for a saved call and return it's result.
        callhash = self.protocol.hashcall(func, *args, **kwargs)

        for i, entry in enumerate(self.entries):
            if isinstance(entry, ReplayCall) and entry.call == callhash:
                if i not in self.replayed:
                    self.replayed.append(i)
                    return entry.result

        # If there's no call saved, call the function, save the
        # result, mark the call used and return it.
        result = func(*args, **kwargs)
        saved = copy.deepcopy(result)
        index = len(self.entries)
        self.entries.append(ReplayCall(callhash, saved))
        self.replayed.append(index)

        return result

    def reset(self):
        """Reset the list of used replay entries.

        Examples:
        >>> r = Replay(filename=None, protocol=ReadableProtocol())
        >>> r(pow, 2, 3) # Creates the first entry and marks it used.
        8
        >>> r(pow, 2, 3) # Creates the second entry and marks it used.
        8
        >>> len(r.entries)
        2
        >>> r.reset()
        >>> r(pow, 2, 3) # Replays the first entry and marks it used.
        8
        >>> len(r.entries)
        2

        >>> import random
        >>> r = Replay(filename=None, protocol=ReadableProtocol())
        >>> x = r(random.random)
        >>> r.reset()
        >>> r(random.random) == x
        True
        
        >>> def somefunc():
        ...     return [1, 2, 3, 4, 5]
        >>> r = Replay()
        >>> l = r(somefunc)
        >>> l.remove(4)
        >>> r.entries[0]
        ReplayCall(call='somefunc()', result=[1, 2, 3, 4, 5])
        """

        # Keeps track of the calls, that have already been used.
        self.replayed = []

    def comment(self, comment):
        """Add a comment to this replay.

        Example:
        >>> r = Replay(filename=None, protocol=None)
        >>> r.comment('This is a comment.')
        >>> isinstance(r.entries[0], ReplayComment)
        True
        >>> r.entries[0].comment
        'This is a comment.'
        """
        self.entries.append(ReplayComment(comment))

    def load(self, replayfile):
        """Load the entries from replayfile.

        replayfile can be a filename or file-like object. If replayfile
        is None the replay will get an empty list of entries.

        Examples:
        >>> r = Replay(filename=None, protocol=None)
        >>> r.load(None)
        >>> r.entries
        []
        """

        if replayfile is None:
            self.entries = []
        else:
            try:
                self.entries = self.protocol.load(replayfile)
            except IOError:
                self.entries = []

    def save(self, replayfile=None):
        """Save the entries of this replay to replayfile.
        
        replayfile can be a filename or file-like object. If replayfile
        is None the filename that has been given at the time of
        object instantiation is used.
        """
        
        if replayfile is None:
            replayfile = self.filename
        self.protocol.save(self.entries, replayfile)
