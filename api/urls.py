from rest_framework import routers
from api import views as api_views

router = routers.SimpleRouter()
router.register(r'users', api_views.UserViewData, basename="user")
router.register(r'posts', api_views.getMultiplePostData, basename="post")
urlpatterns = router.urls