from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('system.urls', namespace='system')),
    path('authentication/', include('authentication.urls', namespace='authentication')),
    path('jet/', include('jet.urls', namespace='jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', namespace='jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('faq/', include('faq.urls')),
    path('quiz/', include('quiz.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)