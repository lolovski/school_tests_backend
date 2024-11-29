from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from core.config import settings

cookie_transport = CookieTransport()
cookie_admin_transport = CookieTransport()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_jwt, lifetime_seconds=60*60*24*30*3)


def get_admin_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_admin_jwt, lifetime_seconds=60*60*24*30*3)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

auth_admin_backend = AuthenticationBackend(
    name="jwt_admin",
    transport=cookie_admin_transport,
    get_strategy=get_admin_jwt_strategy,
)