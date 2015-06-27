#pylint: skip-file
from distutils.core import setup

import replay

version = replay.__version__

setup(
    name = 'replay',
    packages = ['replay'],
    version = version,
    description = 'Replay the results of (random) function calls.',
    author = 'Maik Messerschmidt',
    author_email = 'maik.messerschmidt@gmx.net',
    url = 'https://github.com/messersm/replay',
    download_url = 'https://github.com/messersm/replay/tarball/%s' % version,
    keywords = ['replay'],
    classifiers = [],
)
