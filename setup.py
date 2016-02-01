from setuptools import setup, find_packages


setup(
    name='twtxt',
    version='1.0dev',

    url='https://github.com/buckket/twtxt',

    author='buckket',
    author_email='buckket@cock.li',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    platforms='any',

    install_requires=[
        'aiohttp',
        'appdirs',
        'humanize',
        'click',
        'cached-property',
    ],

    entry_points={
        'console_scripts': ['twtxt=twtxt.cli:main']
    },

    description='Decentralised, minimalist microblogging service for hackers.',
    long_description=open('./README.rst', 'r').read(),

    keywords=['microblogging', 'twitter', 'twtxt'],

    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Communications',
        'Topic :: Utilities',
    ],
)
