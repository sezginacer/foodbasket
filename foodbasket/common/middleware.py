import logging
import time
from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """Middleware to monitor request performance and log slow requests"""
    
    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log slow requests (> 1 second)
        if processing_time > 1.0:
            logger.warning(
                f"Slow request: {request.method} {request.path} "
                f"took {processing_time:.2f}s - Status: {response.status_code}"
            )
        
        # Add processing time to response headers
        response['X-Processing-Time'] = str(processing_time)
        
        return response


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log all requests for debugging"""
    
    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Log request details
        logger.info(
            f"Request: {request.method} {request.path} "
            f"from {request.META.get('REMOTE_ADDR', 'unknown')} "
            f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'unknown')}"
        )
        
        response = self.get_response(request)
        
        # Log response status
        logger.info(f"Response: {request.method} {request.path} - Status: {response.status_code}")
        
        return response

