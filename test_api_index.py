# Updated DummyRequest Class

class DummyRequest:
    def __init__(self, method, path, **kwargs):
        self.method = method
        self.path = path
        # Initialize attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, item):
        # Define behavior for getattr to return None if attribute doesn't exist
        return None

    def __repr__(self):
        return f"DummyRequest(method={self.method}, path={self.path})"