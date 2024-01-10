"""Module providing weather-related functionality."""


class BaseDataClass(object):
    """Base class for weather data classes."""

    def __init__(self, **kwargs: object) -> None:
        """Initialize the BaseDataClass."""
        for key, value in kwargs.items():
            setattr(self, key, value)
