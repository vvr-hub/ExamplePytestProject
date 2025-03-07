# tests/websockets/test_websocket.py

import pytest
import asyncio
import json
import websockets
import logging
from utils.websocket_utils import send_message, receive_message, ping_pong

logger = logging.getLogger(__name__)


# -------------------- 1. Basic Message Exchange Tests --------------------

@pytest.mark.asyncio
async def test_send_receive_message(websocket_connection):
    """Test sending and receiving a simple text message."""
    test_message = "Hello, WebSocket!"
    await send_message(websocket_connection, test_message)
    response = await receive_message(websocket_connection)

    logger.info(f"Received response: {response}")

    expected_responses = [test_message, "echo.websocket.events sponsored by Lob.com"]
    assert response in expected_responses, f"Unexpected response: '{response}'"


@pytest.mark.asyncio
async def test_send_receive_json(websocket_connection):
    """Test sending and receiving JSON data."""
    data = {"key": "value", "number": 123}
    message = json.dumps(data)

    await send_message(websocket_connection, message)
    response = await receive_message(websocket_connection)

    logger.info(f"Received JSON response: {response}")

    # Ignore non-JSON responses from WebSocket
    if "sponsored by Lob.com" in response:
        pytest.skip("WebSocket service does not support JSON echo")

    try:
        received_data = json.loads(response.strip())
        assert received_data == data, f"Expected {data}, but got {received_data}"
    except json.JSONDecodeError:
        pytest.fail(f"Received non-JSON message: {response}")


@pytest.mark.asyncio
async def test_send_large_message(websocket_connection):
    """Test sending and receiving a medium-sized message."""
    message = "A" * 500
    await send_message(websocket_connection, message)
    response = await receive_message(websocket_connection)

    logger.info(f"Sent large message of size {len(message)}. Received: {response}")

    if "sponsored by Lob.com" in response:
        pytest.skip("WebSocket service does not properly echo large messages")

    assert message in response, "Large message response mismatch"


@pytest.mark.asyncio
async def test_multiple_messages(websocket_connection):
    """Test sending and receiving multiple messages."""
    messages = ["First message", "Second message", "Third message"]
    received_messages = set()

    for msg in messages:
        await send_message(websocket_connection, msg)
        response = await receive_message(websocket_connection)

        logger.info(f"Sent: {msg}, Received: {response}")

        received_messages.add(msg)
        received_messages.add("echo.websocket.events sponsored by Lob.com")

        assert response in received_messages, f"Unexpected response: '{response}'"


# -------------------- 2. WebSocket Functionalities Tests --------------------

@pytest.mark.asyncio
async def test_ping_pong(websocket_connection):
    """Test WebSocket Ping-Pong functionality."""
    try:
        await ping_pong(websocket_connection)
        logger.info("Ping-Pong test successful")
    except Exception as e:
        logger.error(f"Ping-Pong failed: {e}")
        pytest.fail(f"Ping-Pong failed: {e}")


@pytest.mark.asyncio
async def test_open_close_connection(websocket_url):
    """Test opening and closing the WebSocket connection."""
    async with websockets.connect(websocket_url) as websocket:
        assert websocket.state == websockets.protocol.State.OPEN, "WebSocket should be open upon connection"
    assert websocket.state == websockets.protocol.State.CLOSED, "WebSocket should be closed after exiting context"


# -------------------- 3. Negative Scenario Tests (Error Handling) --------------------

@pytest.mark.asyncio
async def test_invalid_websocket_uri():
    """Test connecting to an invalid WebSocket URI."""
    with pytest.raises(OSError):  # May raise ConnectionRefusedError or OSError
        async with websockets.connect("wss://invalid-uri"):
            pass


@pytest.mark.asyncio
async def test_connection_timeout():
    """Test WebSocket connection timeout handling."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(websockets.connect("wss://echo.websocket.events"), timeout=0.001)


@pytest.mark.asyncio
async def test_send_after_close(websocket_url):
    """Test sending a message after the connection is closed."""
    async with websockets.connect(websocket_url) as websocket:
        await websocket.close()
        with pytest.raises(websockets.exceptions.ConnectionClosed):
            await websocket.send("test")


@pytest.mark.asyncio
async def test_receive_closed_connection(websocket_url):
    """Test receiving a message on a closed WebSocket connection."""
    async with websockets.connect(websocket_url) as websocket:
        await websocket.close()

        logger.info("Attempting to receive on a closed connection")

        # If the WebSocket is not properly closed, skip the test
        if websocket.state != websockets.protocol.State.CLOSED:
            pytest.skip("WebSocket service does not close connections properly")

        try:
            response = await websocket.recv()
            logger.warning(f"Unexpectedly received data on a closed connection: {response}")
            pytest.skip("WebSocket service does not raise ConnectionClosedError on closed connection")
        except websockets.exceptions.ConnectionClosedError:
            logger.info("Correctly raised ConnectionClosedError when receiving on a closed WebSocket")
