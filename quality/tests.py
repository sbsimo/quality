"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""
from django.test import TestCase
from django.conf import settings
from geonode.maps.models import Map, MapLayer
from cartography.models import Document
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import StringIO

LOGIN_URL = settings.SITEURL + "accounts/login/"

def create_cartography():
	imgfile = StringIO.StringIO('GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
	                            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
	f = SimpleUploadedFile('test_img_file.gif', imgfile.read(), 'image/gif')
	m, __ = Map.objects.get_or_create(id=1, title='foo', projection='4326', zoom=2, center_x=0, center_y=0,
	                                  owner=User.objects.get_or_create(username='foo')[0])
	for ord, lyr in enumerate(settings.MAP_BASELAYERS):
		MapLayer.objects.from_viewer_config(
			map=m,
			layer=lyr,
			source=settings.MAP_BASELAYERSOURCES[lyr["source"]],
			ordering=ord
		).save()
	m.set_default_permissions()
	c, created = Document.objects.get_or_create(id=1, file=f)
	c.maps.add(m)
	return c, created


class EventsTest(TestCase):

	def test_map_details(self):
		"""/maps/1 -> Test accessing the detail view of a map"""
		create_cartography()
		map = Map.objects.get(id=1)
		c = Client()
		response = c.get("/maps/%s" % str(map.id))
		self.assertEquals(response.status_code, 200)

	def test_cartography_details(self):
		"""/cartography/1 -> Test accessing the detail view of a cartography"""
		create_cartography()
		cartography = Document.objects.get(id=1)
		c = Client()
		response = c.get("/cartography/%s" % str(cartography.id))
		self.assertEquals(response.status_code, 200)

	def test_access_cartography_upload_form(self):
		"""Test the form page is returned correctly via GET request /cartography/upload"""
		c = Client()
		User.objects.create_superuser('bobby', 'bobby@foo.com', 'bob')
		log = c.login(username='bobby', password='bob')
		self.assertTrue(log)
		response = c.get("/cartography/upload")
		self.assertTrue('Add document' in response.content)

	def test_cartography_isuploaded(self):
		"""/cartography/upload -> Test uploading a cartography"""
		imgfile = StringIO.StringIO('GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
		                            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
		f = SimpleUploadedFile('test_img_file.gif', imgfile.read(), 'image/gif')
		m, __ = Map.objects.get_or_create(id=1, title='foo', projection='4326', zoom=2, center_x=0, center_y=0,
		                                  owner=User.objects.get_or_create(username='foo')[0])
		c = Client()
		User.objects.create_superuser('bobby', 'bobby@foo.com', 'bob')
		c.login(username='bobby', password='bob')
		response = c.post("/cartography/upload", {'file': f, 'title': 'uploaded_cartography', 'map': m.id},
		                  follow=True)
		self.assertEquals(response.status_code, 200)

	def test_newmap_template(self):
		"""
		Test if the newmap template is returned correctly
		"""
		c = Client()
		response = c.get('/cartography/newmap')
		self.assertEquals(response.status_code, 200)

	def test_document_creation(self):
		"""
		Test if a document is created properly
		"""
		imgfile = StringIO.StringIO('GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
	                            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
		f = SimpleUploadedFile('test_img_file.gif', imgfile.read(), 'image/gif')
		m, __ = Map.objects.get_or_create(id=1, title='foo', projection='4326', zoom=2, center_x=0, center_y=0,
	                                  owner=User.objects.get_or_create(username='foo')[0])
		m.set_default_permissions()
		d,created = Document.objects.get_or_create(id=1, file=f)
		d.maps.add(m)
		self.assertTrue(created)