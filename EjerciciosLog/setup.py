from setuptools import find_packages
from cx_Freeze import setup, Executable


options = {
    'build_exe': {
        'includes': [
            'pandas', 'dash_table',
        ],
        'packages': [
            'dash', 'plotly',
        ],
        'excludes': [],
        'include_files': [
          'assets/'
        ],
    }
}

executables = [
    Executable('server.py',
               base='console',
               icon="assets/favicon.ico",
               targetName='Prez.exe')
]

setup(
    name='Prez',
    packages=find_packages(),
    version='1.0',
    description='rig',
    executables=executables,
    options=options
)
