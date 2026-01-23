import pytest
import os
import tempfile


def pytest_addoption(parser):
    parser.addoption(
        "--use-keyvault-secrets",
        help='Get secrets from a keyvault instead of the environment.',
        action='store_true', default=False
)


@pytest.fixture(scope="session")
def use_keyvault_secrets(request) -> str:
    return request.config.getoption("use_keyvault_secrets")


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Set up minimal environment variables for tests."""
    # Create a temporary .env file for tests
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        f.write("AZURE_OPENAI_MODEL=test-model\n")
        f.write("AZURE_OPENAI_ENDPOINT=https://test.openai.azure.com\n")
        test_env_path = f.name
    
    # Set the DOTENV_PATH environment variable
    os.environ['DOTENV_PATH'] = test_env_path
    
    yield
    
    # Cleanup
    try:
        os.unlink(test_env_path)
    except:
        pass
