import csv
import json
import os
import requests
from helpers import input_color, user_choice_color, error_color, return_to_menu
from istorage import IStorage

class StorageCsv(IStorage):
    """
    CSV storage implementation for storing movie data.
    """
    def __init__(self, file_path):
        """
        Initialize the StorageCsv instance.
        Args:
        file_path (str): The path to the CSV file.
        """
        self.file_path = file_path
        try:
            with open(self.file_path, "r") as handle:
                pass
        except FileNotFoundError:
            with open(self.file_path, "w") as handle:
                writer = csv.writer(handle)
                writer.writerow(["title", "year", "rating", "id", "country", "comment", "poster"])
    
    def list_movies(self):
        """
        Retrieve the list of movies from the CSV file.
        Returns:
        list: The list of movies.
        """
        movies = {}
        with open(self.file_path, "r") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                row["rating"] = float(row["rating"])
                movie_title = row['title']
                movies[movie_title] = row
        return movies

    def add_movie(self):
        """
        Adds a new movie to the CSV file.
        """
        api_key = "eaf9a303"
        request_url = f"http://www.omdbapi.com/?apikey={api_key}&t="
        new_movie = input(input_color("Enter the name of the movie: ")).title()
        response = requests.get(request_url + new_movie)
        if response.status_code == 200:
            movie_info = response.json()
            if movie_info['Response'] == 'False':
                print(error_color("This movie doesn't exist, make sure you write it correctly."))
                return_to_menu()
            else:
                title = movie_info['Title']
                rating = float(movie_info['imdbRating'])
                year = int(movie_info['Year'])
                imdb_id = movie_info['imdbID']
                country = movie_info['Country']
                poster = movie_info['Poster']
                
                country_list = country.split(", ")
                if "United States" in country_list:
                    country_list.remove("United States")
                    country_list.insert(0, "United States")
                modified_country = ", ".join(country_list)
                with open(self.file_path, "r", newline='') as handle:
                    reader = csv.reader(handle)
                    for row in reader:
                        if row[:5] == [title, int(year), float(rating), imdb_id, modified_country]:
                            print(error_color("This movie already exists in the list."))
                            return return_to_menu()
                with open(self.file_path, "a", newline='') as handle:
                    writer = csv.writer(handle)
                    writer.writerow([title, rating, year, imdb_id, modified_country, "", poster])

                print(f"Movie {user_choice_color(new_movie)} successfully added")
                return_to_menu()
        else:
            print(error_color(f"Error {response.status_code}: Could not retrieve movie information."))
            return_to_menu()

    def delete_movie(self):
            """
            Deletes a movie from the CSV file.
            """
            delete_movie_choice = input(
                input_color("Enter the name of the movie you want to delete: "))

            temp_file_path = self.file_path + ".tmp"
            fieldnames = ['title', 'rating', 'year', 'id', 'country', 'comment', 'poster']

            with open(self.file_path, "r") as handle, open(temp_file_path, "w", newline="") as temp_handle:
                reader = csv.DictReader(handle)
                writer = csv.DictWriter(temp_handle, fieldnames=fieldnames)

                writer.writeheader()
                for row in reader:
                    movie_title = row['title']
                    if movie_title != delete_movie_choice:
                        writer.writerow(row)

            os.remove(self.file_path)
            os.rename(temp_file_path, self.file_path)

            print(f"{user_choice_color(delete_movie_choice)} has been deleted.")
            return_to_menu()

    def update_movie(self):
            """
            Update a movie in the CSV file.
            """
            update_movie_choice = input(input_color("Enter the name of the movie to update: ")).title()
            update_comment = input(input_color("Enter the updated comment: "))

            updated = False
            movies = []
            with open(self.file_path, "r") as handle:
                reader = csv.DictReader(handle)
                for row in reader:
                    movies.append(row)

            for movie in movies:
                if movie["title"] == update_movie_choice:
                    movie["comment"] = update_comment
                    updated = True
                    break

            if updated:
                with open(self.file_path, "w", newline='') as handle:
                    fieldnames = ["title", "year", "rating", "id", "country", "comment", "poster"]
                    writer = csv.DictWriter(handle, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(movies)

                print(f"Movie {user_choice_color(update_movie_choice)} successfully updated")
            else:
                print(error_color(f"Movie {update_movie_choice} not found in the list"))

            return_to_menu()

    def get_country_id_flag(self, movie_title):
        """
        Get the country ID flag for a movie.
        Args:
        movie_title (str): The title of the movie.
        Returns:
        str: The country ID flag.
        """
        with open(self.file_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if row["title"] == movie_title:
                        country = row["country"]
                        with open("countries.json", "r") as countries_file:
                            countries_data = json.load(countries_file)
                            country_dict = {val: key for key, val in countries_data.items()}
                            if country in country_dict:
                                return country_dict[country]