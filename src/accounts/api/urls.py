from django.urls import path
from accounts.api.views import (
    api_registration_view,
    account_properties_view,
    account_update_view,
)
from rest_framework.authtoken.views import obtain_auth_token


app_name = "account-api"

urlpatterns = [
    path('register/',api_registration_view, name= "api-register" ),
    path('login/', obtain_auth_token , name="api-login"),
    path('properties/', account_properties_view , name="api-properties"),
    path('properties/update', account_update_view , name="api-update"),

]

