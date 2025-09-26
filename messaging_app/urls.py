from django.contrib import admin
from django.urls import path, include
from messaging_app.chats.auth import token_obtain_pair, token_refresh

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT endpoints
    path('api/token/', token_obtain_pair, name='token_obtain_pair'),
    path('api/token/refresh/', token_refresh, name='token_refresh'),

    # Include chats app URLs
    path('api/chats/', include('messaging_app.chats.urls')),
]


