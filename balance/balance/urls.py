from django.conf.urls import patterns, include, url
from bal.views import login,index,add,transdetails, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       ('^index/$',index),
                       ('^login/$',login),
                       ('^add/$',add),
                       ('^trans/([\d]+)$',transdetails),
                       ('^logout/$',logout),
    # Examples:
    # url(r'^$', 'balance.views.home', name='home'),
    # url(r'^balance/', include('balance.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
