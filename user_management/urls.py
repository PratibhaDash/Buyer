from django.urls import path
from . import views

urlpatterns = [
    path('list', views.UserListApi.as_view(), name='user_list'),
    path('register', views.RegisterApi.as_view(), name='register'),
    path('profile', views.UserActionApi.as_view(), name='user_profile'),
    path('<int:pk>', views.UserModifyApi.as_view(), name='user_modify_profile'),
    path('search', views.UserSearchApi.as_view(), name='user_search'),
    path('status/<int:pk>', views.UserStatusApiView.as_view(), name='user_status'),
    path('password', views.UserChangePasswordApi.as_view(), name='user_password_change'),
    path('reset/password/<int:pk>', views.UserPasswordResetApi.as_view(), name='user_password_reset'),
    path('role/users', views.UserRolesApi.as_view(), name='role_user'),
    path('role/users/<int:pk>', views.UserRoleActionApi.as_view(), name='role_user_details'),
    path('role', views.RoleApi.as_view(), name='role'),
    path('role/<int:pk>', views.RoleActionApi.as_view(), name='role_details'),
    path('account/bank', views.UserBankApi.as_view(), name='user_bank'),
    path('account/bank/<int:pk>', views.UserBankEditApi.as_view(), name='user_bank_details'),
    path('account/upi', views.UserUpiApi.as_view(), name='user_upi'),
    path('account/upi/<int:pk>', views.UserUpiEditApi.as_view(), name='user_upi_details'),
    path('stats', views.AdminStatsApiView.as_view(), name='admin_stats'),

]
