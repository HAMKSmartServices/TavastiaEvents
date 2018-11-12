from django.core.urlresolvers import reverse
from django.conf.urls import url, include
from django.views.generic import View

from .views import message_event

from django.views.generic import TemplateView

app_name = 'tavastiaevents'
urlpatterns = [
    url(r'report/', message_event, name='message-event'),
    url(r'documentation/$', TemplateView.as_view(template_name="rest_framework/api_info.html"), name='documentation')

]
