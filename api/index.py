def handle_request(request):
    try:
        if isinstance(request, dict):
            method = request.get('method')
            path = request.get('path')
        else:
            method = getattr(request, 'method', None)
            path = getattr(request, 'path', None)

        # Add your logic here based on method and path
        return f'Method: {method}, Path: {path}'
    except Exception as e:
        return '500 Internal Server Error'
    
# Usage example
# response = handle_request(request)