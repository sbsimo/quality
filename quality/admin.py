from django.contrib import admin
#from cartography.models import Document

class DocumentAdmin(admin.ModelAdmin):
	filter_horizontal = ('maps',)

#admin.site.register(Document,DocumentAdmin)
