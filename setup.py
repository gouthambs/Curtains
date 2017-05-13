"""
Curtains
--------
Curtains is a command line tool for remote execution, application deployment and system administration
in the Windows environment (as of now) without using SSH.
"""

from setuptools import setup, find_packages
import os
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('curtains/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))



BASE_PATH = os.path.dirname(__file__)


def get_requirements(suffix=''):
    with open(os.path.join(BASE_PATH, 'Requirements%s.txt' % suffix)) as f:
        rv = f.read().splitlines()
    return rv

setup(
    name='Curtains',
    version=version,
    url='https://github.com/gouthambs/Curtains',
    license='MIT',
    author='Gouthaman Balaraman',
    author_email='gouthaman.balaraman@gmail.com',
    description=' A command line tool for remote execution, application deployment and system '
                'administration in the Windows environment (as of now) without using SSH.',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='win',
    install_requires=get_requirements(),
    tests_require=[],
    entry_points={
        'console_scripts': [
            'curt = curtains.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration'
    ]
)