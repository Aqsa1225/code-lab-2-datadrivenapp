# Imported libraries
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io
from tkinter import Listbox

class MoviesApp:
    def clear_widgets(gui):
        # Clear all widgets from the root window except the menu button
        for widget in gui.root.winfo_children():
            if widget != gui.menu_button:
                widget.destroy()

    def __init__(gui, root):
        gui.root = root
        gui.root.title("Movies Application") # Title of the API
        gui.root.geometry("800x600")# Set the  size of the Tkinter window size to 800x600 
        gui.root.resizable(False, False)# Make the Tkinter window non-resizable in both width and height

        # url of api key and MovieDatabase
        gui.api_key = "43bac13ee6250a0184e8f77ab0024010"
        gui.base_url = "https://api.themoviedb.org/3/search/movie"

        # Configure root window background color
        gui.root.configure(bg="#2E2E2E")

        # Load background image for the welcome page
        gui.mainpage_bg_image = Image.open("Yellow Entertaiment Youtube Banner (1).png")
        gui.mainpage_bg_image = gui.mainpage_bg_image.resize((800, 600))
        gui.mainpage_bg_photo = ImageTk.PhotoImage(gui.mainpage_bg_image)

        # Display the welcome page
        gui.show_welcome_page()

        # Configure styles for the back button
        gui.back_button_style = ttk.Style()
        gui.back_button_style.configure("Back.TButton", padding=6, relief="flat", font=("Arial", 14))

    def show_welcome_page(gui):
        # Display the welcome page with background image and menu button
        gui.clear_widgets()

        bg_label = tk.Label(gui.root, image=gui.mainpage_bg_photo)  
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menu button for navigation
        gui.menu_button = tk.Menubutton(gui.root, text="\u2630", font=("Arial", 24), bg="#2E2E2E", fg="white")
        gui.menu_button.menu = tk.Menu(gui.menu_button, tearoff=0, font=("Arial", 14), bg="#2E2E2E", fg="white")
        gui.menu_button["menu"] = gui.menu_button.menu
        gui.menu_button.menu.add_command(label="Home", command=gui.show_welcome_page)
        gui.menu_button.menu.add_command(label="Movies", command=gui.show_movies_page)
        gui.menu_button.menu.add_command(label="Popular Movies", command=gui.show_popular_movies)
        gui.menu_button.menu.add_command(label="Upcoming Movies", command=gui.show_upcoming_movies)
        gui.menu_button.menu.add_command(label="Details", command=gui.show_details_page)

        # Position the menu button
        gui.menu_button.pack_forget()
        gui.menu_button.place(x=10, y=10)

        # Display greeting message 
        greeting_message = tk.Label(gui.root, text="Welcome to Movie API App", font=("Arial", 24, "bold"), bg="sky blue", fg="yellow")
        greeting_message.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        created_by = tk.Label(gui.root, text="Created by Aqsa Riaz", font=("Arial", 19, "italic"), bg="sky blue", fg="yellow")
        created_by.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def show_movies_page(gui):
        # Display the movies page with search bar and movie details
        gui.clear_widgets()

        gui.root.configure(bg="#334455")

        search_entry = tk.Entry(gui.root, font=("Arial", 16), bg="white", fg="#2E2E2E")
        search_entry.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=("Arial", 14))
        search_button = ttk.Button(gui.root, text="Search", command=lambda: gui.search_movie(search_entry.get()),
                                   style="TButton", cursor="hand2")
        search_button.pack(pady=10)

        gui.info_frame = tk.Frame(gui.root, bg="#007ACC", bd=4, relief=tk.SOLID, width=400, height=300)
        gui.info_frame.pack(side=tk.LEFT, padx=10, pady=20)
        gui.info_frame.pack_propagate(0)

        gui.image_frame = tk.Frame(gui.root, bg="#334455")
        gui.image_frame.pack(side=tk.LEFT, padx=10, pady=20)

    def show_details_page(gui):
        # Display the details page with instructions
        gui.clear_widgets()

        gui.root.configure(bg="#334455")

        details_label = tk.Label(gui.root, text="How to Use the App", font=("Arial", 25, "bold"), bg="#334455", fg="sky blue")
        details_label.pack(pady=20)

        instructions_label = tk.Label(gui.root, text="Instructions:", font=("Arial", 25, "bold"), bg="#334455", fg="yellow")
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
        instructions_text_widget = tk.Text(gui.root, wrap=tk.WORD, width=60, height=12, font=("Arial", 12), bg="white", fg="black")
        instructions_text_widget.insert(tk.END, instructions_text)
        instructions_text_widget.config(state=tk.DISABLED)
        instructions_text_widget.pack(pady=20)

        back_button = ttk.Button(gui.root, text="Back to Menu", command=gui.show_menu, style="Back.TButton")
        back_button.pack(pady=20)

    def show_popular_movies(gui):
        # Display popular movies in a frame
        gui.clear_widgets()

        gui.root.configure(bg="#334455")

        heading_label = tk.Label(gui.root, text="Popular Movies", font=("Arial", 25, "bold"), bg="#334455", fg="yellow")
        heading_label.pack(pady=20)

        popular_movies_frame = tk.Frame(gui.root, bg="#334455")
        popular_movies_frame.pack(pady=20)

        back_button = ttk.Button(gui.root, text="Back", command=gui.show_menu, style="Back.TButton")
        back_button.pack(pady=10)

        popular_movies_url = "https://api.themoviedb.org/3/movie/popular"
        params = {
            "api_key": gui.api_key
        }

        try:
            response = requests.get(popular_movies_url, params=params)
            response.raise_for_status()
            popular_movies_data = response.json()

            moviesbox = Listbox(popular_movies_frame, selectbackground="sky blue", font=("Arial", 14), bg="#334455", fg="white", width=40, height=10)
            for movie in popular_movies_data.get("results", []):
                moviesbox.insert(tk.END, movie.get("title", "N/A"))

            moviesbox.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(popular_movies_frame, orient=tk.VERTICAL)
            scrollbar.config(command=moviesbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            moviesbox.config(yscrollcommand=scrollbar.set)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching popular movies data: {e}")

    def show_upcoming_movies(gui):
        # Display upcoming movies with a listbox
        gui.clear_widgets()

        gui.root.configure(bg="#334455")
        heading_label = tk.Label(gui.root, text="Upcoming Movies", font=("Arial", 25, "bold"), bg="#334455", fg="yellow")
        heading_label.pack(pady=20)

        upcoming_movies_frame = tk.Frame(gui.root, bg="#334455")
        upcoming_movies_frame.pack(pady=20)

        back_button = ttk.Button(gui.root, text="Back", command=gui.show_menu, style="Back.TButton")
        back_button.pack(pady=10)

        upcoming_movies_url = "https://api.themoviedb.org/3/movie/upcoming"
        params = {
            "api_key": gui.api_key
        }

        try:
            response = requests.get(upcoming_movies_url, params=params)
            response.raise_for_status()
            upcoming_movies_data = response.json()

            moviesbox = Listbox(upcoming_movies_frame, selectbackground="sky blue", font=("Arial", 14), bg="#334455", fg="white", width=40, height=10)
            for movie in upcoming_movies_data.get("results", []):
                moviesbox.insert(tk.END, movie.get("title", "N/A"))

            moviesbox.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(upcoming_movies_frame, orient=tk.VERTICAL)
            scrollbar.config(command=moviesbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            moviesbox.config(yscrollcommand=scrollbar.set)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching upcoming movies data: {e}")

    def search_movie(gui, query):
        # Search for a movie using the provided query
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return

        request_parameters = {
            "api_key": gui.api_key,
            "query": query
        }

        try:
            response = requests.get(gui.base_url, params=request_parameters)
            response.raise_for_status()
            movie_data = response.json()
            if movie_data.get("results"):
                first_movie = movie_data["results"][0]

                gui.display_movie_details(first_movie)
                gui.display_movie_poster(first_movie)

            else:
                messagebox.showinfo("Information", "No results found.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching movie data: {e}")

    def display_movie_details(gui, movie_data):
        # Display details of the selected movie
        movie_title = movie_data.get("title", "N/A")
        movie_overview = movie_data.get("overview", "No overview available.")
        release_date = movie_data.get("release_date", "N/A")
        original_language = movie_data.get("original_language", "N/A")
        vote_average = movie_data.get("vote_average", "N/A")
        movie_id = movie_data.get("id", "N/A")

        for widget in gui.info_frame.winfo_children():
            widget.destroy()

        details_text = f"Title: {movie_title}\nRelease Date: {release_date}\n"
        details_text += f"Language: {original_language}\nRating: {vote_average}\nMovie ID: {movie_id}\n"
        details_text += f"\nOverview: {movie_overview}"

        details_text_widget = tk.Text(gui.info_frame, wrap=tk.WORD, width=50, height=15,
                                      font=("Arial", 12), bg="#007ACC", fg="white")
        scrollbar = ttk.Scrollbar(gui.info_frame, command=details_text_widget.yview)
        details_text_widget.config(yscrollcommand=scrollbar.set)

        details_text_widget.insert(tk.END, details_text)
        details_text_widget.config(state=tk.DISABLED)

        details_text_widget.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def display_movie_poster(gui, movie_data):
        # Display the poster of the selected movie
        poster_path = movie_data.get("poster_path")

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            poster_image_data = requests.get(poster_url).content

            poster_image = Image.open(io.BytesIO(poster_image_data))
            poster_image = poster_image.resize((340, 300))

            photo_image = ImageTk.PhotoImage(poster_image)

            for widget in gui.image_frame.winfo_children():
                widget.destroy()

            poster_label = tk.Label(gui.image_frame, image=photo_image, text="", compound=tk.TOP, bg="#334455", bd=5, relief=tk.RAISED,
                                    highlightbackground="white", highlightcolor="white")
            poster_label.image = photo_image
            poster_label.pack(pady=10)
        else:
            messagebox.showinfo("Information", "No poster available.")

    def show_menu(gui):
        # Display the navigation menu
        x = gui.menu_button.winfo_rootx()
        y = gui.menu_button.winfo_rooty() + gui.menu_button.winfo_height()

        gui.menu_button.menu.post(x, y)

if __name__ == "__main__":
    # Create and run the MovieApp 
    root = tk.Tk()
    app = MoviesApp(root)
    root.mainloop()
