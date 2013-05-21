from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='vilaix.theme',
      version=version,
      description='Vilaix genweb flavour',
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
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
          'five.grok',
          'genweb.theme',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
