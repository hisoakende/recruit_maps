from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

from src import config

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=config.JWT_SECRET, lifetime_seconds=None)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
