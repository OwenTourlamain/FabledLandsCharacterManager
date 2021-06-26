class Error(Exception):
    """Base class for exceptions in this module"""

class InventoryFullError(Error):
    """Exception raised when a characters inventory is full"""
