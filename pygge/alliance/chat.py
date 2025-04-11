"""
This module contains the class for interacting with the Goodgame Empire API's chat-related functions.

The `Chat` class provides methods for retrieving chat messages. It is a subclass of `BaseGgeSocket`.
"""

from ..base_gge_socket import BaseGgeSocket


class Chat(BaseGgeSocket):
    """
    A class for interacting with the Goodgame Empire API's chat-related functions.

    This class provides methods for retrieving chat messages. It is a subclass of `BaseGgeSocket`.
    """

    def get_alliance_chat(
        self, sync: bool = True, quiet: bool = False
    ) -> dict | bool:
        """
        Retrieve the alliance chat messages.

        Args:
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            dict: The response from the server if `sync` is True.
            bool: True if the operation was successful and `sync` is False. False if the operation failed and `quiet` is True.

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        try:
            self.send_json_command("acl", {})
            if sync:
                response = self.wait_for_json_response("acl")
                self.raise_for_status(response)
                return response
            return True
        except Exception as e:
            if not quiet:
                raise e
            return False
