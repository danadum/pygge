"""TCP implementation for Goodgame Empire connections."""

import socket
import threading
from .base_gge_socket import BaseGgeSocket


class BaseTcpSocket(BaseGgeSocket):
    """TCP socket implementation extending BaseGgeSocket."""

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
        super().__init__(server_header, on_send, on_open, on_message, on_error, on_close)
        self.url = url
        url = url.split("://")[1]
        self.host = url.split(":")[0]
        self.port = url.split(":")[1] if ":" in url else 443
        self.port = int(self.port)
        self.buffer = ""
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect_thread = threading.Thread(target=self.__connect)
        self.__connect_thread.daemon = True
        self.__connect_thread.start()

    def __connect(self) -> None:
        try:
            self.socket.connect((self.host, self.port))
            self._onopen(self)
            
            while not self.closed.is_set():
                try:
                    data = self.socket.recv(4096)
                    if not data:
                        break
                    self.__on_data(data)
                except Exception as e:
                    if not self.closed.is_set():
                        self._onerror(self, e)
                    break
            
            if not self.closed.is_set():
                self._onclose(self, 1000, "Connection closed")
        except Exception as e:
            self._onerror(self, e)
            self._onclose(self, 1006, "Connection error")

    def __on_data(self, data: bytes) -> None:
        self.buffer += data.decode("UTF-8")
        
        while "\x00" in self.buffer:
            null_index = self.buffer.index("\x00")
            message = self.buffer[:null_index]
            self.buffer = self.buffer[null_index + 1:]
            self._onmessage(self, message)

    def _send(self, data: str) -> None:
        self.socket.sendall((data + "\x00").encode("UTF-8"))

    def close(self) -> None:
        self.closed.set()
        self.socket.close()

    def run_forever(self, *args, **kwargs) -> None:
        """Keeps the connection alive (for compatibility with WebSocketApp)."""
        self.__connect_thread.join()
