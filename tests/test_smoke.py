"""Basic smoke tests for DriftBench SDK."""

def test_import_cli():
    """Test that the CLI module can be imported."""
    try:
        from cli import main as cli_main
        assert cli_main.cli is not None
    except ImportError as e:
        assert False, f"Failed to import cli.main: {e}"

def test_import_api():
    """Test that the API module can be imported."""
    try:
        from sdk import api as sdk_api
        assert sdk_api.app is not None
    except ImportError as e:
        assert False, f"Failed to import sdk.api: {e}"

# TODO: Add more comprehensive tests later

