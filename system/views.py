from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required as login_required
from system.models import ReviewCenter


def index(request):
    return render(request=request, template_name='index.html')

@login_required
def dashboard(request):
    context = {}
    menu = request.GET.get('menu', None)
    if not menu or menu == 'home':
        pass
    elif menu == 'reviewcenters':
        context['reviewcenters'] = ReviewCenter.objects.filter(active=True)
    elif menu == 'forums':
        context['can_add_question'] = True
    

    return render(request=request, template_name='system/dashboard.html', context=context)

@login_required
def video_tutorials(request):
    return render(request=request, template_name='system/video_tutorials.html')

@login_required
def quizzes(request):
    return render(request=request, template_name='system/quizzes.html')

@login_required
def reviewcenter_detail(request, slug):
    instance = ReviewCenter.objects.filter(slug__iexact = slug)
    if instance.exists():
        instance = instance.first()
    else:
        return HttpResponse('<h1>Review Center Not Found</h1>')
    context = {
        'reviewcenter': instance
    }
    return render(request, 'system/reviewcenter_detail.html', context)