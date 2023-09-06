from django.urls import path, include

from bank.routers import router
from bank.views import TransferAPIView

app_name = 'bank'

urlpatterns = [
    path('', include(router.urls)),
    path('transfer/', TransferAPIView.as_view(), name='transfer'),
]
