from django.conf.urls.defaults import patterns, url
#from cartography.models import Document
#from cartography.views import documentdetail,newmaptpl,upload_document

#info_dict = {
#	'queryset': Document.objects.all(),
#	}

#urlpatterns = patterns('',
#	(r'^(?P<docid>\d+)$', documentdetail),
 #   (r'^upload/(?P<mapid>\d+)/?$', upload_document),
#	url(r'^upload/?$', 'cartography.views.upload_document', name='document-upload'),
#	(r'^newmap$', newmaptpl),
#)
urlpatterns = patterns('',
    url(r'^subtopics/','quality.views.listSubtopics'),
    url(r'^ask4weights/','quality.views.ask4weights'),
)
