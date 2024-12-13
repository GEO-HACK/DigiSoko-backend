from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from  .import views

urlpatterns = [
    path('products/',views.products, name = 'products'),
    path('products/<int:id>',views.product_details, name = 'product_details'),
    path('products/related/<str:category_name>/', views.related_products, name='related-products'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
