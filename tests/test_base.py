import pytest
from fastapi_rest_utils.viewsets.base import (
    BaseViewSet, ListView, RetrieveView, CreateView, UpdateView, PartialUpdateView, DeleteView
)
from fastapi_rest_utils.tests.conftest import TestProductSchema, TestProductCreateSchema, TestProductUpdateSchema

class MyListView(ListView):
    schema_config = {"list": {"response": TestProductSchema}}

class MyRetrieveView(RetrieveView):
    schema_config = {"retrieve": {"response": TestProductSchema}}

class MyCreateView(CreateView):
    schema_config = {
        "create": {
            "response": TestProductSchema,
            "payload": TestProductCreateSchema
        }
    }

class MyUpdateView(UpdateView):
    schema_config = {
        "update": {
            "response": TestProductSchema,
            "payload": TestProductUpdateSchema
        }
    }

class MyDeleteView(DeleteView):
    schema_config = {"delete": {"response": None}}

class ModelViewSet(BaseViewSet, MyListView, MyRetrieveView, MyCreateView, MyUpdateView, MyDeleteView):
    pass

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

def test_model_viewset_aggregates_all_route_configs():
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

def test_model_viewset_http_methods():
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

def test_model_viewset_paths():
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

@pytest.mark.parametrize(
    "view_cls, schema_config, expected_error, expected_msg",
    [
        # ListView
        (ListView, {"wrong_key": {"response": TestProductSchema}}, NotImplementedError, r"schema_config\['list'\]\['response'\] must be set"),
        (ListView, {"list": {}}, NotImplementedError, r"schema_config\['list'\]\['response'\] must be set"),
        (ListView, {"list": {"response": "not_a_model"}}, NotImplementedError, r"schema_config\['list'\]\['response'\] must be set"),
        # RetrieveView
        (RetrieveView, {"wrong_key": {"response": TestProductSchema}}, NotImplementedError, r"schema_config\['retrieve'\]\['response'\] must be set"),
        (RetrieveView, {"retrieve": {}}, NotImplementedError, r"schema_config\['retrieve'\]\['response'\] must be set"),
        (RetrieveView, {"retrieve": {"response": "not_a_model"}}, NotImplementedError, r"schema_config\['retrieve'\]\['response'\] must be set"),
        # CreateView
        (CreateView, {"create": {"response": TestProductSchema}}, NotImplementedError, r"schema_config\['create'\]\['payload'\] must be set"),
        (CreateView, {"create": {"payload": TestProductCreateSchema}}, NotImplementedError, r"schema_config\['create'\]\['response'\] must be set"),
        (CreateView, {"create": {"response": "not_a_model", "payload": TestProductCreateSchema}}, NotImplementedError, r"schema_config\['create'\]\['response'\] must be set"),
        (CreateView, {"create": {"response": TestProductSchema, "payload": "not_a_model"}}, NotImplementedError, r"schema_config\['create'\]\['payload'\] must be set"),
        # UpdateView
        (UpdateView, {"update": {"response": TestProductSchema}}, NotImplementedError, r"schema_config\['update'\]\['payload'\] must be set"),
        (UpdateView, {"update": {"payload": TestProductUpdateSchema}}, NotImplementedError, r"schema_config\['update'\]\['response'\] must be set"),
        (UpdateView, {"update": {"response": "not_a_model", "payload": TestProductUpdateSchema}}, NotImplementedError, r"schema_config\['update'\]\['response'\] must be set"),
        (UpdateView, {"update": {"response": TestProductSchema, "payload": "not_a_model"}}, NotImplementedError, r"schema_config\['update'\]\['payload'\] must be set"),
        # PartialUpdateView
        (PartialUpdateView, {"partial_update": {"response": TestProductSchema}}, NotImplementedError, r"schema_config\['partial_update'\]\['payload'\] must be set"),
        (PartialUpdateView, {"partial_update": {"payload": TestProductUpdateSchema}}, NotImplementedError, r"schema_config\['partial_update'\]\['response'\] must be set"),
        (PartialUpdateView, {"partial_update": {"response": "not_a_model", "payload": TestProductUpdateSchema}}, NotImplementedError, r"schema_config\['partial_update'\]\['response'\] must be set"),
        (PartialUpdateView, {"partial_update": {"response": TestProductSchema, "payload": "not_a_model"}}, NotImplementedError, r"schema_config\['partial_update'\]\['payload'\] must be set"),
    ]
)
def test_viewset_schema_config_errors(view_cls, schema_config, expected_error, expected_msg):
    # Dynamically create a subclass with the given schema_config
    attrs = {} if schema_config is None else {"schema_config": schema_config}
    TestView = type("TestView", (view_cls,), attrs)
    with pytest.raises(expected_error, match=expected_msg):
        TestView.route_config() 