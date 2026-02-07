"""
This module contains the base class for Goodgame Empire socket connections.

The `BaseGgeSocket` class provides common functionality for sending and receiving messages.
"""

from __future__ import annotations

import json
import re
import threading
from typing import Callable


class BaseGgeSocket:
    """
    Base class for Goodgame Empire websocket connections.

    This class is a subclass of websocket.WebSocketApp and provides additional functionality for sending and receiving messages.

    Attributes:
        server_header (str): The server header to use.
        opened (threading.Event): An event that is set when the connection is opened.
        closed (threading.Event): An event that is set when the connection is closed.
    """

    def __init__(
        self,
        server_header: str,
        on_send: Callable[[BaseGgeSocket, str], None] = None,
        on_open: Callable[[BaseGgeSocket], None] = None,
        on_message: Callable[[BaseGgeSocket, str], None] = None,
        on_error: Callable[[BaseGgeSocket, Exception], None] = None,
        on_close: Callable[[BaseGgeSocket, int, str], None] = None,
    ) -> None:
        """
        Initializes the socket connection.

        Args:
            server_header (str): The server header to use.
            on_send (function, optional): A function to call when sending a message. Defaults to None.
            on_open (function, optional): A function to call when the connection is opened. Defaults to None.
            on_message (function, optional): A function to call when a message is received. Defaults to None.
            on_error (function, optional): A function to call when an error occurs. Defaults to None.
            on_close (function, optional): A function to call when the connection is closed. Defaults to None.

        Returns:
            None
        """
        self.server_header = server_header
        """ str: The server header to use. """
        self.__on_send = on_send
        """ function | None: A function to call when sending a message. """
        self.__on_open = on_open
        """ function | None: A function to call when the connection is opened. """
        self.__on_error = on_error
        """ function | None: A function to call when an error occurs. """
        self.__on_message = on_message
        """ function | None: A function to call when a message is received. """
        self.__on_close = on_close
        """ function | None: A function to call when the connection is closed. """
        self.opened = threading.Event()
        """ threading.Event: An event that is set when the connection is opened. """
        self.closed = threading.Event()
        """ threading.Event: An event that is set when the connection is closed. """
        self.__messages: list[dict] = []
        """ list[dict]: Internal list of messages waiting for a response. """

    def _onopen(self, ws: BaseGgeSocket) -> None:
        """
        Internal function which is called when the connection is opened.

        Args:
            ws (BaseGgeSocket): The socket connection object.

        Returns:
            None
        """
        self.opened.set()
        self.__on_open and self.__on_open(ws)

    def _onmessage(self, ws: BaseGgeSocket, message: str) -> None:
        """
        Internal function which is called when a message is received.

        Args:
            ws (BaseGgeSocket): The socket connection object.
            message (str): The message received.

        Returns:
            None
        """
        response = self.parse_response(message)
        self.__process_response(response)
        self.__on_message and self.__on_message(ws, message)

    def _onerror(self, ws: BaseGgeSocket, error: Exception) -> None:
        """
        Internal function which is called when an error occurs.

        Args:
            ws (BaseGgeSocket): The socket connection object.
            error (Exception): The error that occurred.

        Returns:
            None
        """
        self.__on_error and self.__on_error(ws, error)

    def _onclose(
        self, ws: BaseGgeSocket, close_status_code: int, close_msg: str
    ) -> None:
        """
        Internal function which is called when the connection is closed.

        Args:
            ws (BaseGgeSocket): The socket connection object.
            close_status_code (int): The status code of the close.
            close_msg (str): The message of the close.

        Returns:
            None
        """
        self.opened.clear()
        self.closed.set()
        self.__on_close and self.__on_close(ws, close_status_code, close_msg)

    def _send(self, data: str) -> None:
        """
        Internal method to send data. Must be implemented by subclass.

        Args:
            data (str): The data to send.

        Returns:
            None

        Raises:
            NotImplementedError: This method must be implemented by subclass.
        """
        raise NotImplementedError("_send() must be implemented by subclass")

    def close(self) -> None:
        """
        Closes the connection. Must be implemented by subclass.

        Returns:
            None

        Raises:
            NotImplementedError: This method must be implemented by subclass.
        """
        raise NotImplementedError("close() must be implemented by subclass")

    def send(self, data: str) -> None:
        """
        Sends a message over the socket connection.

        Args:
            data (str): The message to send.

        Returns:
            None
        """
        self.__on_send and self.__on_send(self, data)
        self._send(data)

    def __send_command_message(self, data: list[str]) -> None:
        """
        Internal function which sends a command message over the websocket connection.

        Args:
            data (list[str]): The data to send.

        Returns:
            None
        """
        self.send("%".join(["", *data, ""]))

    def send_raw_command(self, command: str, data: list[str]) -> None:
        """
        Sends a raw command over the websocket connection.

        Args:
            command (str): The command to send.
            data (list[str]): The data to send.

        Returns:
            None
        """
        self.__send_command_message(["xt", self.server_header, command, "1", *data])

    def send_json_command(self, command: str, data: dict) -> None:
        """
        Sends a JSON command over the websocket connection.

        Args:
            command (str): The command to send.
            data (dict): The data to send.

        Returns:
            None
        """
        self.__send_command_message(
            ["xt", self.server_header, command, "1", json.dumps(data)]
        )

    def send_xml_message(self, t: str, action: str, r: str, data: str) -> None:
        """
        Sends an XML message over the websocket connection.

        Args:
            t (str): The t attribute of the message.
            action (str): The action attribute of the message.
            r (str): The r attribute of the message.
            data (str): The data of the message.

        Returns:
            None
        """
        self.send(f"<msg t='{t}'><body action='{action}' r='{r}'>{data}</body></msg>")

    def __wait_for_response(
        self, type: str, conditions: dict, timeout: int = 5, count: int = 1
    ) -> dict:
        """
        Internal function which waits for a response with the specified type and conditions.

        Args:
            type (str): The expected type of the response.
            conditions (dict): The expected conditions of the response.
            timeout (int, optional): The timeout to wait for the response. Defaults to 5.
            count (int, optional): The number of expected responses. Defaults to 1. -1 or 0 for infinite.

        Returns:
            dict: The response if count is 1.
            list[dict]: The list of responses if count is greater than 1.

        Raises:
            TimeoutError: If the response is not received within the timeout.
        """
        event = threading.Event()
        message = {
            "type": type,
            "conditions": conditions,
            "responses": [],
            "event": event,
        }
        self.__messages.append(message)
        result = event.wait(timeout)
        if count != 1 and result:
            while True:
                event.clear()
                result = event.wait(0.1)
                if not result or len(message["responses"]) == count:
                    result = True
                    break
        self.__messages.remove(message)
        if not result:
            raise TimeoutError("Timeout waiting for response")
        if count == 1:
            response = message["responses"][0]
        else:
            response = message["responses"]
        return response

    def wait_for_json_response(
        self, command: str, data: dict | bool = False, timeout: int = 5, count: int = 1
    ) -> dict:
        """
        Waits for a JSON response with the specified command and data.

        Args:
            command (str): The expected command of the response.
            data (dict, optional): The expected data of the response. Defaults to False.
            timeout (int, optional): The timeout to wait for the response. Defaults to 5.
            count (int, optional): The number of expected responses. Defaults to 1. -1 or 0 for infinite.

        Returns:
            dict: The response if count is 1.
            list[dict]: The list of responses if count is greater than 1.

        Raises:
            TimeoutError: If the response is not received within the timeout.
        """
        return self.__wait_for_response(
            "json", {"command": command, "data": data}, timeout=timeout, count=count
        )

    def wait_for_xml_response(
        self, t: str, action: str, r: str, timeout: int = 5, count: int = 1
    ) -> dict:
        """
        Waits for an XML response with the specified t, action, and r attributes.

        Args:
            t (str): The expected t attribute of the response.
            action (str): The expected action attribute of the response.
            r (str): The expected r attribute of the response.
            timeout (int, optional): The timeout to wait for the response. Defaults to 5.
            count (int, optional): The number of expected responses. Defaults to 1. -1 or 0 for infinite.

        Returns:
            dict: The response if count is 1.
            list[dict]: The list of responses if count is greater than 1.

        Raises:
            TimeoutError: If the response is not received within the timeout.
        """
        return self.__wait_for_response(
            "xml",
            {
                "t": t,
                "action": action,
                "r": r,
            },
            timeout=timeout,
            count=count,
        )

    def raise_for_status(self, response: dict, expected_status: int = 0) -> None:
        """
        Raises an exception if the status of the response is not the expected status.

        Args:
            response (dict): The response to check.
            expected_status (int, optional): The expected status. Defaults to 0.

        Returns:
            None

        Raises:
            Exception: If the status of the response is not the expected status.
        """
        if (
            response["type"] == "json"
            and response["payload"]["status"] != expected_status
        ):
            raise Exception(f"Unexpected status: {response['payload']['status']}")

    def parse_response(self, response: str) -> dict:
        """
        Parses a response into a dictionary with the type and payload.

        Args:
            response (str): The response to parse.

        Returns:
            dict: The parsed response.
        """
        if response.startswith("<"):
            response = re.search(
                r"<msg t='(.*?)'><body action='(.*?)' r='(.*?)'>(.*?)</body></msg>",
                response,
            ).groups()
            return {
                "type": "xml",
                "payload": {
                    "t": response[0],
                    "action": response[1],
                    "r": response[2],
                    "data": response[3],
                },
            }
        else:
            response = response.strip("%").split("%")
            response = {
                "type": "json",
                "payload": {
                    "command": response[1],
                    "status": int(response[3]),
                    "data": "%".join(response[4:]) if len(response) > 4 else None,
                },
            }
            if response["payload"]["data"] and response["payload"]["data"].startswith(
                "{"
            ):
                response["payload"]["data"] = json.loads(response["payload"]["data"])
            return response

    def __process_response(self, response: dict) -> None:
        """
        Internal function which sets a waiting message as done if the response matches its conditions.

        Args:
            response (dict): The response to process.

        Returns:
            None
        """
        for message in self.__messages:
            if self.__compare_response(response, message):
                message["responses"].append(response)
                message["event"].set()
                break

    def __compare_response(self, response: dict, expected: dict) -> bool:
        """
        Compares a response to an expected response.

        Args:
            response (dict): The response to compare.
            expected (dict): The expected response.

        Returns:
            bool: True if the response matches the expected response, False otherwise.
        """
        if "json" == response["type"] == expected["type"] and response["payload"]["command"] == expected["conditions"]["command"]:
            if expected["conditions"]["data"] == False:
                return True
            elif expected["conditions"]["data"] == True and response["payload"]["data"] != None:
                return True
            elif None == expected["conditions"]["data"] == response["payload"]["data"]:
                return True
            elif {} == expected["conditions"]["data"] == response["payload"]["data"]:
                return True
            elif isinstance(response["payload"]["data"], dict) and isinstance(expected["conditions"]["data"], dict):
                if self.__compare_nested_headers(expected["conditions"]["data"], response["payload"]["data"]):
                    return True
        elif "xml" == response["type"] == expected["type"]:
            if response["payload"]["t"] == expected["conditions"]["t"] and response["payload"]["action"] == expected["conditions"]["action"] and response["payload"]["r"] == expected["conditions"]["r"]:
                return True
        return False
    
    def __compare_nested_headers(self, message: dict | None, response: dict | None) -> bool:
        if message is None or response is None:
            return False
        for key in message:
            if type(message) is not type(response):
                return False
            elif type(message[key]) is dict:
                if not self.__compare_nested_headers(message[key], response[key]):
                    return False
            else:
                if key not in response or response[key] != message[key]:
                    return False
        return True

