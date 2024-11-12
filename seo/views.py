from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import RobotsTxt


def robots_txt(request):
    robots = get_object_or_404(RobotsTxt)
    return HttpResponse(robots.content, content_type="text/plain")
