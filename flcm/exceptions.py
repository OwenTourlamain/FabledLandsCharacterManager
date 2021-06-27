class Error(Exception):
    """Base class for exceptions in this module"""

class InventoryFullError(Error):
    """Exception raised when a characters inventory is full"""

class ItemNotFoundError(Error):
    """Exception raised when an item is not found in a charcters inventory"""
