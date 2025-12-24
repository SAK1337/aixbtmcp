"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient

from mcp_aixbt.main import app
from mcp_aixbt.config import Settings


@pytest.fixture
def test_settings():
    """Provide test configuration."""
    return Settings(
        aixbt_api_key="test_api_key_12345",
        host="127.0.0.1",
        port=8000,
        debug=True,
        log_level="DEBUG",
        cache_ttl_seconds=0,  # Disable caching in tests
    )


@pytest.fixture
def client(test_settings):
    """Provide test client with mocked settings."""
    with patch("mcp_aixbt.config.get_settings", return_value=test_settings):
        with TestClient(app) as test_client:
            yield test_client


@pytest.fixture
def mock_aixbt_response():
    """Factory for mock AIXBT API responses."""
    def _make_response(data, status=200, pagination=None):
        response = {"status": status, "data": data}
        if pagination:
            response["pagination"] = pagination
        return response
    return _make_response


@pytest.fixture
def sample_project():
    """Provide sample project data."""
    return {
        "id": "507f1f77bcf86cd799439011",
        "name": "ethereum",
        "xHandle": "ethereum",
        "momentumScore": 0.85,
        "popularityScore": 18,
        "coingeckoData": {
            "apiId": "ethereum",
            "symbol": "eth",
            "categories": ["Smart Contract Platform"]
        },
        "signals": []
    }


@pytest.fixture
def sample_signal():
    """Provide sample signal data."""
    return {
        "id": "signal123",
        "detectedAt": "2025-12-23T10:00:00Z",
        "reinforcedAt": "2025-12-23T11:00:00Z",
        "description": "Major protocol upgrade announced",
        "projectName": "ethereum",
        "projectId": "507f1f77bcf86cd799439011",
        "category": "TECH_EVENT",
        "officialSources": ["https://ethereum.org"],
        "clusters": [{"id": "c1", "name": "DeFi"}]
    }
