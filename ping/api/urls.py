from django.conf.urls import url

from api.views import ping_1

urlpatterns = [
    url(r'^ping/$', ping_1, name="ping"),
]