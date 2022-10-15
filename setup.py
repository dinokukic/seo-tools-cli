from setuptools import setup

setup (
    name="seo-tools-cli",
    version="0.1",
    author='Dino Kukic',
    author_email='dino@stu404.com',
    py_modules=['index', 'psi', 'statuscodes', 'redirects', 'emailval', 'sitemap', 'getmetas'],
    install_requires=[
        'argparse',
        'httplib2',
        'oauth2client',
        'pysocks',
        'dnspython',
        'bs4'
    ],
    entry_points='''
        [console_scripts]
        index=index:cli
        psi=psi:cli
        statuscodes=statuscodes:cli
        redirects=redirects:cli
        emailval=emailval:cli
        sitemap=sitemap:cli
        getmetas=getmetas:cli
    '''
)