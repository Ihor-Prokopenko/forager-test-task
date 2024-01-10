"""Module providing weather-related functionality."""
from typing import Generic, Type, TypeVar

from weather_client.exceptions import WeatherAPIDataManagerError
from weather_client.weather_data_classes import BaseDataClass

T = TypeVar('T', bound=BaseDataClass)


class BaseDataManager(Generic[T]):
    """Manages weather API results."""

    data_class: Type[T]
    objects_storage: list = []

    def __init__(self, filter_field: str) -> None:
        """Initialize the BaseDataManager."""
        self.filter_field = filter_field

    def _save_or_update_object(self, data_obj: T) -> T:
        """
        Save or update the object.

        Args:
            data_obj (T): The object to save or update.

        Returns:
            T: The saved or updated object.
        """
        if not isinstance(data_obj, self.data_class):
            raise TypeError('Invalid result type. Expected:{0}, got:{1}'.format(self.data_class, type(data_obj)))

        filter_field = self.filter_field
        filter_value = getattr(data_obj, self.filter_field)
        if not isinstance(filter_value, str):
            raise TypeError('Invalid filter value type. Expected: str, got: {0}'.format(type(filter_value)))

        for existing_obj in self.objects_storage:
            if getattr(existing_obj, filter_field).lower() == filter_value.lower():
                for field in self.data_class.__dict__:
                    setattr(existing_obj, field, getattr(data_obj, field))
                return existing_obj
        self.objects_storage.append(data_obj)
        return data_obj

    def _delete_stored_objects(self, filter_value: str = '') -> int:
        """
        Delete stored objects.

        Args:
            filter_value (str): The filter value.

        Returns:
            int: The number of deleted objects.
        """
        filter_field = self.filter_field

        if not isinstance(filter_value, str):
            raise TypeError('Invalid filter value type. Expected: str, got: {0}'.format(type(filter_value)))
        if not filter_value:
            objects_count = self.count()
            self.objects_storage = []
            return objects_count

        objects_to_delete_indices = [
            index for index, data_obj in enumerate(self.objects_storage) if
            getattr(data_obj, filter_field).lower() == filter_value.lower()
        ]

        for index in sorted(objects_to_delete_indices, reverse=True):
            del self.objects_storage[index]

        return len(objects_to_delete_indices)

    def _get_object(self, filter_value: str) -> T | None:
        """
        Get an object.

        Args:
            filter_value (str): The filter value.

        Returns:
            data_class: The object.
        """
        if not isinstance(filter_value, str):
            raise WeatherAPIDataManagerError(
                'Invalid filter value type. Expected: str, got: {0}'.format(type(filter_value)),
            )
        for data_obj in self.objects_storage:
            if getattr(data_obj, self.filter_field).lower() == filter_value.lower():
                return data_obj
        return None

    def save(self, data_obj: T) -> T | None:
        """
        Save a result.

        Args:
            data_obj: The result to save.

        Returns:
            The saved result.
        """
        if not data_obj:
            return None
        try:
            saved_obj = self._save_or_update_object(data_obj)
        except TypeError as error:
            raise WeatherAPIDataManagerError(str(error))
        return saved_obj

    def count(self) -> int:
        """
        Get the count of stored data objects results.

        Returns:
            int: The count of stored weather results.
        """
        return len(self.objects_storage)

    def get_as_str(self) -> str:
        """
        Get the stored object as a string.

        Returns:
            str: The stored objects as a string.
        """
        return '\n'.join([str(weather_obj) for weather_obj in self.objects_storage])
