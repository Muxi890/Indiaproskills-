"""Vercel Serverless Function entrypoint for Indiaproskills-.

This file is used by Vercel when deploying the `api/` function.
"""

from __future__ import annotations


def _normalize_path(request):
    path = getattr(request, "path", None)
    if not path:
        url = getattr(request, "url", None)
        path = getattr(url, "path", "/") if url is not None else "/"
    return path or "/"


def handler(request):
    """HTTP handler for Vercel functions."""
    method = getattr(request, "method", "GET").upper()

    if method not in ("GET", "HEAD", "OPTIONS", "POST"):
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": "{\"error\": \"Method Not Allowed\"}",
        }

    path = _normalize_path(request)

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

    if path == "/api/health":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": "{\"health\": \"pass\"}",
        }

    return {
        "statusCode": 404,
        "headers": {"Content-Type": "application/json"},
        "body": "{\"error\": \"Not Found\"}",
    }
