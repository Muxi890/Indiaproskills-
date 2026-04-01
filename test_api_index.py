from api.index import handler

class DummyRequest:
    def __init__(self, method="GET", path="/"):
        self.method = method
        self.path = path


def test_handler_root_status_ok():
    req = DummyRequest(method="GET", path="/")
    response = handler(req)
    assert response["statusCode"] == 200
    assert "Indiaproskills" in response["body"]


def test_handler_health_endpoint():
    req = DummyRequest(method="GET", path="/api/health")
    response = handler(req)
    assert response["statusCode"] == 200
    assert "health" in response["body"]


def test_handler_method_not_allowed():
    req = DummyRequest(method="DELETE", path="/")
    response = handler(req)
    assert response["statusCode"] == 405
    assert "error" in response["body"]