from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def chatView(request):
    return render(request, 'chatapp/core/chat.html', {})