from django.shortcuts import render
from .models import Profesores

def profesor_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if Profesores.objects.filter(usuario=request.user).exists():
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'base/403_custom.html', status=403)
    return _wrapped_view_func