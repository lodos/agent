from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=[
        'requests',
        'psutil',
        'platform',
        'socket',
        'math',
        'uuid',
        'datetime',
        'getpass',
        'time',
    ]
)
