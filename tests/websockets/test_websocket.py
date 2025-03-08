import pytest
import asyncio
import json
import websockets
import logging
import base64
from utils.websocket_utils import send_message, receive_message, ping_pong

logger = logging.getLogger(__name__)


# -------------------- 1. Basic Message Exchange Tests --------------------

@pytest.mark.asyncio
async def test_send_receive_message(websocket_connection):
    """Test sending and receiving a simple text message."""
    test_message = "Hello, WebSocket!"
    await send_message(websocket_connection, test_message)
    response = await receive_message(websocket_connection)

    logger.info(f"Sent: {test_message}, Received: {response}")

    assert response == test_message, f"Unexpected response: '{response}'"


@pytest.mark.asyncio
async def test_send_receive_json(websocket_connection):
    """Test sending and receiving JSON data."""
    data = {"key": "value", "number": 123}
    message = json.dumps(data)

    await send_message(websocket_connection, message)
    response = await receive_message(websocket_connection)

    logger.info(f"Sent JSON: {message}, Received JSON: {response}")

    try:
        received_data = json.loads(response.strip())
        assert received_data == data, f"Expected {data}, but got {received_data}"
    except json.JSONDecodeError:
        pytest.fail(f"Received non-JSON message: {response}")


@pytest.mark.asyncio
async def test_send_large_message(websocket_connection):
    """Test sending and receiving a large message."""
    message = "A" * 500  # Keeping message size manageable
    await send_message(websocket_connection, message)
    response = await receive_message(websocket_connection)

    logger.info(f"Sent large message of size {len(message)}. Received: {response}")

    assert response == message, "Large message response mismatch"


@pytest.mark.asyncio
async def test_multiple_messages(websocket_connection):
    """Test sending and receiving multiple messages."""
    messages = ["First message", "Second message", "Third message"]

    for msg in messages:
        await send_message(websocket_connection, msg)
        response = await receive_message(websocket_connection)

        logger.info(f"Sent: {msg}, Received: {response}")

        assert response == msg, f"Unexpected response: '{response}'"


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
    # implicit close.
    assert websocket.state == websockets.protocol.State.CLOSED, "WebSocket should be closed after exiting context"


# -------------------- 3. Negative Scenario Tests (Error Handling) --------------------

@pytest.mark.asyncio
async def test_invalid_websocket_uri():
    """Test connecting to an invalid WebSocket URI."""
    with pytest.raises(OSError) as excinfo:  # Capture exception info
        async with websockets.connect("wss://invalid-uri"):
            pass
    assert "nodename nor servname provided, or not known" in str(excinfo.value) or "Connection refused" in str(
        excinfo.value)


@pytest.mark.asyncio
async def test_connection_timeout():
    """Test WebSocket connection timeout handling."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(websockets.connect("wss://ws.postman-echo.com/raw"), timeout=0.1)


@pytest.mark.asyncio
async def test_send_after_close(websocket_url):
    """Test sending a message after the connection is closed."""
    async with websockets.connect(websocket_url) as websocket:
        await websocket.close()
        with pytest.raises(websockets.exceptions.ConnectionClosed) as excinfo:
            await websocket.send("test")
        assert excinfo.value.rcvd.code in [1000, 1001, 1005, 1006]


@pytest.mark.asyncio
async def test_receive_closed_connection(websocket_url):
    """Test receiving a message on a closed WebSocket connection."""
    async with websockets.connect(websocket_url) as websocket:
        await websocket.close()

    logger.info("Attempting to receive on a closed connection")

    if websocket.state != websockets.protocol.State.CLOSED:
        pytest.skip("WebSocket service does not close connections properly")

    with pytest.raises(
            (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK)) as excinfo:
        await websocket.recv()
    assert excinfo.value.rcvd.code in [1000, 1001, 1005, 1006]


# -------------------- 4. Edge Case Tests --------------------
@pytest.mark.asyncio
async def test_send_receive_binary(websocket_connection):
    """Test sending and receiving binary data."""
    binary_data = b'\x00\x01\x02\x03'
    encoded_data = base64.b64encode(binary_data).decode('utf-8')  # encode to base64.
    await websocket_connection.send(encoded_data)
    response = await websocket_connection.recv()
    decoded_response = base64.b64decode(response)  # decode base64.
    assert decoded_response == binary_data

    logger.info(f"Sent Binary: {binary_data}, Received Binary: {decoded_response}")


@pytest.mark.asyncio
async def test_send_empty_message(websocket_connection):
    """Test sending an empty message."""
    await websocket_connection.send("")
    response = await websocket_connection.recv()
    assert response in ["", None], "Unexpected response for empty message"
    logger.info("Sent empty message, and recieved empty message.")


@pytest.mark.asyncio
async def test_send_receive_mixed_data(websocket_connection):
    """Test sending and receiving mixed data types."""
    mixed_data = [b'\x04\x05', "Hello", 123, {"key": "value"}]
    for item in mixed_data:
        if isinstance(item, bytes):
            encoded_item = base64.b64encode(item).decode('utf-8')
            await websocket_connection.send(encoded_item)
            response = await websocket_connection.recv()
            decoded_response = base64.b64decode(response)
            assert decoded_response == item
        elif isinstance(item, (str, int, dict)):
            message = json.dumps(item)
            await websocket_connection.send(message)
            response = await websocket_connection.recv()
            try:
                response_data = json.loads(response)
                assert response_data == item
            except json.JSONDecodeError:
                pytest.fail(f"Received non-JSON response: {response}")

        logger.info(f"Sent: {item}, Received: {response}")
