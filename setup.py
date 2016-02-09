import sys
from setuptools import setup, find_packages


if sys.version_info < (3, 4, 1):
    raise RuntimeError("twtxt requires Python 3.4.1+")


setup(
    name='twtxt',
    version='1.1.0',

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

    entry_points={
        'console_scripts': ['twtxt=twtxt.__main__:main']
    },

    description='Decentralised, minimalist microblogging service for hackers.',
    long_description=open('./README.rst', 'r').read(),

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
