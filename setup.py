from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-helloresource',
	version=version,
	description="",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='malex',
	author_email='alexakis@imis.athena-innovation.gr',
	url='',
	license='GPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.helloresource'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
    [ckan.plugins]
	helloresource = ckanext.helloresource.plugin:HelloResourcePlugin

    [ckan.celery_task]
    tasks = ckanext.helloresource.celery_import:task_imports
	""",
)
