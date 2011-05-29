from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='Products.UpfrontAccounting',
      version=version,
      description="Plone Accounting Package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone accounting ledger invoice cashbook',
      author='RC Compaan',
      author_email='roche at upfrontsystems dot co dot za',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.index',
          'Plone',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
