from django.urls import path, include

from bank.routers import router
from . import views

app_name = 'bank'

urlpatterns = [
    path('', include(router.urls)),
    path('transfer/', views.TransferAPIView.as_view(), name='transfer'),
    path('pay_a_bill/', views.PayABillAPIView.as_view(), name='pay_a_bill'),
    path('transfer_history/', views.TransferHistoryViewSet.as_view({'get': 'list'}), name='transfer_history'),
    path('merchants/', views.MerchantViewSet.as_view({'get': 'list'}), name='merchant'),
]
