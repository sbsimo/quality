from geonode.maps.views import _perms_info, MAP_LEV_NAMES
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from geonode.maps.models import Map, MapLayer
import json
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
#from cartography.models import Document
from django.contrib.auth.decorators import login_required
from geonode.maps.views import default_map_config

#imgtypes = ['jpg','jpeg','tif','tiff','png','gif']

#def documentdetail(request, docid):
#	"""
#	The view that show details of each document
#	"""
#	document = get_object_or_404(Document, pk=docid)
#	map = document.maps.all()[0]
#	if not request.user.has_perm('maps.view_map', obj=map):
#		return HttpResponse(loader.render_to_string('401.html',
#			RequestContext(request, {'error_message':
#				_("You are not allowed to view this map.")})), status=401)

#	return render_to_response("cartography/docinfo.html", RequestContext(request, {
#		'map': map,
#		'permissions_json': json.dumps(_perms_info(map, MAP_LEV_NAMES)),
#		'document': document,
#	    'imgtypes': imgtypes
#	}))

#def newmaptpl(request):
#	config = default_map_config()[0]
#	return render_to_response('cartography/newmaptpl.html',RequestContext(request, {'config':json.dumps(config)}))

#@login_required
#def upload_document(request,mapid=None):
#	if request.method == 'GET':
#		return render_to_response('cartography/document_upload.html',
#		                          RequestContext(request,{'mapid':mapid,}),
#		                          context_instance=RequestContext(request)
#		)

#	elif request.method == 'POST':
#		mapid = str(request.POST['map'])
#		file = request.FILES['file']
#		title = request.POST['title']
#		document = Document(title=title, file=file)
#		document.save()
#		document.maps.add(Map.objects.get(id=mapid))
#		return HttpResponse(json.dumps({'success': True,'redirect_to':'/maps/' + str(mapid)}))
