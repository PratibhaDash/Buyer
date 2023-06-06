from django.urls import path
from . import views

urlpatterns = [
    path('', views.FarmApi.as_view(), name='farm'),
    path('<int:pk>', views.FarmEditApi.as_view(), name='farm_details'),
    path('logs', views.FarmLogsApi.as_view(), name='farm_logs'),
    path('logs/<int:pk>', views.FarmLogDetailsApi.as_view(), name='farm_logs_details'),
    path('user/list', views.UserFarmApi.as_view(), name='user_farm_list'),
    path('user/stage', views.UserFarmStageApi.as_view(), name='user_farm_stage_list'),
    path('image/', views.FarmImageApi.as_view(), name='farm_image'),
    path('image/<int:pk>', views.FarmImageEditApi.as_view(), name='farm_image_details'),
    path('master/stage/', views.StageMasterApiView.as_view(), name='stage_master'),
    path('stage/', views.FarmStageApiView.as_view(), name='farm_stage'),
    path('stage/<int:pk>', views.FarmStageStatusApiView.as_view(), name='farm_stage_status'),
    path('stages/image/', views.FarmStageImageApiView.as_view(), name='farm_stage_image'),
    path('stages/image/<int:pk>', views.FarmStageImageEditApi.as_view(), name='farm_image_details'),
    path('farmer/payment', views.FarmerPaymentApi.as_view(), name='farm_payment'),
    path('farmer/payment/<int:pk>', views.FarmerPaymentEditApi.as_view(), name='farm_Payment_edit'),

]
