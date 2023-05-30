from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Abstract base class for movie storage.
    """

    @abstractmethod
    def list_movies(self):
        """
        Abstract method to retrieve the list of movies.
        """
        pass

    @abstractmethod
    def add_movie(self):
        """
        Abstract method to add a new movie.
        """
        pass

    @abstractmethod
    def delete_movie(self):
        """
        Abstract method to delete a movie.
        """
        pass

    @abstractmethod
    def update_movie(self):
        """
        Abstract method to update a movie.
        """
        pass
