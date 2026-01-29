'''
Greenfield Community Library Book Management System

System Developer: Hamza Bawah Ibrahim
'''
# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------
from datetime import datetime
import os

# ---------------------------------------------------------
# Global variables
# ---------------------------------------------------------
FILENAME = "library_books.txt" # File name to save and load data
books = [] # This list will store all the books 
CURRENT_YEAR = datetime.now().year # Used to validate years (ensures user cannot enter unrealistic year)

# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------
# checking if year is number and 4-digit number between 1000 and current year
def is_valid_year(year_string):
    '''Return true if year_str is a 4-digit number between 1000 and current year'''
    # rejecting blank or non-numeric input
    if not year_string.isdigit() or len(year_string) != 4:
        return False
    # converting year to integer safely
    year_value = int(year_string.strip()) #.strip() removes any spaces at the beginning and end of the text the user typed.
    
    # validate year range
    return 1000 <= year_value <=CURRENT_YEAR

#checking if the user enter '0' to return to the main program 
def get_input(prompt):
    ''' Prompts the user for input and check 
    if user enter "0" the operationis is cancelled and the function
    returns None so that the calling function can safely stop
    '''
    value = input(prompt).strip()

    # Check if the user wants to cancel
    if value == "0":
        print("\n Operation cancelled. Returning to main menu...\n")
        return None # Signal cancellation to the caller
    return value # Return the valid input

# ---------------------------------------------------------
# Core feature functions
# ---------------------------------------------------------
# Add Book function
def add_book():
    print("\n ========= Add a New Book =========")
    print("(Enter 0 at any prompt to cancel and return to the main menu.)")
    
    title = get_input("Enter title: ")
    if title is None:
        return  # User chose to cancel
    author = get_input("Enter author: ")
    if author is None:
        return  # User chose to cancel
    year = get_input("Enter Publication year (YYYY): ")
    if year is None:
        return  # User chose to cancel
    genre = get_input("Enter genre: ")
    if genre is None:
        return  # User chose to cancel

    # All field required validation
    if not title or not author or not year or not genre:
        print("Error: All fields must be filled.")
        return
    
    # validate year using the yea
    if not is_valid_year(year):
        print(f"Error: Year must be 4-digits and between 1000 to {CURRENT_YEAR}. Book not added.")
        return
    
    # Adding book to books collection on memory
    book = {"title": title, "author": author, "year": year, "genre": genre}
    books.append(book)
    print("Book added successfully")

# Display Books function
def display_books():
    print("\n ========= Book List =========\n")
    # If no books found
    if len(books) == 0:
        print("No books available.")
        return
    
    # Print table header with fixed columns widths
    print(f"{'ID':<6} {'TITLE':<30} {'AUTHOR':<20} {'YEAR':<6} GENRE")
    print("-" * 80)
    
    # Loop through list and print each book in a formatted table row
    for id, book in enumerate(books):
        print(f"{id:<6} {book['title'][:30]:<30} {book['author'][:20]:<20} {book['year']:<6} {book['genre']}")

    # Menu inside display
    print("\n1. Search a book")
    print("2. Delete a book")
    print("0. Back to main menu")

    user_choice = input("Choose an option: ")

    if user_choice == "1":
        search_books()
    elif user_choice == "2":
        delete_book()
    elif user_choice == "0":
        return
    else:
        print("Invalid option.")

# Search Book function
def search_books():
    print("\n ========= Search Book by keyword =========\n")
    keyword = input("Enter keyword to search (title, author, year, genre): ").strip().lower()

    found = False

    print("\n ========= Search List =========\n")
    # Print table header with fixed columns widths
    print(f"{'ID':<6} {'TITLE':<30} {'AUTHOR':<20} {'YEAR':<6} GENRE")
    print("-" * 80)
    for id, book in enumerate(books):
        # Check if any field contains the search word
        if (keyword in book["title"].lower() or
            keyword in book["author"].lower() or
            keyword in book["year"].lower() or
            keyword in book["genre"].lower()):

            print(f"{id:<6} {book['title'][:30]:<30} {book['author'][:20]:<20} {book['year']:<6} {book['genre']}")
            found = True

    if not found:
        print("No book found.")


# Delete a book by its index
def delete_book():
    print("\n========= Delete Book =========\n")

    index = input("Enter the ID number of the book: ")

    # Check if number
    if not index.isdigit():
        print("Invalid number.")
        return

    index = int(index)

    # Check if in range
    if index < 0 or index >= len(books):
        print("ID does not exist.")
        return

    # Remove book
    removed = books.pop(index)
    print(f"Book '{removed['title']}' deleted.")


