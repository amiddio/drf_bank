from django.urls import path

from account.views import AccountTypeListAPIView

app_name = 'account'

urlpatterns = [
    path('account_types/', AccountTypeListAPIView.as_view(), name='account_types'),
]
