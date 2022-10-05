from setuptools import setup

setup (
    name="indx",
    version="1.0",
    py_modules=['hello', 'index', 'psi', 'statuscodes', 'redirects', 'emailval'],
    install_requires=[
        'argparse',
        'httplib2',
        'oauth2client',
        'pysocks',
        'dnspython'
    ],
    entry_points='''
        [console_scripts]
        hello=hello:cli
        index=index:cli
        psi=psi:cli
        statuscodes=statuscodes:cli
        redirects=redirects:cli
        emailval=emailval:cli
    '''
)