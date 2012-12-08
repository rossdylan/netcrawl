from setuptools import setup

setup(
    name='netcrawl',
    version='0.1.0',
    description='Crawl the internet',
    author='Ross Delinger',
    author_email='rossdylan@csh.rit.edu',
    install_requires = [
        'redis-py',
        'retask',
    ],
    zip_safe=False,
    entry_points="""
    [console_scripts]
    netcrawl_scanner = netcrawl:run_scanner
    netcrawl_chunker = netcrawl:run_chunker
    netcrawl_receiver = netcrawl:run_chunker
    """
    )
