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
        'excludes': ['tkinter'],
        'include_files': [
          'assets/'
        ],
    }
}

executables = [
    Executable('server.py',
               base='console',
               targetName='Prez.exe')
]

setup(
    name='Prez',
    packages=find_packages(),
    version='0.0.3',
    description='rig',
    executables=executables,
    options=options
)
