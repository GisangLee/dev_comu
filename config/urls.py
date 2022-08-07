from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import perms
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="project name",
        default_version='프로젝트 버전 ( 1.0 )',
        description="API 문서",
        #terms_of_service="https://www.google.com/policies/terms/",
        #contact=openapi.Contact(email="이메일"), # 부가정보
        #license=openapi.License(name="mit"),     # 부가정보
    ),
    public=True,
    permission_classes=[perms.AllowAny],
)


urlpatterns = [
    #path('admin/', admin.site.urls),
    path(r'api-v1/swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'api-v1/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'api-v1/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path('api-v1/accounts/', include("accounts.urls", namespace="accounts")),
    path('api-v1/posts/', include("posts.urls", namespace="posts")),
    #path('api-v1/comments/', include("comments.urls", namespace="comments")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    # ...
    path('__debug__/', include('debug_toolbar.urls')),
]
