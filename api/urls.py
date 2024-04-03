from django.urls import path

from api.likes.views import LikeToggleView
from api.questions.views import QuestionListView, QuestionDetailView
from api.comments.views import CommentListView, CommentUpdateDeleteView
from api.user.views import ObtainTokenView

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('comments/', CommentListView.as_view(), name='comment_list'),
    path('comments/<int:pk>', CommentUpdateDeleteView.as_view(), name='comment_update_delete'),
    path('user/token/', ObtainTokenView.as_view(), name='obtain_token'),
    path('likes/', LikeToggleView.as_view(), name='like_toggle'),
]
