from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

{% if cookiecutter.include_sample_content == 'Y' -%}
from {{ cookiecutter.pkg_name }}.{{ cookiecutter.first_app_name }}.rest import ImageViewSet
from {{ cookiecutter.pkg_name }}.{{ cookiecutter.first_app_name }}.views import GalleryView, image_summary
{% endif %}
router = routers.SimpleRouter()
{% if cookiecutter.include_sample_content == 'Y' -%}
router.register(r'images', ImageViewSet)
{% endif %}

# OpenAPI generation
schema_view = get_schema_view(
    openapi.Info(title='{{ cookiecutter.project_name }}', default_version='v1', description=''),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/docs/redoc', schema_view.with_ui('redoc'), name='docs-redoc'),
    path('api/docs/swagger', schema_view.with_ui('swagger'), name='docs-swagger'),
    path('api/s3-upload/', include('s3_file_field.urls')),
    path('summary/', image_summary, name='image-summary'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
