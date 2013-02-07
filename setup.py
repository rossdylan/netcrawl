from setuptools import setup

setup(
    name='netcrawl',
    version='0.1.0',
    description='Crawl the internet',
    author='Ross Delinger',
    author_email='rossdylan@csh.rit.edu',
    install_requires = [
        'beautifulsoup4',
        'requests',
        'redis',
        'pyelasticsearch',
        'nltk',
        'retask==0.3',
    ],
    packages=['netcrawl'],
    zip_safe=False,
    entry_points="""
    [console_scripts]
    netcrawl_scanner = netcrawl:run_scanner
    netcrawl_chunker = netcrawl:run_chunker
    netcrawl_receiver = netcrawl:run_receiver
    netcrawl_dump = netcrawl:run_dump
    netcrawl_test = netcrawl:run_test
    netcrawl_spider = netcrawl:run_spider
    netcrawl_crawler = netcrawl:run_crawler
    netcrawl_indexer = netcrawl:run_indexer
    """
    )
