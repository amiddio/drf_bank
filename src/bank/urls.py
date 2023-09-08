from django.urls import path, include

from bank.routers import router
from bank.views import TransferAPIView, TransferHistoryViewSet

app_name = 'bank'

urlpatterns = [
    path('', include(router.urls)),
    path('transfer/', TransferAPIView.as_view(), name='transfer'),
    path('transfer_history/', TransferHistoryViewSet.as_view({'get': 'list'}), name='transfer_history'),
]