# Show statistics
def show_statistics():
    print("\n========= Statistics =========\n")

    print("Total books:", len(books))

    # Count how many per genre
    genre_count = {}
    for book in books:
        counting_genre = book["genre"]
        if counting_genre not in genre_count:
            genre_count[counting_genre] = 1
        else:
            genre_count[counting_genre] += 1

    # Display formatted results
    print("\nBooks by Genre:\n")

    # Table header
    print(f"{'GENRE':<30} {'COUNT':<6}")
    print("-" * 40)

    # Print each genre and count in aligned columns
    for genre, count in genre_count.items():
        print(f"{genre[:30]:<30} {count:<6}")

    
# Save to file
def save_to_file():
    try:
        with open(FILENAME, "w") as file_writer:
            for book in books:
                # Convert book dictionary to a comma-separated line
                line = f"{book['title']},{book['author']},{book['year']},{book['genre']}\n"
                file_writer.write(line)
        print("File saved successfully.")
    except Exception as error:
        print("Error saving file.", error)


# Load from file
def load_from_file():
    try:
        # Auto-create empty file if it does not exist
        if not os.path.exists(FILENAME):
            with open(FILENAME, "w") as file_writer:
                pass  # create an empty file
            print("No saved file found. Empty file created.")
            return

        with open(FILENAME, "r") as file_reader:
            books.clear()

            for line in file_reader:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                parts = line.split(",")

                # Validate correct format (must have exactly 4 fields)
                if len(parts) != 4:
                    print(f"Warning: Skipped corrupted line -> {line}")
                    continue

                title, author, year, genre = parts

                # Validate year
                if not is_valid_year(year):
                    print(f"Warning: Invalid year skipped -> {line}")
                    continue

                books.append({
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre
                })

        print("File loaded successfully.")

    except FileNotFoundError:
        print("No saved file found. Please save a file first.")

    except Exception as error:
        print("Error loading file:", error)


# Help Menu
def help_menu():
    print("\n========== HELP MENU ==========")
    print("1. Add Book        - Add a new book to the list.")
    print("2. Display Books   - Show all stored books in a table.")
    print("3. Search Books    - Search by title, author, year, or genre.")
    print("4. Statistics      - View total books and genre breakdown.")
    print("5. Save File       - Save all books to the data file.")
    print("6. Load File       - Load books from the saved file.")
    print("0. Exit            - Close the program.")
    print("================================\n")


# Exit program
def exit_program():
    while True:
        print("\nAre you sure you want to exit? (Y/N)")
        user_choice = input("Choice: ").strip().lower()

        if user_choice == "y":
            print("Goodbye.")
            raise SystemExit()

        elif user_choice == "n":
            print("Exit cancelled. Returning to main menu...")
            return

        # Inform the user when their input is invalid and prompt them to try again
        else:
            print("Invalid input. Please enter Y or N.")


# -------------------------
# Main program loop
# -------------------------
def main_menu():
    '''
    Main menu loop for Greenfield Community Library Book Management System.
    - Continuously displays a menu of actions until the user chooses to exit.
    - Handles invalid input by prompting the user again.
    '''

    while True:
        # Display the main menu options
        print("\n=== Greenfield Community Library System ===")
        print("1. Add Book")        # Add a new book to the library
        print("2. Display Books")   # Show all books in a formatted table
        print("3. Search Books")    # Search books by title, author, year, or genre
        print("4. Statistics")      # Display total number of books and counts per genre
        print("5. Save File")       # Save all current records to the text file
        print("6. Load File")       # Load records from the text file into memory
        print("7. Help")            # Show help instructions
        print("0. Exit")            # Exit the program

        # Prompt the user to select an option
        user_choice = input("Enter choice: ").strip()

        if user_choice == "1":
            add_book()
        elif user_choice == "2":
            display_books()
        elif user_choice == "3":
            search_books()
        elif user_choice == "4":
            show_statistics()
        elif user_choice == "5":
            save_to_file()
        elif user_choice == "6":
            load_from_file()
        elif user_choice == "7":
            help_menu()
        elif user_choice == "0":
            exit_program()
        else:
            # Handle invalid input
            print("Invalid option. Please try again.")


# Entry point of the program
if __name__ == "__main__":
    main_menu()