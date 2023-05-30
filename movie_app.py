from statistics import median
import random
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt
from helpers import input_color, user_choice_color, error_color, return_to_menu, YELLOW, RESET_COLOR


class MovieApp:
    """
    A class representing a Movie App.
    """
    def __init__(self, storage):
        """
        Initializes a MovieApp instance with the given storage object.
        Parameters:
        - storage (IStorage): An object implementing the IStorage interface for movie storage.
        """
        self._storage = storage
        self.movies = self._storage.list_movies()

    def _command_list_movies(self):
        """
        Lists all movies with their ratings and years.
        Returns:
        str: A formatted string with the total number of movies and
        the list of movies with their ratings and years.
        """
        total_movies = f"{len(self.movies)} movies in total\n"
        movies_with_ranking = ""
        for key, val in self.movies.items():
            movies_with_ranking += f"{key}: {val['rating']}, {val['year']}\n"
        return total_movies + movies_with_ranking

    def _command_add_movie(self):
        """
        Prompts the user to add a new movie to the movie database.
        """
        self._storage.add_movie()
        self.movies = self._storage.list_movies()

    def _command_delete_movie(self):
        """
        Prompts the user to delete a movie from the movie database.
        """
        self._storage.delete_movie()
        self.movies = self._storage.list_movies()

    def _command_update_movie(self):
        """
        Prompts the user to update the comment for a movie in the movie database.
        """
        self._storage.update_movie()
        self.movies = self._storage.list_movies()

    def _average(self):
        """
        Calculates the average rating of all movies.
        Returns:
        float: The average rating of all movies.
        """
        sum_rating = 0
        for val in self.movies.values():
            sum_rating += val['rating']
        average_rating = sum_rating / len(self.movies)
        return round(average_rating, 1)

    def _command_movie_stats(self):
        """
        Displays various statistics about the movies in the database.
        """
        ratings = [movie['rating'] for movie in self.movies.values()]
        print(f"Average rating: {self._average()}")
        print(f"Median rating: {median(ratings):.1f}")
        best_movie = max(self.movies, key=lambda movie: self.movies[movie]['rating'])
        worst_movie = min(self.movies, key=lambda movie: self.movies[movie]['rating'])
        print(f"Best movie: {best_movie}, {self.movies[best_movie]['rating']}")
        print(f"Worst movie: {worst_movie}, {self.movies[worst_movie]['rating']}")
        return_to_menu()

    def _command_random_movie(self):
        """
        Picks a random movie from the database and displays its details.
        """
        random_movie = random.choice(list(self.movies.keys()))
        print(f"Your movie for tonight: {random_movie}, " \
              f"it's rated {self.movies[random_movie]['rating']}")
        return_to_menu()

    def find_matching_movies(self, movie):
        """
        Finds movies in the database that match the given search query.
        Parameters:
        - movie (str): The search query.
        Returns:
        list: A list of matching movies with their ratings.
        """
        matching_movies = []
        for title, val in self.movies.items():
            if movie in title.lower():
                matching_movies.append(f"{title}, {val['rating']}")
        return matching_movies

    def find_possible_matches(self, movie):
        """
        Finds possible movie titles that closely match the given search query.
        Parameters:
        - movie (str): The search query.
        Returns:
        list: A list of possible movie titles.
        """
        possible_matches = []
        for title in self.movies:
            ratio = fuzz.ratio(movie, title.lower())
            if ratio > 50:
                possible_matches.append(title)
        return possible_matches

    def print_possible_matches(self, movie, possible_matches):
        """
        Prints the possible movie matches for a given query.
        Parameters:
        - movie (str): The search query.
        - possible_matches (list): A list of possible movie titles.
        """
        print(f'The movie "{user_choice_color(movie.title())}" does not exist. Did you mean:')
        for title in possible_matches:
            print(title)

    def _command_search_movie(self):
        """
        Searches for movies based on a partial movie name.
        """
        movie_search = input(input_color("Enter part of movie name: ")).lower()
        matching_movies = self.find_matching_movies(movie_search)
        if matching_movies:
            for movie in matching_movies:
                print(movie)
        else:
            possible_matches = self.find_possible_matches(movie_search)
            if possible_matches:
                self.print_possible_matches(movie_search, possible_matches)
            else:
                print(error_color("No movies matched your search"))

    def _command_sorted_movies(self):
        """
        Lists movies in descending order of their ratings.
        """
        sorted_movies = dict(sorted(self.movies.items(),
                                    key=lambda item: item[1]['rating'], reverse=True))
        for key, val in sorted_movies.items():
            print(f"{key}: {val['rating']}")
        return_to_menu()

    def get_movie_data(self):
        """
        Retrieves movie data and generates an HTML representation.
        Returns:
        str: A string containing HTML representation of movie data.
        """
        url_imdb = "https://www.imdb.com/title/"
        url_country_flag = "https://flagcdn.com/60x45/"
        movie_data_str = ""
        for key, val in self.movies.items():
            if isinstance(val, dict) and 'comment' in val:
                movie_data_str += f"""
            <li>
                <div class="movie">
                  <a href="{url_imdb}{val['id']}/">
                    <img class="movie-poster"
                        src="{val['poster']}"
                        title="{val['comment']}"/>
                  </a>
                    <div class="movie-title">{key}<img class= "movie-flag" src="{url_country_flag + self._storage.get_country_id_flag(key) + '.png'}" alt="{key}"></div>
                    <div class="movie-year">{val['year']}</div>
                    <div class="movie-title">{val['rating']}</div>
                </div>
            </li>"""
            else:
                movie_data_str += f"""
            <li>
                <div class="movie">
                  <a href="{url_imdb}{val['id']}/">
                    <img class="movie-poster"
                        src="{val['poster']}""
                        title=""/>
                  </a>
                    <div class="movie-title">{key}<img class= "movie-flag" src="{url_country_flag + self._storage.get_country_id_flag(key) + '.png'}" alt="{key}"></div>
                    <div class="movie-year">{val['year']}</div>
                    <div class="movie-title">{val['rating']}</div>
                </div>
            </li>"""
        return movie_data_str

    def _generate_website(self, movies_data):
        """
        Generates an HTML website with the given movie data.
        Parameters:
        - movies_data (str): The movie data in HTML format.
        """
        with open("_static/index_template.html", "r") as html_file:
            data = html_file.read()
            new_data = data.replace("__TEMPLATE_MOVIE_GRID__", movies_data)
        with open("_static/index.html", "w") as updated_html_file:
            updated_html_file.write(new_data)
        print("Website was generated successfully.")
        return_to_menu()

    def _command_ratings_histogram(self):
        """
        Displays a histogram of movie ratings and saves it to a file.
        """
        ratings = [movie['rating'] for movie in self.movies.values()]
        plt.hist(ratings, bins=10)
        print("Checking histogram...")
        plt.title("Movie Ratings Histogram")
        plt.xlabel("Rating")
        plt.ylabel("Frequency")
        plt.show()
        save_file = input(input_color
                    ("How would you like to name the file where the histogram will be saved?"))
        plt.savefig(save_file)
        return_to_menu()

    def run(self):
        """
        Runs the main loop of the Movie App, allowing users to interact with the program.
        """
        while True:
            print(YELLOW + """********** My Movies Database **********
      Menu:
      0. Exit
      1. List movies
      2. Add movie
      3. Delete movie
      4. Update movie
      5. Stats
      6. Random movie
      7. Search movie
      8. Movies sorted by rating
      9. Generate website
      10. Create a Histogram of Rates
      """ + RESET_COLOR)

            choice_menu = input(input_color("Enter choice (0-10): "))
            if int(choice_menu) < 0 or int(choice_menu) > 10:
                print(error_color("Invalid Choice"))
            elif choice_menu == "1":
                print(self._command_list_movies())
                return_to_menu()
            elif choice_menu == "2":
                self._command_add_movie()
            elif choice_menu == "3":
                self._command_delete_movie()
            elif choice_menu == "4":
                self._command_update_movie()
            elif choice_menu == "5":
                self._command_movie_stats()
            elif choice_menu == "6":
                self._command_random_movie()
            elif choice_menu == "7":
                self._command_search_movie()
                return_to_menu()
            elif choice_menu == "8":
                self._command_sorted_movies()
            elif choice_menu == "9":
                movie_info = self.get_movie_data()
                self._generate_website(movie_info)
            elif choice_menu == "10":
                self._command_ratings_histogram()
            elif choice_menu == "0":
                print("Bye!")
                break
