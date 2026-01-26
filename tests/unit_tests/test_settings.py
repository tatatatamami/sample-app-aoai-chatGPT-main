import os
import pytest
from importlib import import_module, reload


@pytest.fixture(scope="function")
def dotenv_path(request):
    test_case_name = request.node.originalname.partition("test_")[2]
    return os.path.join(
        os.path.dirname(__file__),
        "dotenv_data",
        test_case_name
    )


@pytest.fixture(scope="function")
def app_settings(dotenv_path):
    # Reload module object to pick up new environment
    os.environ["DOTENV_PATH"] = dotenv_path
    settings_module = import_module("backend.settings")
    settings_module = reload(settings_module)
    
    yield getattr(settings_module, "app_settings")


def test_dotenv_no_datasource_1(app_settings):    
    # Validate model object
    assert app_settings.base_settings.datasource_type is None
    assert app_settings.datasource is None
    assert app_settings.azure_openai is not None
    
    
def test_dotenv_no_datasource_2(app_settings):    
    # Validate model object
    assert app_settings.datasource is None
    assert app_settings.azure_openai is not None

    
def test_dotenv_with_azure_search_success(app_settings):
    # Validate model object
    assert app_settings.search is not None
    assert app_settings.base_settings.datasource_type == "AzureCognitiveSearch"
    assert app_settings.datasource is not None
    assert app_settings.datasource.service == "search_service"
    assert app_settings.azure_openai is not None
    
    # Validate API payload structure
    payload = app_settings.datasource.construct_payload_configuration()
    assert payload["type"] == "azure_search"
    assert payload["parameters"] is not None
    assert payload["parameters"]["endpoint"] == "https://search_service.search.windows.net"
    print(payload)


def test_dotenv_with_elasticsearch_success(app_settings):
    # Validate model object
    assert app_settings.search is not None
    assert app_settings.base_settings.datasource_type == "Elasticsearch"
    assert app_settings.datasource is not None
    assert app_settings.datasource.endpoint == "dummy"
    assert app_settings.azure_openai is not None
    
    # Validate API payload structure
    payload = app_settings.datasource.construct_payload_configuration()
    assert payload["type"] == "elasticsearch"
    assert payload["parameters"] is not None
    assert payload["parameters"]["endpoint"] == "dummy"
    print(payload)


def test_dotenv_foundry_disabled(app_settings):
    # Validate model object
    assert app_settings.foundry is not None
    assert app_settings.foundry.enabled is False
    assert app_settings.azure_openai is not None
    print(f"Foundry settings: enabled={app_settings.foundry.enabled}")


def test_dotenv_foundry_enabled(app_settings):
    # Validate model object
    assert app_settings.foundry is not None
    assert app_settings.foundry.enabled is True
    assert app_settings.foundry.endpoint == "https://test-foundry.example.com/api/agent"
    assert app_settings.foundry.bearer_token == "test-bearer-token-12345"
    assert app_settings.azure_openai is not None
    print(f"Foundry settings: enabled={app_settings.foundry.enabled}, endpoint={app_settings.foundry.endpoint}")
