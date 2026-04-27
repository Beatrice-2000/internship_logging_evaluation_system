from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/logbook/', include('logbook.urls')),
    path('api/evaluations/', include('evaluations.urls')),
    path('api/placements/', include('placements.urls')),
]