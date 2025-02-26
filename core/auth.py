from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from core.config import settings

cookie_transport = CookieTransport(
    cookie_name="access_token",
    cookie_max_age=3600,
    cookie_secure=True,  # Установите в True, если используете HTTPS
    cookie_samesite="None",
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_jwt, lifetime_seconds=60*60*24*30*3)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
