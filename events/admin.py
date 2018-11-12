from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext as _
from leaflet.admin import LeafletGeoAdmin
from modeltranslation.admin import TranslationAdmin
from reversion.admin import VersionAdmin
from events.api import generate_id
from events.models import Place, License, DataSource, Event, Offer, Keyword, KeywordLabel, KeywordSet, EventLink, Image


class BaseAdmin(admin.ModelAdmin):
    exclude = ("created_by", "modified_by",)

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user
        obj.save()

class OfferInline(admin.TabularInline):
    model = Offer
    extra = 0

class EventLinkInline(admin.TabularInline):
    model = EventLink
    extra = 0

class EventModelAdmin(BaseAdmin, TranslationAdmin, VersionAdmin):
    list_display = ('pin', 'id', 'name' , 'provider')
    inlines = [
        OfferInline,
        EventLinkInline
    ]

admin.site.register(Event, EventModelAdmin)

class ImageModelAdmin(BaseAdmin, VersionAdmin):
    model = Image

admin.site.register(Image, ImageModelAdmin)

class KeywordAdmin(BaseAdmin, TranslationAdmin, VersionAdmin):
    model = Keyword

admin.site.register(Keyword, KeywordAdmin)

class KeywordSetAdmin(BaseAdmin, TranslationAdmin, VersionAdmin):
    filter_horizontal = ('keywords',) 

admin.site.register(KeywordSet, KeywordSetAdmin)


class HelsinkiGeoAdmin(LeafletGeoAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (60.171944, 24.941389),
        'DEFAULT_ZOOM': 11,
        'MIN_ZOOM': 3,
        'MAX_ZOOM': 19,
    }


class PlaceAdmin(HelsinkiGeoAdmin, BaseAdmin, TranslationAdmin, VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('publisher', 'name', 'description', 'info_url', 'position')

        }),
        (_('Contact info'), {
            'fields': (
                'email', 'telephone', 'contact_type', 'street_address',
                'address_locality', 'address_region', 'postal_code', 'post_office_box_num')
        }),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # use https CDN instead
        self.openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'

    def save_model(self, request, obj, form, change):
        system_id = settings.SYSTEM_DATA_SOURCE_ID
        obj.data_source_id = system_id
        if not obj.id:
            #obj.id = generate_id(system_id)
            obj.id = generate_id()
        #obj.origin_id = obj.id.split(':')[1]

        super().save_model(request, obj, form, change)


admin.site.register(Place, PlaceAdmin)


class DataSourceAdmin(BaseAdmin):
    fields = ('id', 'name', 'api_key', 'owner', 'user_editable')


admin.site.register(DataSource, DataSourceAdmin)


class LanguageAdmin(BaseAdmin, VersionAdmin):
    pass


class PersonAdmin(BaseAdmin, VersionAdmin):
    pass


class LicenseAdmin(BaseAdmin, TranslationAdmin, VersionAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id']
        else:
            return []


admin.site.register(License, LicenseAdmin)


#class EventAdmin(Event)
