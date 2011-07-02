#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup


setup(
        name=u'{app_name}'.encode('utf-8'),
        version='0.1',
        author=u'{author}'.encode('utf-8'),
        author_email=u'{author_email}'.encode('utf-8'),
        packages=['{package_name}',]
        package_dir={{'{package_name}': 'src'}},
        #package_data={{'{package_name}': []}},
                                        # List of data files to be included 
                                        # into package.
        requires=[                      # Dependencies for the package.
            'distribute',
            ],
        scripts=[],                     # List of python script files.
        #data_files=[('/etc/init.d', ['init-script'])]
                                        # List of files, which have to
                                        # be installed into specific 
                                        # locations.
        #url='',                        # Home page.
        #download_url='',               # Page from which package could
                                        # be downloaded.
        description=u'{app_name}'.encode('utf-8'),
        long_description=(
            open('README.rst').read()+open('CHANGES.txt').read()),
        # Full list of classifiers could be found at:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 1 - Planning',
            #'Environment :: Console',
            #'Framework :: Django',
            'Intended Audience :: Developers',
            (
                'License :: OSI Approved :: '
                'GNU Library or Lesser General Public License (LGPL)'),
            #'Natural Language :: Lithuanian',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            (
                'Topic :: Software Development :: Libraries :: '
                'Python Modules'),
            ],
        licence='LGPL'
        )
