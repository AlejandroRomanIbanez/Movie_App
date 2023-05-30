import json
import requests
from helpers import input_color, user_choice_color, error_color, return_to_menu
from istorage import IStorage


class StorageJson(IStorage):
    """
    JSON storage implementation for storing movie data.
    """
    def __init__(self, file_path):
        """
        Initialize the StorageJson instance.

        Args:
            file_path (str): The path to the JSON file.
        """
        self.file_path = file_path
        try:
            with open(self.file_path, "r") as handle:
                pass
        except FileNotFoundError:
            with open(self.file_path, "w") as handle:
                json.dump({}, handle)

    def list_movies(self):
        """
        Retrieve the list of movies from the JSON file.
        Returns:
        dict: The dictionary of movies.
        """
        with open(self.file_path, "r") as handle:
            movies_str = handle.read()
            movies = json.loads(movies_str)
        return movies

    def add_movie(self):
        """
        Adds a new movie to the movie dictionary.
        """
        api_key = "eaf9a303"
        request_url = f"http://www.omdbapi.com/?apikey={api_key}&t="
        movie_response = requests.get(request_url)
        new_movie = input(input_color("Enter the name of the movie: ")).title()
        response = requests.post(request_url + new_movie)
        if movie_response.status_code == 200:
            movie_info = response.json()
            if movie_info['Response'] == 'False':
                print(error_color("This movie doesn't exist, make sure you write it correctly."))
                return_to_menu()
            else:
                title = movie_info['Title']
                year = int(movie_info['Year'])
                rating = float(movie_info['imdbRating'])
                poster = movie_info['Poster']
                imdb_id = movie_info['imdbID']
                country = movie_info['Country']
                with open(self.file_path, "r") as handle:
                    movies_str = handle.read()
                    movies = json.loads(movies_str)
                country_list = country.split(", ")
                if "United States" in country_list:
                    country_list.remove("United States")
                    country_list.insert(0, "United States")
                movies[title] = {"rating": rating, "year": year, "poster": poster,
                                 "id": imdb_id, "country": ", ".join(country_list)}
                with open(self.file_path, "w") as handle:
                    json.dump(movies, handle, indent=4)
                print(f"Movie {user_choice_color(new_movie)} successfully added")
                return_to_menu()
        else:
            print(error_color(f"Error {response.status_code}: Could not retrieve movie information."))
            return_to_menu()

    def delete_movie(self):
        """
        Deletes a movie from the movie dictionary.
        """
        delete_movie_choice = input(
            input_color("Enter the name of the movie you want to delete: "))
        with open(self.file_path, "r") as handle:
            movies = json.load(handle)

            if delete_movie_choice in movies:
                del movies[delete_movie_choice]

                with open(self.file_path, "w") as handle:
                    json.dump(movies, handle, indent=4)

                print(f"{user_choice_color(delete_movie_choice)} has been deleted.")
                return_to_menu()
            else:
              print(user_choice_color(delete_movie_choice) + error_color(" is not in the movie list."))
              return_to_menu()

    def update_movie(self):
        """
        Updates the comment for a movie in the movie dictionary.
        """
        with open(self.file_path, "r") as handle:
            movies = json.load(handle)
        update_movie = input(
        input_color("Enter the name of the movie you want to add a comment: ")
        ).title()
        if update_movie in movies:
            update_comment = input(input_color("Enter the comment you want: "))
            movies[update_movie]['comment'] = update_comment
            with open(self.file_path, "w") as handle:
                json.dump(movies, handle, indent=4)
            return_to_menu()
        else:
            print(error_color("That movie is not in the list, look again in the list and try again"))
            return_to_menu()

    def get_country_id_flag(self, movie_title):
        """
        Get the country ID flag for a movie.
        Args:
        movie_title (str): The title of the movie.
        Returns:
        str: The country ID flag.
        """
        with open(self.file_path, "r") as handle:
            movies_str = handle.read()
            movies = json.loads(movies_str)

        movie_country = movies[movie_title]['country']
        with open("countries.json", "r") as handle:
            countries_str = handle.read()
            countries = json.loads(countries_str)

        countries_list = movie_country.split(',')
        first_country = countries_list[0].strip()

        for country_id, country_data in countries.items():
            if country_data == first_country:
                return country_id
