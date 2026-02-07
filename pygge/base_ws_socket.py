"""WebSocket implementation for Goodgame Empire connections."""

import websocket
from .base_gge_socket import BaseGgeSocket


class BaseWsSocket(BaseGgeSocket, websocket.WebSocketApp):
    """WebSocket implementation extending BaseGgeSocket."""

    def __init__(
        self,
        url: str,
        server_header: str,
        on_send = None,
        on_open = None,
        on_message = None,
        on_error = None,
        on_close = None,
        *args,
        **kwargs,
    ) -> None:
        BaseGgeSocket.__init__(self, server_header, on_send, on_open, on_message, on_error, on_close)
        self.url = url
        
        websocket.WebSocketApp.__init__(
            self,
            url,
            on_open=self.__onopen,
            on_message=self.__onmessage,
            on_error=self.__onerror,
            on_close=self.__onclose,
            *args,
            **kwargs,
        )

    def __onopen(self, ws: websocket.WebSocketApp) -> None:
        self._onopen(ws)

    def __onmessage(self, ws: websocket.WebSocketApp, message: bytes) -> None:
        message = message.decode("UTF-8")
        self._onmessage(ws, message)

    def __onerror(self, ws: websocket.WebSocketApp, error: Exception) -> None:
        self._onerror(ws, error)

    def __onclose(self, ws: websocket.WebSocketApp, close_status_code: int, close_msg: str) -> None:
        self._onclose(ws, close_status_code, close_msg)

    def _send(self, data: str) -> None:
        websocket.WebSocketApp.send(self, data)

    def close(self) -> None:
        websocket.WebSocketApp.close(self)
