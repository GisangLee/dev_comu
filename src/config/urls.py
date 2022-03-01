# from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("api-v1/accounts/", include("accounts.urls", namespace="accounts")),
    path("api-v1/posts/", include("posts.urls", namespace="posts")),
    # path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
