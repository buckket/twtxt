import ast
import re
import sys

from setuptools import find_packages
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('twtxt/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='twtxt',
    version=version,

    url='https://github.com/buckket/twtxt',

    author='buckket',
    author_email='buckket@cock.li',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    platforms='any',

    install_requires=[
        'aiohttp',
        'python-dateutil',
        'humanize',
        'click',
    ],

    extras_require={
        'dev': [
            'tox',
            'pytest',
            'pytest-cov',
        ],
    },

    entry_points={
        'console_scripts': ['twtxt=twtxt.cli:main']
    },

    description='Decentralised, minimalist microblogging service for hackers.',
    long_description=open('./README.rst', 'r', encoding='utf-8').read(),

    keywords=['microblogging', 'twitter', 'twtxt'],

    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Communications',
        'Topic :: Utilities',
    ],
)
