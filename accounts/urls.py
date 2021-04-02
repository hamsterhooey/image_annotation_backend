from django.urls import path
from .views import SignupView, BlacklistTokenView, UserDetailView

app_name = "accounts"

urlpatterns = [
    path("signup", SignupView.as_view(), name="create_users"),
    path("logout/blacklist/", BlacklistTokenView.as_view(), name="blacklist"),
    path("user/<email>", UserDetailView.as_view(), name="user_detail"),
]