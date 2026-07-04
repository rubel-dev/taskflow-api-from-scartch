

from app.core.security import create_access_token, verify_refresh_token
from app.exception.custom_exceptions import UnauthorizedException


def refresh_access_tokens_services(refresh_token: str):
    user_id = verify_refresh_token(refresh_token)

    if not user_id:
        raise UnauthorizedException("Invalid refresh token")
    new_access_token = create_access_token(
        data = {"user_id": user_id}
    )
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }