import json

from annoying.decorators import render_to
import requests
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect

from training.core import (DAILYMILE_AUTH_URI, DAILYMILE_TOKEN_URI, oauth2_url,
                           oauth2_token)
from training.core.models import DailyMileProfile, Goal


def register_dailymile(request):
    auth_url = oauth2_url(DAILYMILE_AUTH_URI,
                          settings.DAILYMILE_CLIENT_ID,
                          settings.DAILYMILE_REDIRECT_URI)
    return HttpResponseRedirect(auth_url)


@render_to('core/success.html')
def register_dailymile_callback(request):
    user = authenticate(code=request.GET['code'])
    if user:
        login(request, user)
        if 'state' in request.GET.keys():
            if request.GET['state'] == 'website':
                HttpResponseRedirect(reverse('core_website_success'))
    return HttpResponseRedirect(reverse('index'))


@render_to('core/profile.html')
def profile_view(request, username):
    profile = DailyMileProfile.objects.filter(user__username__iexact=username)
    is_current_user = False
    stats = None

    if profile.exists():
        profile = profile.get()
        stats = profile.stats_as_json()
        is_current_user = profile.user == request.user
    else:
        profile = None

    return {'profile': profile,
            'is_current_user': is_current_user,
            'stats': stats,}

@login_required
def profile_view_self(request):
    return HttpResponseRedirect(
        reverse('core_profile_view',
                kwargs={'username': request.user.username}))

@render_to('core/goals_edit.html')
@login_required
def profile_goals_edit(request):
    user_profile = request.user.get_profile()
    GoalFormSet = inlineformset_factory(DailyMileProfile, Goal, extra=1)
    if request.method == "POST":
        import ipdb; ipdb.set_trace()
        goal_forms = GoalFormSet(request.POST, instance=user_profile)
        if goal_forms.is_valid:
            goal_forms.save()
            return HttpResponseRedirect(reverse('core_profile_view_self'))
    else:
        goal_forms = GoalFormSet(instance=user_profile)
    return {'goal_forms': goal_forms}
