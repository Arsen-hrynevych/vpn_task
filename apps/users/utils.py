from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
import requests

from .forms import UserEditForm, CreateSiteForm
from .models import CreatedSite,PageTransitionStatistic


def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'dashboard/edit_profile.html', {'form': form})


def create_site(request):
    if request.method == 'POST':
        form = CreateSiteForm(request.POST)
        if form.is_valid():
            created_site = form.save(commit=False)
            created_site.user = request.user
            created_site.save()
            return redirect('dashboard')
    else:
        form = CreateSiteForm()

    context = {'form': form}
    return render(request, 'dashboard/create_site.html', context)


def internal_redirect(request, user_site_name, routes):
    try:
        original_site_url = f'{routes}'
        response = requests.get(original_site_url)

        response.raise_for_status()

        data_sent = sum(len(v) for v in response.request.headers.values())
        data_received = len(response.content)

        created_site = CreatedSite.objects.get(url=original_site_url)
        page_transition_statistic, created = PageTransitionStatistic.objects.get_or_create(site=created_site, site_name=user_site_name)

        page_transition_statistic.update_statistics(data_sent, data_received)

        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else 'utf-8'
        django_response = HttpResponse(response.content.decode(encoding), content_type=response.headers['Content-Type'])

        return django_response
    except requests.RequestException as e:
        return HttpResponseBadRequest(f"Internal redirection failed: {str(e)}")
    except Exception as e:
        return HttpResponseBadRequest(f"Internal error: {str(e)}")
