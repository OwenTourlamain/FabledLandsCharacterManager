class Error(Exception):
    """Base class for exceptions in this module"""

class InventoryFullError(Error):
    """Exception raised when a characters inventory is full"""

class ItemNotFoundError(Error):
    """Exception raised when an item is not found in a charcters inventory"""

class NoteNotFoundError(Error):
    """Exception raised when a note is not found in a charcters notes"""

class NotEnoughShardsError(Error):
    """Exception raised when trying to remove more shards than a character has"""

class AlreadyWorshippingError(Error):
    """Exception raised when trying to become an initiate of one god whilst currently worshipping another"""
