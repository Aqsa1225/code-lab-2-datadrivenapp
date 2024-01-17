import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io
from tkinter import Listbox

class MovieApp:
    def __init__(self, root):
        # Initialize the MovieApp class
        self.root = root
        self.root.title("Movie API App")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # API key and base URL for movie data
        self.api_key = "43bac13ee6250a0184e8f77ab0024010"
        self.base_url = "https://api.themoviedb.org/3/search/movie"

        # Configure root window background color
        self.root.configure(bg="#2E2E2E")

        # Load background image for the welcome page
        self.home_bg_image = Image.open("Yellow Entertaiment Youtube Banner (1).png")
        self.home_bg_image = self.home_bg_image.resize((800, 600))
        self.home_bg_photo = ImageTk.PhotoImage(self.home_bg_image)

        # Display the welcome page
        self.show_welcome_page()

        # Configure styles for the back button
        self.back_button_style = ttk.Style()
        self.back_button_style.configure("Back.TButton", padding=6, relief="flat", font=("Arial", 14))

    def show_welcome_page(self):
        # Display the welcome page with background image and menu button
        self.clear_widgets()

        bg_label = tk.Label(self.root, image=self.home_bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menu button for navigation
        self.toggle_button = tk.Menubutton(self.root, text="\u2630", font=("Arial", 24), bg="#2E2E2E", fg="white")
        self.toggle_button.menu = tk.Menu(self.toggle_button, tearoff=0, font=("Arial", 14), bg="#2E2E2E", fg="white")
        self.toggle_button["menu"] = self.toggle_button.menu
        self.toggle_button.menu.add_command(label="Home", command=self.show_welcome_page)
        self.toggle_button.menu.add_command(label="Movies", command=self.show_movies_page)
        self.toggle_button.menu.add_command(label="Popular Movies", command=self.show_popular_movies)
        self.toggle_button.menu.add_command(label="Upcoming Movies", command=self.show_upcoming_movies)
        self.toggle_button.menu.add_command(label="Details", command=self.show_details_page)

        # Position the menu button
        self.toggle_button.pack_forget()
        self.toggle_button.place(x=10, y=10)

        # Display welcome message
        welcome_label = tk.Label(self.root, text="Welcome to Movie API App", font=("Arial", 24, "bold"), bg="sky blue", fg="yellow")
        welcome_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        created_by_label = tk.Label(self.root, text="Created by Aqsa Riaz", font=("Arial", 19, "italic"), bg="sky blue", fg="yellow")
        created_by_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def show_movies_page(self):
        # Display the movies page with search bar and movie details
        self.clear_widgets()

        self.root.configure(bg="#334455")

        search_entry = tk.Entry(self.root, font=("Arial", 16), bg="white", fg="#2E2E2E")
        search_entry.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=("Arial", 14))
        search_button = ttk.Button(self.root, text="Search", command=lambda: self.search_movie(search_entry.get()),
                                   style="TButton", cursor="hand2")
        search_button.pack(pady=10)

        self.details_frame = tk.Frame(self.root, bg="#007ACC", bd=4, relief=tk.SOLID, width=400, height=300)
        self.details_frame.pack(side=tk.LEFT, padx=10, pady=20)
        self.details_frame.pack_propagate(0)

        self.poster_frame = tk.Frame(self.root, bg="#334455")
        self.poster_frame.pack(side=tk.LEFT, padx=10, pady=20)

    def show_details_page(self):
        # Display the details page with instructions
        self.clear_widgets()

        self.root.configure(bg="#334455")

        details_label = tk.Label(self.root, text="How to Use the App", font=("Arial", 25,"bold"), bg="#334455", fg="sky blue")
        details_label.pack(pady=20)

        instructions_label = tk.Label(self.root, text="Instructions:", font=("Arial", 25, "bold"), bg="#334455", fg="yellow")
        instructions_label.pack(pady=10)

        instructions_text = """
        1. Enter a movie name in the search bar.
        2. Click the 'Search' button.
        3. View the movie details on the left side.
        4. If available, the movie poster will be displayed on the right side.
        5. Explore 'Popular Movies' to discover trending films.
        6. Check out 'Upcoming Movies' to see what's coming soon to theaters.
        7. Use the 'Back to Menu' button to return to the main menu.
        """
        instructions_text_widget = tk.Text(self.root, wrap=tk.WORD, width=60, height=12, font=("Arial", 12), bg="white", fg="black")
        instructions_text_widget.insert(tk.END, instructions_text)
        instructions_text_widget.config(state=tk.DISABLED)
        instructions_text_widget.pack(pady=20)

        back_button = ttk.Button(self.root, text="Back to Menu", command=self.show_menu, style="Back.TButton")
        back_button.pack(pady=20)

    def show_popular_movies(self):
        # Display popular movies with a listbox
        self.clear_widgets()

        self.root.configure(bg="#334455")

        heading_label = tk.Label(self.root, text="Popular Movies", font=("Arial", 25, "bold"), bg="#334455", fg="yellow")
        heading_label.pack(pady=20)

        popular_movies_frame = tk.Frame(self.root, bg="#334455")
        popular_movies_frame.pack(pady=20)

        back_to_menu_button = ttk.Button(self.root, text="Back to Menu", command=self.show_menu, style="Back.TButton")
        back_to_menu_button.pack(pady=10)

        popular_movies_url = "https://api.themoviedb.org/3/movie/popular"
        params = {
            "api_key": self.api_key
        }

        try:
            response = requests.get(popular_movies_url, params=params)
            response.raise_for_status()
            popular_movies_data = response.json()

            listbox = Listbox(popular_movies_frame, selectbackground="sky blue", font=("Arial", 14), bg="#334455", fg="white", width=40, height=10)
            for movie in popular_movies_data.get("results", []):
                listbox.insert(tk.END, movie.get("title", "N/A"))

            listbox.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(popular_movies_frame, orient=tk.VERTICAL)
            scrollbar.config(command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox.config(yscrollcommand=scrollbar.set)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching popular movies data: {e}")

    def show_upcoming_movies(self):
        # Display upcoming movies with a listbox
        self.clear_widgets()

        self.root.configure(bg="#334455")
        heading_label = tk.Label(self.root, text="Upcoming Movies", font=("Arial", 25, "bold"), bg="#334455", fg="yellow")
        heading_label.pack(pady=20)

        upcoming_movies_frame = tk.Frame(self.root, bg="#334455")
        upcoming_movies_frame.pack(pady=20)

        back_to_menu_button = ttk.Button(self.root, text="Back to Menu", command=self.show_menu, style="Back.TButton")
        back_to_menu_button.pack(pady=10)

        upcoming_movies_url = "https://api.themoviedb.org/3/movie/upcoming"
        params = {
            "api_key": self.api_key
        }

        try:
            response = requests.get(upcoming_movies_url, params=params)
            response.raise_for_status()
            upcoming_movies_data = response.json()

            listbox = Listbox(upcoming_movies_frame, selectbackground="sky blue", font=("Arial", 14), bg="#334455", fg="white", width=40, height=10)
            for movie in upcoming_movies_data.get("results", []):
                listbox.insert(tk.END, movie.get("title", "N/A"))

            listbox.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(upcoming_movies_frame, orient=tk.VERTICAL)
            scrollbar.config(command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox.config(yscrollcommand=scrollbar.set)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching upcoming movies data: {e}")

    def search_movie(self, query):
        # Search for a movie using the provided query
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return

        params = {
            "api_key": self.api_key,
            "query": query
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            movie_data = response.json()
            if movie_data.get("results"):
                first_movie = movie_data["results"][0]

                self.display_movie_details(first_movie)
                self.display_movie_poster(first_movie)

            else:
                messagebox.showinfo("Information", "No results found.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching movie data: {e}")

    def display_movie_details(self, movie_data):
        # Display details of the selected movie
        title = movie_data.get("title", "N/A")
        overview = movie_data.get("overview", "No overview available.")
        release_date = movie_data.get("release_date", "N/A")
        language = movie_data.get("original_language", "N/A")
        rating = movie_data.get("vote_average", "N/A")
        movie_id = movie_data.get("id", "N/A")

        for widget in self.details_frame.winfo_children():
            widget.destroy()

        details_text = f"Title: {title}\nRelease Date: {release_date}\n"
        details_text += f"Language: {language}\nRating: {rating}\nMovie ID: {movie_id}\n"
        details_text += f"\nOverview: {overview}"

        details_text_widget = tk.Text(self.details_frame, wrap=tk.WORD, width=50, height=15,
                                      font=("Arial", 12), bg="#007ACC", fg="white")
        scrollbar = ttk.Scrollbar(self.details_frame, command=details_text_widget.yview)
        details_text_widget.config(yscrollcommand=scrollbar.set)

        details_text_widget.insert(tk.END, details_text)
        details_text_widget.config(state=tk.DISABLED)

        details_text_widget.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def display_movie_poster(self, movie_data):
        # Display the poster of the selected movie
        poster_path = movie_data.get("poster_path")

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            poster_image_data = requests.get(poster_url).content

            poster_image = Image.open(io.BytesIO(poster_image_data))
            poster_image = poster_image.resize((340, 300))

            photo_image = ImageTk.PhotoImage(poster_image)

            for widget in self.poster_frame.winfo_children():
                widget.destroy()

            poster_label = tk.Label(self.poster_frame, image=photo_image, text="", compound=tk.TOP, bg="#334455", bd=5, relief=tk.RAISED,
                                    highlightbackground="white", highlightcolor="white")
            poster_label.image = photo_image
            poster_label.pack(pady=10)
        else:
            messagebox.showinfo("Information", "No poster available.")

    def show_menu(self):
        # Display the navigation menu
        x = self.toggle_button.winfo_rootx()
        y = self.toggle_button.winfo_rooty() + self.toggle_button.winfo_height()

        self.toggle_button.menu.post(x, y)

    def clear_widgets(self):
        # Clear all widgets from the root window except the menu button
        for widget in self.root.winfo_children():
            if widget != self.toggle_button:
                widget.destroy()

if __name__ == "__main__":
    # Create and run the MovieApp instance
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
