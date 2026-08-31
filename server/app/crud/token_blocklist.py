from datetime import datetime, timezone
from app.core.redis_client import redis_client


def revoke_token(jti: str, expires_at: datetime) -> None:
    ttl_seconds = int((expires_at - datetime.now(timezone.utc)).total_seconds())
    if ttl_seconds > 0:
        redis_client.setex(f"revoked_token:{jti}", ttl_seconds, "1")


def is_token_revoked(jti: str) -> bool:
    return redis_client.exists(f"revoked_token:{jti}") == 1
