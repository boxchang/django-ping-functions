from django.conf.urls import url

from api.views import subnet_ping, ping

urlpatterns = [
    url(r'^subnet_ping/$', subnet_ping, name="subnet_ping"),
    url(r'^ping/$', ping, name="ping"),
]