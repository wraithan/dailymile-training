from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(template_name='core/index.html'),
        name='index'),

    url(r'^loggedout$',
        TemplateView.as_view(template_name='core/index.html'),
        kwargs={'from': 'logout'},
        name='loggedout'),

    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {'next_page': '/loggedout'},
        name='logout'),

    url(r'^about$',
        TemplateView.as_view(template_name='core/about.html'),
        name='about'),

    url(r'^stats$',
        'training.core.views.stats',
        name='stats'),

    url(r'^register/dailymile$',
        'training.core.views.register_dailymile',
        name='core_register_dailymile'),

    url(r'^register/dailymile-callback$',
        'training.core.views.register_dailymile_callback',
        name='core_register_dailymile_callback'),

    url(r'^profile/me$',
        'training.core.views.profile_view_self',
        name='core_profile_view_self'),

    url(r'^profile/(?P<username>[\w.@+-]+)$',
        'training.core.views.profile_view',
        name='core_profile_view'),

    url(r'^profile/goals/edit$',
        'training.core.views.profile_goals_edit',
        name='core_profile_goals_edit'),
)
