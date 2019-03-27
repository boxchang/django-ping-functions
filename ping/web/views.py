from django.shortcuts import render

def base(request):
    return render(request, 'web/base.html', locals())