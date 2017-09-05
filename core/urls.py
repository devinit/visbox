from django.conf.urls import url
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = [
    url(r'^$',views.index,name='core.views.index'),
    url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='core.views.login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'core/logout.html'}, name='core.views.logout'),
    url(r'^signup/$', views.signup, name='core.views.signup'),
    url(r'^start/$', views.start, name='core.views.start'),
    url(r'^dataset/(?P<datasetPK>.+)/$', views.dataset, name='core.views.dataset'),
    url(r'^csv/(?P<datasetPK>.+).csv/$', views.csv, name='core.views.csv'),
    url(r'^deleteDataset/(?P<datasetPK>.+)/$', views.deleteDataset, name='core.views.deleteDataset'),
    url(r'^delete/(?P<chartPK>\d+)/$', views.deleteVis, name='core.views.deleteVis'),
    url(r'^create/(?P<chart>[\w\-]+)/(?P<datasetPK>\d+)/$', views.createVis, name='core.views.createVis'),
    url(r'^view/(?P<chartPK>\d+)/$', views.viewVis, name='core.views.viewVis'),
    url(r'^edit/(?P<chartPK>\d+)/$', views.editVis, name='core.views.editVis'),
    url(r'^gallery/$', views.gallery, name='core.views.gallery'),
    url(r'^api/(?P<templatePK>\d+)/$',views.api,name='core.views.api'),
    url(r'^config/(?P<templatePK>\d+)/$',views.config,name='core.views.config'),
]
