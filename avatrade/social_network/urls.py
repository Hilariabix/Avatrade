from rest_framework.routers import SimpleRouter
from avatrade.social_network import views


router = SimpleRouter()
router.register('users', views.UserViewSet, basename="user")
router.register('posts', views.PostViewSet, basename="post")
router.register('likes', views.LikeViewSet, basename="like")
urlpatterns = router.urls
