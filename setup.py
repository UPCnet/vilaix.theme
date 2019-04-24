from setuptools import setup, find_packages
import os

version = '1.18.dev0'

README = open("README.rst").read()
HISTORY = open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='vilaix.theme',
      version=version,
      description='Vilaix genweb flavour',
      long_description=README + "\n" + HISTORY,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='theme genweb plone',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://git.upcnet.es/{{package.name}}}.git',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['vilaix'],
      extras_require={'test': ['plone.app.testing[robot]>=4.2.2']},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'genweb.theme',
          'Products.PloneFormGen',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
