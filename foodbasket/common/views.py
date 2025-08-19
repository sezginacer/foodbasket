import logging
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.conf import settings
import redis

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Basic health check endpoint"""
    return JsonResponse({"status": "healthy", "service": "foodbasket"})


@csrf_exempt
@require_http_methods(["GET"])
def system_status(request):
    """Comprehensive system status check"""
    status = {
        "status": "healthy",
        "database": "unknown",
        "cache": "unknown",
        "redis": "unknown",
        "version": "1.0.0"
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            status["database"] = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        status["database"] = "unhealthy"
        status["status"] = "degraded"
    
    # Check cache
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            status["cache"] = "healthy"
        else:
            status["cache"] = "unhealthy"
            status["status"] = "degraded"
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        status["cache"] = "unhealthy"
        status["status"] = "degraded"
    
    # Check Redis PubSub
    try:
        pubsub_config = getattr(settings, 'PUBSUB_CONFIG', {})
        if pubsub_config.get('class', '').endswith('RedisPubSub'):
            redis_options = pubsub_config.get('options', {})
            r = redis.Redis(
                host=redis_options.get('host', 'localhost'),
                port=redis_options.get('port', 6379),
                db=redis_options.get('db', 1),
                socket_connect_timeout=5
            )
            r.ping()
            status["redis"] = "healthy"
        else:
            status["redis"] = "not_configured"
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        status["redis"] = "unhealthy"
        status["status"] = "degraded"
    
    # Return appropriate HTTP status
    if status["status"] == "healthy":
        return JsonResponse(status, status=200)
    elif status["status"] == "degraded":
        return JsonResponse(status, status=503)
    else:
        return JsonResponse(status, status=500)

