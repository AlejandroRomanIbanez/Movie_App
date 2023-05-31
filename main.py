import argparse
from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


def main():
    """
    Entry point of the Movie App program.
    Parses the command-line arguments to determine the movie data file,
    initializes the appropriate storage object based on the file extension,
    creates an instance of the MovieApp class with the storage object,
    and runs the main loop of the Movie App.
    """
    parser = argparse.ArgumentParser(description="Movie App")
    parser.add_argument('filename', help='Path to the movie data file(json or csv)')

    args = parser.parse_args()
    filename = args.filename

    if filename.endswith('.csv'):
        storage = StorageCsv(filename)
    elif filename.endswith('.json'):
        storage = StorageJson(filename)
    else:
        print("The argument is invalid, use .json or .csv example: john.json")
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
