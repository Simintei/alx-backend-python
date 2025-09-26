from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# You can expose TokenObtainPairView and TokenRefreshView here if you want
# e.g. from .auth import token_obtain_pair, token_refresh in urls.py
token_obtain_pair = TokenObtainPairView.as_view()
token_refresh = TokenRefreshView.as_view()
