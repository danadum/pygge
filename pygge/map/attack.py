"""
Module for handling attack operations in Goodgame Empire.

This module defines the `Attack` class, which provides a method to send an attack with various 
parameters, including army composition, lord selection, horses, tools, and other modifiers.
"""

from ..base_gge_socket import BaseGgeSocket


class Attack(BaseGgeSocket):
    """
    A class for handling attack operations in Goodgame Empire.

    This class provides a method to send an attack, allowing customization of army composition,
    attack strategy, and various modifiers.
    """

    def send_attack(
        self,
        kingdom,
        sx,
        sy,
        tx,
        ty,
        army,
        lord_id=0,
        horses_type=-1,
        feathers=0,
        slowdown=0,
        boosters=[],
        support_tools=[],
        final_wave=[],
        sync=True,
        quiet=False,
    ):
        """
        Send an attack to a target location.

        Args:
            kingdom (int): The ID of the kingdom where the attack is being sent.
            sx (int): The x-coordinate of the starting position.
            sy (int): The y-coordinate of the starting position.
            tx (int): The x-coordinate of the target.
            ty (int): The y-coordinate of the target.
            army (list): The composition of the attacking army.
            lord_id (int, optional): The ID of the lord leading the attack. Defaults to 0.
            horses_type (int, optional): The type of horses used (-1 for default). Defaults to -1.
            feathers (int, optional): Whether to use feathers to speed up the attack. Defaults to 0.
            slowdown (int, optional): The amount of slowdown applied. Defaults to 0.
            boosters (list, optional): List of boosters applied to the attack. Defaults to an empty list.
            support_tools (list, optional): List of support tools used in the attack. Defaults to an empty list.
            final_wave (list, optional): The composition of the final wave of the attack. Defaults to an empty list.
            sync (bool, optional): If True, waits for a response and returns it. Defaults to True.
            quiet (bool, optional): If True, suppresses exceptions and returns False on failure. Defaults to False.

        Returns:
            dict: The response from the server if `sync` is True.
            bool: True if the operation was successful and `sync` is False, False if it failed and `quiet` is True.

        Raises:
            Exception: If an error occurs and `quiet` is False.
        """
        try:
            self.send_json_command(
                "cra",
                {
                    "SX": sx,
                    "SY": sy,
                    "TX": tx,
                    "TY": ty,
                    "KID": kingdom,
                    "LID": lord_id,
                    "WT": 0,
                    "HBW": horses_type,
                    "BPC": 0,
                    "ATT": 0,
                    "AV": 0,
                    "LP": 0,
                    "FC": 0,
                    "PTT": feathers,
                    "SD": slowdown,
                    "ICA": 0,
                    "CD": 99,
                    "A": army,
                    "BKS": boosters,
                    "AST": support_tools,
                    "RW": final_wave,
                    "ASCT": 0,
                },
            )
            if sync:
                response = self.wait_for_json_response("cra")
                self.raise_for_status(response)
                return response
            return True
        except Exception as e:
            if not quiet:
                raise e
            return False
