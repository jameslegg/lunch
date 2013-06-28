from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lunch.eat.views.home'),
    url(r'^manage/new_meal', 'lunch.eat.views.new_meal'),
    url(r'^manage/', 'lunch.eat.views.manage'),
    url(r'^add', 'lunch.eat.views.add_choice'),
    url(r'^delete', 'lunch.eat.views.delete_choice'),
    # url(r'^lunch/', include('lunch.foo.views.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + staticfiles_urlpatterns()
