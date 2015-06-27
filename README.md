# replay
Python library to replay the results of (random) function calls.

[![Build Status](https://travis-ci.org/messersm/replay.svg?branch=master)](https://travis-ci.org/messersm/replay)

## Introduction

replay is a simple package that enables you to save the results of
time intensive deterministic function calls or random function calls
(and by function I mean any kind of callables), that should be replayed,
within a file using a simple API.

replay will never execute any code from a replay file. It hashes the
calls and looks for the hashes in the replay file, so there's no
security risk in changing replay files (other then, that you could
get other results...).

Example:
```python
>>> import os
>>> import random
>>> import replay
>>> import tempfile
>>> fd, tmpname = tempfile.mkstemp(suffix='.replay')
>>> r1 = Replay(tmpname)
>>> random_numbers1 = [r1(random.random) for i in range(10)]
>>> r1.save()
>>> del r1
>>> r2 = Replay(tmpname)
>>> random_numbers2 = [r2(random.random) for i in range(10)]
>>> random_numbers1 == random_numbers2
True
>>> os.remove(tmpname)
```

Replay files can have different formats. Right now only a human-readable
and -editable format is implemented. This format looks mostly like python
except that the actual values a encoded with json.

Here's an example for such a file:
```
random() = 0.3
pow(2, 3) = 8
# This is a comment.
random() = 0.2
sorted([7, 2, 3], reverse=true) = [7, 3, 2]
```

You can freely edit such a file and future calls to these functions
will return the results you write into them:

Example:
```
>>> import os
>>> import random
>>> import replay
>>> import tempfile
>>> fd, tmpname = tempfile.mkstemp(suffix='.replay')
>>> with open(tmpname, 'w') as f: n = f.write('random() = 40\n')
>>> r = Replay(tmpname)
>>> r(random.random)
40
>>> os.remove(tmpname)
```
"""

## Installation

replay is registred in the Python Package Index (PyPi). You can simply
install the package using pip:

```shell
pip install replay
```
