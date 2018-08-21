#!/usr/bin/python
from __future__ import print_function

import os
import shutil
import subprocess
import sys
import tempfile

def safe_decode(str_or_bytes):
    if hasattr(str_or_bytes, 'decode'):
        return str_or_bytes.decode()

    return str_or_bytes

def main():
    name = safe_decode(subprocess.check_output(['python', 'setup.py', '--name'])).strip()
    url = "https://pypi.python.org/pypi/%s/" % name
    description = safe_decode(subprocess.check_output(['python', 'setup.py', '--description'])).strip()
    assert 'python' not in name
    if len(sys.argv) == 1:
        print("Usage: %s alias [setup.py arguments]" % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    alias = sys.argv[1]
    author = safe_decode(subprocess.check_output(['python', 'setup.py', '--author'])).strip()
    author_email = safe_decode(subprocess.check_output(['python', 'setup.py', '--author-email'])).strip()
    maintainer = safe_decode(subprocess.check_output(['python', 'setup.py', '--maintainer'])).strip()
    maintainer_email = safe_decode(subprocess.check_output(['python', 'setup.py', '--maintainer-email'])).strip()

    try:
        path = tempfile.mkdtemp()
        os.chdir(path)
        with open(os.path.join(path, 'setup.cfg'), 'w') as fh:
            fh.write("""[bdist_wheel]
universal = 1
""")
        with open(os.path.join(path, 'setup.py'), 'w') as fh:
            fh.write("""# encoding: utf8

from setuptools import setup


setup(
    author=%(author)r,
    author_email=%(author_email)r,
    description=%(description)r,
    install_requires=[%(name)r],
    long_description='''Use `%(name)s <%(url)s>`_ instead.''',
    maintainer=%(author)r,
    maintainer_email=%(author_email)r,
    name=%(alias)r,
    platforms=['all'],
    py_modules=['wheel-platform-tag-is-broken-on-empty-wheels-see-issue-141'],
    url=%(url)r,
    version="0.0",
    zip_safe=False,
)
""" % locals())

        if sys.argv[2] == "twine":
           subprocess.call(['python', 'setup.py', 'bdist_wheel'])
           subprocess.call(sys.argv[2:] + [alias + '*'])
        else:
           subprocess.call(['python', 'setup.py'] + sys.argv[2:])
    finally:
        shutil.rmtree(path)

if __name__ == '__main__':
    main()
