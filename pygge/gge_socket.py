"""
This module contains the main class for interacting with the Goodgame Empire API.

The`GgeSocket` class is a subclass of all the other classes in the `pygge` package. It is a convenience class that allows you to interact with the Goodgame Empire API using a single object.
"""

from .account.account import Account
from .account.auth import Auth
from .account.emblem import Emblem
from .account.friends import Friends
from .account.settings import Settings

from .alliance.help import Help
from .alliance.chat import Chat

from .army.hospital import Hospital
from .army.soldiers import Soldiers
from .army.tools import Tools
from .army.units import Units

from .building.buildings_inventory import BuildingsInventory
from .building.buildings import Buildings
from .building.extension import Extension
from .building.repair import Repair
from .building.wall import Wall

from .castle.castle import Castle
from .castle.defense import Defense

from .events.beyond_the_horizon import BeyondTheHorizon
from .events.events import Events
from .events.fortune_teller import FortuneTeller
from .events.imperial_patronage import ImperialPatronage
from .events.lucky_wheel import LuckyWheel
from .events.mercenary_camp import MercenaryCamp
from .events.outer_realms import OuterRealms
from .events.technicus import Technicus
from .events.wishing_well import WishingWell

from .generals.tavern import Tavern

from .gifts.castle_gifts import CastleGifts
from .gifts.daily_gifts import DailyGifts
from .gifts.gifts import Gifts

from .lords.lords import Lords

from .map.attack import Attack
from .map.bookmarks import Bookmarks
from .map.map import Map
from .map.movements import Movements
from .map.ruins import Ruins
from .map.spy import Spy

from .shop.bestseller import Bestseller
from .shop.kings_market import KingsMarket
from .shop.shop import Shop
from .shop.shopping_cart import ShoppingCart
from .shop.special_offers import SpecialOffers
from .shop.specialist import Specialist

from .tutorial.tutorial import Tutorial

from .utils.system import System

from .misc.build_items import BuildItems
from .misc.global_effects import GlobalEffects
from .misc.quests import Quests
from .misc.tax import Tax


class GgeSocket(
    Account,
    Auth,
    Emblem,
    Friends,
    Settings,
    Help,
    Chat,
    Hospital,
    Soldiers,
    Tools,
    Units,
    BuildingsInventory,
    Buildings,
    Extension,
    Repair,
    Wall,
    Castle,
    Defense,
    BeyondTheHorizon,
    Events,
    FortuneTeller,
    ImperialPatronage,
    LuckyWheel,
    MercenaryCamp,
    OuterRealms,
    Technicus,
    WishingWell,
    Tavern,
    CastleGifts,
    DailyGifts,
    Gifts,
    Lords,
    Attack,
    Bookmarks,
    Map,
    Movements,
    Ruins,
    Spy,
    Bestseller,
    KingsMarket,
    Shop,
    ShoppingCart,
    SpecialOffers,
    Specialist,
    Tutorial,
    System,
    BuildItems,
    GlobalEffects,
    Quests,
    Tax,
):
    """
    The main class for interacting with the Goodgame Empire API.

    This class is a subclass of all the other classes in the `pygge` package. It is a convenience class that allows you to interact with the Goodgame Empire API using a single object.
    """

    def open_quest_book(self, sync: bool = True, quiet: bool = False) -> None:
        """
        Simulates the opening of the quest book.

        Args:
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        self.tracking_recommended_quests(quiet=quiet)
        self.get_quests(sync=sync, quiet=quiet)

    def open_tax_menu(self, sync: bool = True, quiet: bool = False) -> None:
        """
        Simulates the opening of the tax menu.

        Args:
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        self.get_tax_infos(sync=sync, quiet=quiet)
        self.get_tax_infos(sync=sync, quiet=quiet)

    def open_defense_menu(
        self, x: int, y: int, castle_id: int, sync: bool = True, quiet: bool = False
    ) -> None:
        """
        Simulates the opening of the defense menu.

        Args:
            x (int): The x-coordinate of the castle.
            y (int): The y-coordinate of the castle.
            castle_id (int): The ID of the castle.
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        self.get_castle_defense(x, y, castle_id, sync=sync, quiet=quiet)
        self.get_lords(sync=sync, quiet=quiet)

    def close_defense_menu(self, sync: bool = True, quiet: bool = False) -> None:
        """
        Simulates the closing of the defense menu.

        Args:
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        self.get_units_inventory(sync=sync, quiet=quiet)

    def open_construction_menu(self, sync: bool = True, quiet: bool = False) -> None:
        """
        Simulates the opening of the construction menu.

        Args:
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        self.get_building_inventory(sync=sync, quiet=quiet)

    def open_barracks(self, sync: bool = True, quiet: bool = False) -> None:
        """
        Simulates the opening of the barracks.

        Args:
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        self.get_detailed_castles(sync=sync, quiet=quiet)
        self.get_recruitment_queue(sync=sync, quiet=quiet)
        self.get_units_inventory(sync=sync, quiet=quiet)

    def open_workshop(self, sync: bool = True, quiet: bool = False) -> None:
        """
        Simulates the opening of the workshop.

        Args:
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        self.get_detailed_castles(sync=sync, quiet=quiet)
        self.get_production_queue(sync=sync, quiet=quiet)
        self.get_units_inventory(sync=sync, quiet=quiet)

    def open_hospital(self, sync: bool = True, quiet: bool = False) -> None:
        """
        Simulates the opening of the hospital.

        Args:
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        self.get_detailed_castles(sync=sync, quiet=quiet)

    def open_map(self, kingdom: int, sync: bool = True, quiet: bool = False) -> None:
        """
        Simulates the opening of the map.

        Args:
            kingdom (int): The kingdom number to open the map for.
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False.
        """
        self.get_bookmarks(sync=sync, quiet=quiet)
        self.get_map_chunk(kingdom, 0, 0, sync=sync, quiet=quiet)

    def skip_generals_tutorial(self, sync: bool = True, quiet: bool = False) -> None:
        """
        Skips the generals tutorial.

        Args:
            sync (bool, optional): If True, wait for a response and return it. Defaults to True.
            quiet (bool, optional): If True, suppress exceptions and return False on failure. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the operation and `quiet` is False
        """
        self.get_offerings_status(sync=sync, quiet=quiet)
        self.complete_quest_condition(1, "visitGeneralsInn", sync=sync, quiet=quiet)
        self.skip_generals_intro(sync=sync, quiet=quiet)
