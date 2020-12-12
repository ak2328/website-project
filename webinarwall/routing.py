from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import main_website.routing
from channels.sessions import SessionMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            main_website.routing.websocket_urlpatterns
        )
  ),
})