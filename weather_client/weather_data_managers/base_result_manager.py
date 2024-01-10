from weather_client.exceptions import WeatherAPIDataManagerError
from weather_client.weather_data_classes import BaseDataClass


class BaseDataManager(object):
    """Manages weather results."""
    data_class = BaseDataClass
    objects_storage: list = []

    def __init__(self, filter_field: str) -> None:
        """Initialize the BaseDataManager."""
        self.filter_field = filter_field

    def _save_or_update_object(self, obj: data_class) -> data_class:
        """
        Save or update the object.

        Args:
            obj (data_class): The object to save or update.

        Returns:
            data_class: The saved or updated object.
        """
        if not isinstance(obj, self.data_class):
            raise TypeError('Invalid result type. Expected: {}, got: {}'.format(self.data_class, type(obj)))

        filter_field = self.filter_field
        filter_value = getattr(obj, self.filter_field)
        if not isinstance(filter_value, str):
            raise TypeError('Invalid filter value type. Expected: str, got: {}'.format(type(filter_value)))

        for existing_obj in self.objects_storage:
            if getattr(existing_obj, filter_field).lower() == filter_value.lower():
                for field in vars(self.data_class):
                    setattr(existing_obj, field, getattr(obj, field))
                return existing_obj
        self.objects_storage.append(obj)
        return obj

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
            raise TypeError('Invalid filter value type. Expected: str, got: {}'.format(type(filter_value)))
        if not filter_value:
            objects_count = self.count()
            self.objects_storage = []
            return objects_count

        objects_to_delete_indices = [index for index, obj in enumerate(self.objects_storage) if
                                     getattr(obj, filter_field).lower() == filter_value.lower()]

        for index in sorted(objects_to_delete_indices, reverse=True):
            del self.objects_storage[index]

        return len(objects_to_delete_indices)

    def _get_object(self, filter_value: str) -> data_class:
        """
        Get an object.

        Args:
            filter_value (str): The filter value.

        Returns:
            data_class: The object.
        """
        if not isinstance(filter_value, str):
            raise WeatherAPIDataManagerError(
                'Invalid filter value type. Expected: str, got: {}'.format(type(filter_value)),
            )
        for obj in self.objects_storage:
            if getattr(obj, self.filter_field).lower() == filter_value.lower():
                return obj

    def save(self, obj: data_class) -> data_class | None:
        """
        Save a result.

        Args:
            obj: The result to save.

        Returns:
            The saved result.
        """
        if not obj:
            return None
        try:
            saved_obj = self._save_or_update_object(obj)
        except TypeError as e:
            raise WeatherAPIDataManagerError(str(e))
        return saved_obj

    def count(self) -> int:
        """
        Get the count of stored weather results.

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
