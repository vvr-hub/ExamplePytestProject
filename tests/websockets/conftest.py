# tests/websockets/conftest.py

import pytest_asyncio
import websockets
from config.config_loader import ConfigLoader


@pytest_asyncio.fixture(scope='session')
def config():
    return ConfigLoader()


@pytest_asyncio.fixture(scope='session')
def websocket_url(config):
    return config.get_websocket_url()


@pytest_asyncio.fixture(scope='function')
async def websocket_connection(websocket_url):
    async with websockets.connect(websocket_url) as websocket:
        yield websocket  # Ensures WebSocket is properly opened and closed
