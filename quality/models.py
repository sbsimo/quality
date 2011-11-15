from django.db import models
from geonode.maps.models import Map, Layer
from django.db.models import signals
import os

#class Document(models.Model):
#	"""

#	A document is any kind of information that can be attached to a map such as pdf, images, videos, xls...

#	"""

#	title = models.CharField(max_length=255)
#	maps = models.ManyToManyField(Map)
#	file = models.FileField(upload_to='documents')
#	type = models.CharField(max_length=128,blank=True,null=True)

#	def __unicode__(self):
#		return self.title

#	@models.permalink
#	def get_absolute_url(self):
#		return self.file.url

#def pre_save_document(instance, sender, **kwargs):
#	base_name, extension = os.path.splitext(instance.file.name)
#	instance.type=extension[1:]

#signals.pre_save.connect(pre_save_document, sender=Document)

class QualityMatrix(models.Model):
    layer = models.OneToOneField(Layer)
    geographicExtent = models.IntegerField('Geographic Extent')
    licensingConstraint = models.IntegerField('Licensing and Constraint')
    scaleDenominator = models.IntegerField('Scale Denominator')
    update = models.IntegerField('Update')
    temporalExtent = models.IntegerField('Temporal Extent')
    fitness4Use = models.IntegerField('Fitness for Use')
    thematicRichness = models.IntegerField('Thematic Richness')
    integration = models.IntegerField('Integration')
    dataIntegrity = models.IntegerField('Data Integrity')
    positionalAccuracy = models.IntegerField('Positional Accuracy')
    thematicAccuracy = models.IntegerField('Thematic Accuracy')
    completeness = models.IntegerField('Completeness')

    def __unicode__(self):
        return "bravo"
