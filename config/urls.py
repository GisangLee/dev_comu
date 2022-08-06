
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api-v1/accounts/', include("accounts.urls", namespace="accounts")),
]

urlpatterns = [
    # ...
    path('__debug__/', include('debug_toolbar.urls')),
]
