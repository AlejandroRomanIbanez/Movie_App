from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


def main():
    """
    Entry point of the movie app program.
    This function creates an instance of the `StorageJson` class to handle movie storage,
    and an instance of the `MovieApp` class to interact with the user and manage the movie app.
    It then calls the `run()` method on the `MovieApp` instance to start the movie app program.
    The movie storage is based on a JSON file specified by the file path.
    Usage:
    The `main()` function is typically called when executing the movie app script directly.
    It serves as the starting point of the movie app program.
    """
    storage = StorageCsv('movies_Alex2.csv')
    storage2 = StorageJson('movies_Alex.json')
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
  main()
