Data Quality Application for GeoNode
====================================

This is a GeoNode application aimed to publishing the data quality assessment results for the GMES Reference Data Access Lot 2 project. It defines a data model for quality results and some templates in order to retrieve and publish them. Furthermore it implements a tool for data choosing on a quality basis.

Installation
------------

#. Install the application::
	source bin/activate
	pip install -e git+git://github.com/sbsimo/quality.git

#. Add ``quality`` to the variable INSTALLED_APPS in the Django settings.py file

#. Add the following line to the variable TEMPLATE_DIRS in the Django settings.py file::
	os.path.join(PROJECT_ROOT, "..", "..", 'quality', 'quality', "templates"),

#. Append the following line to the Django urls.py module, in the variable urlpatterns::
	(r'^quality/', include('quality.urls')),

#. Modify the following line in the urls.py module:
	(r'^data/(?P<layername>[^/]*)$', 'geonode.maps.views.layerController'),

	and substitute with the following:
	(r'^data/(?P<layername>[^/]*)$', 'quality.views.layerController'),
	
#. Run ``syncdb`` command and reload the web server in order to get to see the application working
