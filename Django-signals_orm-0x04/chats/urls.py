from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet, DeleteUserView

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
	*router.urls,
	path('users/delete/', DeleteUserView.as_view(), name='delete_user'),
]