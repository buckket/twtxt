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

    python_requires='>=3.7',
    install_requires=[
        'aiohttp>=3.8.1,<4',
        'python-dateutil>=2.6.1,<3',
        'humanize>=4.0.0,<5',
        'click>=8.0.0,<9',
        'nest-asyncio>=1.5.0,<2'
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Communications',
        'Topic :: Utilities',
    ],
)
