from rest_framework import routers
from .views import *

router = routers.SimpleRouter()

# Router list
router.register(r'accounts', AccountViewSet, basename='Account')
