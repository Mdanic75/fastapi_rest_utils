import pytest
from conftest import TestProductCreateSchema, TestProductSchema, TestProductUpdateSchema

from fastapi_rest_utils.viewsets.base import (
    CreateView,
    DeleteView,
    ListView,
    PartialUpdateView,
    RetrieveView,
    UpdateView,
)


class MyListView(ListView):
    schema_config = {"list": {"response": TestProductSchema}}


class MyRetrieveView(RetrieveView):
    schema_config = {"retrieve": {"response": TestProductSchema}}


class MyCreateView(CreateView):
    schema_config = {
        "create": {"response": TestProductSchema, "payload": TestProductCreateSchema}
    }


class MyUpdateView(UpdateView):
    schema_config = {
        "update": {"response": TestProductSchema, "payload": TestProductUpdateSchema}
    }


class MyDeleteView(DeleteView):
    schema_config = {"delete": {"response": None}}


class ModelViewSet(
    MyListView, MyRetrieveView, MyCreateView, MyUpdateView, MyDeleteView
):
    schema_config = {
        "list": {"response": TestProductSchema},
        "retrieve": {"response": TestProductSchema},
        "create": {"response": TestProductSchema, "payload": TestProductCreateSchema},
        "update": {"response": TestProductSchema, "payload": TestProductUpdateSchema},
        "delete": {"response": None},
    }


# Error test classes
class InvalidListView(ListView):
    # Missing schema_config - should raise NotImplementedError
    pass


class InvalidListView2(ListView):
    # Wrong schema structure - should raise NotImplementedError
    schema_config = {"wrong_key": {"response": TestProductSchema}}


class InvalidListView3(ListView):
    # Missing response - should raise NotImplementedError
    schema_config = {"list": {}}


class InvalidListView4(ListView):
    # Response is not a Pydantic model - should raise NotImplementedError
    schema_config = {"list": {"response": "not_a_model"}}


class InvalidCreateView(CreateView):
    # Missing payload - should raise NotImplementedError
    schema_config = {"create": {"response": TestProductSchema}}


def test_model_viewset_aggregates_all_route_configs() -> None:
    vs = ModelViewSet()
    configs = vs.routes_config()

    # Should have 5 route configs (list, retrieve, create, update, delete)
    assert len(configs) == 5

    # Check each endpoint is present
    endpoint_names = [c["endpoint_name"] for c in configs]
    assert "list" in endpoint_names
    assert "retrieve" in endpoint_names
    assert "create" in endpoint_names
    assert "update" in endpoint_names
    assert "delete" in endpoint_names

    # Check response models
    list_config = next(c for c in configs if c["endpoint_name"] == "list")
    assert list_config["response_model"] is TestProductSchema

    retrieve_config = next(c for c in configs if c["endpoint_name"] == "retrieve")
    assert retrieve_config["response_model"] is TestProductSchema

    create_config = next(c for c in configs if c["endpoint_name"] == "create")
    assert create_config["response_model"] is TestProductSchema

    update_config = next(c for c in configs if c["endpoint_name"] == "update")
    assert update_config["response_model"] is TestProductSchema

    delete_config = next(c for c in configs if c["endpoint_name"] == "delete")
    assert delete_config["response_model"] is None


def test_model_viewset_http_methods() -> None:
    vs = ModelViewSet()
    configs = vs.routes_config()

    # Check HTTP methods
    list_config = next(c for c in configs if c["endpoint_name"] == "list")
    assert list_config["method"] == "GET"

    retrieve_config = next(c for c in configs if c["endpoint_name"] == "retrieve")
    assert retrieve_config["method"] == "GET"

    create_config = next(c for c in configs if c["endpoint_name"] == "create")
    assert create_config["method"] == "POST"

    update_config = next(c for c in configs if c["endpoint_name"] == "update")
    assert update_config["method"] == "PUT"

    delete_config = next(c for c in configs if c["endpoint_name"] == "delete")
    assert delete_config["method"] == "DELETE"


def test_model_viewset_paths() -> None:
    vs = ModelViewSet()
    configs = vs.routes_config()

    # Check paths
    list_config = next(c for c in configs if c["endpoint_name"] == "list")
    assert list_config["path"] == ""

    retrieve_config = next(c for c in configs if c["endpoint_name"] == "retrieve")
    assert retrieve_config["path"] == "/{id}"

    create_config = next(c for c in configs if c["endpoint_name"] == "create")
    assert create_config["path"] == ""

    update_config = next(c for c in configs if c["endpoint_name"] == "update")
    assert update_config["path"] == "/{id}"

    delete_config = next(c for c in configs if c["endpoint_name"] == "delete")
    assert delete_config["path"] == "/{id}"
