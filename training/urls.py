from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(template_name='core/index.html'),
        name='index'),

    url(r'^register/dailymile$',
        'training.core.views.register_dailymile',
        name='core_register_dailymile'),

    url(r'^register/dailymile-callback$',
        'training.core.views.register_dailymile_callback',
        name='core_register_dailymile_callback'),

    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'),

    url(r'^profile/(?P<username>[\w.@+-]+)$',
        'training.core.views.profile_view',
        name='core_profile_view'),
)
