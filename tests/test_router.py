from fastapi_rest_utils.router import RestRouter


def test_router_registers_routes_and_openapi(mock_viewset_with_routes):
    router = RestRouter()
    router.register_viewset(mock_viewset_with_routes, "/mock")

    assert len(router.routes) == 2

    post_route = next((r for r in router.routes if "POST" in getattr(r, "methods", [])), None)
    assert post_route is not None

    if hasattr(post_route, "openapi_extra"):
        openapi_extra = post_route.openapi_extra
    else:
        openapi_extra = getattr(post_route.endpoint, "openapi_extra", None)
    assert openapi_extra is not None
    assert "requestBody" in openapi_extra
