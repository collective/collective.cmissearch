# Copyright (c) 2013 Beleidsdomein Leefmilieu, Natuur en Energie (LNE) and Vlaamse Milieumaatschappij (VMM). All rights reserved.
# See also LICENSE.txt

import os
from setuptools import setup, find_packages

version = '1.1dev'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.rst')
    + '\n' +
    read('docs/HISTORY.txt')
    )

setup(name='collective.cmissearch',
      version=version,
      description="CMIS search for Plone",
      long_description=long_description,
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        ],
      keywords='CMIS connection search plone',
      author='Sylvain Viollon',
      author_email='sylvain@infrae.com',
      url='http://pypi.python.org/pypi/collective.cmissearch',
      license='GPL',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          "collective.cmisbrowser",
          ],
      )
