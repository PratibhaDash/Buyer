from django.urls import path
from . import views

urlpatterns = [
    path('product/variant', views.VariantApi.as_view(), name='variant'),
    path('product/variant/deleted', views.VariantDeletedApi.as_view(), name='variant'),
    path('product/variant/<int:pk>', views.VariantEditApi.as_view(), name='variant_details'),
    path('product', views.ProductApi.as_view(), name='product'),
    path('product/deleted', views.ProductDeletedApi.as_view(), name='product'),
    path('product/<int:pk>', views.ProductEditApi.as_view(), name='product_details'),
    path('', views.CategoryApi.as_view(), name='category'),
    path('deleted', views.CategoryDeletedApi.as_view(), name='category'),
    path('<int:pk>', views.CategoryEditApi.as_view(), name='category_details'),
    path('product/variant/image/', views.VariantImageApi.as_view(), name='variant_image'),
    path('product/variant/image/deleted/', views.VariantImageDeletedApi.as_view(), name='variant_image'),
    path('product/variant/image/<int:pk>', views.VariantImageEditApi.as_view(), name='variant_image_details'),
]
