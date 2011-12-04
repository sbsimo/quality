from geonode import settings
from geonode.maps.views import _perms_info, MAP_LEV_NAMES, _perms_info_json, \
LAYER_LEV_NAMES, _describe_layer
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from geonode.maps.models import Map, MapLayer, Layer
import json
from django.template import RequestContext, loader, Context
from django.utils.translation import ugettext as _
#from cartography.models import Document
from django.contrib.auth.decorators import login_required
from geonode.maps.views import default_map_config
from django.views.decorators.csrf import csrf_exempt
from quality.models import Subtopic, LayerSubtopic, QualityMatrix

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

@csrf_exempt
def layerController(request, layername):
    DEFAULT_MAP_CONFIG, DEFAULT_BASE_LAYERS = default_map_config()
    layer = get_object_or_404(Layer, typename=layername)
    if (request.META['QUERY_STRING'] == "describe"):
        return _describe_layer(request,layer)
    if (request.META['QUERY_STRING'] == "remove"):
        return _removeLayer(request,layer)
    if (request.META['QUERY_STRING'] == "update"):
        return _updateLayer(request,layer)
    if (request.META['QUERY_STRING'] == "style"):
        return _changeLayerDefaultStyle(request,layer)
    else:
        if not request.user.has_perm('maps.view_layer', obj=layer):
            return HttpResponse(loader.render_to_string('401.html',
                RequestContext(request, {'error_message':
                    _("You are not permitted to view this layer")})), status=401)

        metadata = layer.metadata_csw()

        maplayer = MapLayer(name = layer.typename, ows_url = settings.GEOSERVER_BASE_URL + "wms")

        # center/zoom don't matter; the viewer will center on the layer bounds
        map = Map(projection="EPSG:900913")

	qualityRecord = layer.qualitymatrix	

        return render_to_response('quality/layer.html', RequestContext(request, {
            "layer": layer,
            "metadata": metadata,
            "viewer": json.dumps(map.viewer_json(* (DEFAULT_BASE_LAYERS + [maplayer]))),
            "permissions_json": _perms_info_json(layer, LAYER_LEV_NAMES),
            "GEOSERVER_BASE_URL": settings.GEOSERVER_BASE_URL,
	    "qualityRecord": qualityRecord
            }))

GENERIC_UPLOAD_ERROR = _("There was an error while attempting to upload your data. \
Please try again, or contact and administrator if the problem continues.")

def listSubtopics(request):
    layerSubtopic = LayerSubtopic.objects.get(pk=1)
    subtopic = layerSubtopic.subtopic
    allLayerSubtopics = LayerSubtopic.objects.distinct('subtopic')
    t = loader.get_template('quality/subtopics.html')
    c = Context({
	'subtopic': subtopic,
	'allLS': allLayerSubtopics,
    })
#    return HttpResponse("this is an example page, the real implementation \
#    will follow!")
#    return HttpResponse(t.render(c))
    return render_to_response('quality/subtopics.html', RequestContext(request, {
	'subtopic': subtopic,
	'allLS': allLayerSubtopics,
	}))

def ask4weights(request):
	if request.method == 'GET':
		subtopic_pk = request.GET.__getitem__("subtopic")[0]
		subtopic = Subtopic.objects.get(pk=subtopic_pk)
		return render_to_response('quality/ask4weights.html', RequestContext(request, {
		'subtopic': subtopic,
		'subtopic_pk': subtopic_pk,
		}))
	else:
		return HttpResponse(loader.render_to_string('401.html',
                RequestContext(request, {'error_message':
                    _("You are not permitted to view this layer")})), status=401)

def calculateBest(request):
	if request.method == 'GET':
		scaleDenominator = request.GET.__getitem__("scaleDenominator")
		l1 = QualityMatrix.objects.get(pk=3).layer
		layername = l1.typename
		return layerController(request, layername)
#		return render_to_response('quality/temp.html', RequestContext(request, {
#		'scaleDenominator': scaleDenominator,
#		'layername': layername,
#		}))
	else:
		return HttpResponse(loader.render_to_string('401.html',
                RequestContext(request, {'error_message':
                    _("You are not permitted to view this layer")})), status=401)
