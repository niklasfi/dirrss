from django.conf.urls import url
from dirrss import views

urlpatterns = [
	url(r'^$', views.index, name="dirrss_index"),
	url(r'^(?P<folder>[^/]+)/$', views.FolderFeed(), name="dirrss_feed"),
]
