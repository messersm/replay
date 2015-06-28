# replay [![Build Status](https://travis-ci.org/messersm/replay.svg?branch=master)](https://travis-ci.org/messersm/replay)

Python library to replay the results of (random) function calls.

## Introduction

replay is a simple package that enables you to save the results of
time intensive deterministic function calls or random function calls
(and by function I mean any kind of callables), that should be replayed,
within a file using a simple API.

replay will never execute any code from a replay file. It hashes the
calls and looks for the hashes in the replay file, so there's no
security risk in changing replay files (other then, that you could
get other results...).

Replay files can have different formats. Right now only a human-readable
and -editable format is implemented. This format looks mostly like python
except that the actual values a encoded with json.

Here's an example script:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import replay

r = replay.Replay('random.replay')

for i in range(5):
    print(r(random.random))
    
r.save()
```

The output is:

```
0.471306418755
0.954368067794
0.975113533495
0.155125371588
0.50165523797
```

Running this for the first time will create the file 'random.replay',
which will look like this:

```
random() = 0.4713064187546834
random() = 0.9543680677943641
random() = 0.9751135334950991
random() = 0.15512537158813866
random() = 0.501655237970431
```

Running the script for the second time will result in the same output.
Here's another example for a replay file:
```
random() = 0.3
pow(2, 3) = 8
# This is a comment.
random() = 0.2
sorted([7, 2, 3], reverse=true) = [7, 3, 2]
```

You can freely edit such a file and future calls to these functions
will return the results you write into them. Example:
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

## Installation

replay is registred in the Python Package Index (PyPi). You can simply
install the package using pip:

```shell
pip install replay
```
