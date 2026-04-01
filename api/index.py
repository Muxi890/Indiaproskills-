"""Vercel Serverless Function entrypoint for Indiaproskills-.

This file is used by Vercel when deploying the `api/` function.
"""

from __future__ import annotations

def handler(request):
    """HTTP handler for Vercel functions.
    
    Vercel passes request as an object with attributes, not a dict.
    We need to use getattr() instead of .get() to safely access properties.
    """
    try:
        # Extract method from request object using getattr
        method = getattr(request, 'method', 'GET')
        if not method:
            method = 'GET'
        method = method.upper()

        # Validate HTTP method
        if method not in ("GET", "HEAD", "OPTIONS", "POST"):
            return {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": '{"error": "Method Not Allowed"}',
            }

        # Extract path from request object
        path = getattr(request, 'path', None)
        if not path:
            # Try to get path from url attribute
            url = getattr(request, 'url', None)
            if url and isinstance(url, str):
                # Extract path from URL
                path = url.split('?')[0] if '?' in url else url
            else:
                path = "/"
        
        # Ensure path starts with /
        if not isinstance(path, str):
            path = "/"
        elif not path.startswith('/'): 
            path = '/' + path

        # Handle root and api endpoints
        if path in ("/", "/api", "/api/index.py"):
            payload = {
                "status": "ok",
                "message": "Indiaproskills serverless function is running",
                "path": path,
                "method": method,
            }
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": str(payload).replace("'", '"'),
            }

        # Handle health check endpoint
        if path == "/api/health":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": '{"health": "pass"}',
            }

        # 404 for unknown paths
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": '{"error": "Not Found"}',
        }

    except Exception as e:
        # Return error details for debugging
        import traceback
        error_trace = traceback.format_exc()
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"error": "Internal Server Error", "message": "{str(e)}"}}',
        }