from setuptools import setup

dependencies = ['click', 'termcolor']

setup(
    name='fire',
    version='0.1',
    py_modules=['fire'],
    install_requires=dependencies,
    entry_points='''
    [console_scripts]
    fire=fire:cli
    ''',
)
