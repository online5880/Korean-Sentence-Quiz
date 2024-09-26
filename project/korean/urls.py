from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_text_analysis(request):
    return redirect('set_nickname')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_text_analysis, name='root'),
    path('', include('korean_app.urls')),
]