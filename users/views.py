from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    profile = request.user.profile

    context = {
        "profile": profile,
    }

    return render(request, "dashboard.html", context)