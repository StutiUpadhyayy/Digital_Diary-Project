from datetime import datetime

FILE_NAME = "diary.txt"


def load_notes():
    """Load notes from the text file and return them as a list of dictionaries."""
    notes = []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                line = line.rstrip("\n")
                if not line.strip():
                    continue

                # Split only at the first separator so note text may contain '|'.
                parts = line.split(" | ", 1)
                if len(parts) == 2:
                    date, text = parts
                    notes.append({"date": date, "text": text})
    except FileNotFoundError:
        # The diary file is created automatically when the first note is saved.
        pass
    except OSError as error:
        print(f"Error reading diary file: {error}")

    return notes


def save_notes(notes):
    """Save the complete notes list to the text file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for note in notes:
                file.write(f"{note['date']} | {note['text']}\n")
        return True
    except OSError as error:
        print(f"Error saving diary file: {error}")
        return False


def is_valid_date(date_text):
    """Check that a date exactly follows YYYY-MM-DD and is a real calendar date."""
    try:
        parsed_date = datetime.strptime(date_text, "%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%d") == date_text
    except ValueError:
        return False


def add_note():
    """Get date and text from the user, validate them, and save the note."""
    date_text = input("Enter date (YYYY-MM-DD): ").strip()

    if not is_valid_date(date_text):
        print("Invalid date. Use YYYY-MM-DD.")
        return

    note_text = input("Enter note text: ").strip()

    if not note_text:
        print("Note text cannot be empty.")
        return

    notes = load_notes()
    notes.append({"date": date_text, "text": note_text})

    if save_notes(notes):
        print("Note saved.")


def view_all_notes():
    """Display all notes with note numbers starting from 1."""
    notes = load_notes()

    if not notes:
        print("No notes found. Your diary is empty.")
        return

    print("\n--- ALL DIARY NOTES ---")
    for number, note in enumerate(notes, start=1):
        print(f"{number} | {note['date']} | {note['text']}")


def search_notes():
    """Search note text by keyword without case sensitivity."""
    keyword = input("Enter keyword to search: ").strip()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    notes = load_notes()
    matches = []

    for number, note in enumerate(notes, start=1):
        # lower() makes the search case-insensitive; find() checks for a match.
        if note["text"].lower().find(keyword.lower()) != -1:
            matches.append((number, note))

    if not matches:
        print("No matching notes found.")
        return

    print(f"Found {len(matches)} note(s):")
    for number, note in matches:
        print(f"{number} | {note['date']} | {note['text']}")


def delete_note():
    """Delete a note using its displayed number."""
    notes = load_notes()

    if not notes:
        print("No notes found. Your diary is empty.")
        return

    try:
        number = int(input("Enter note number to delete: ").strip())
    except ValueError:
        print("Invalid note number. Enter a whole number.")
        return

    if number < 1 or number > len(notes):
        print(f"Note number {number} not found.")
        return

    deleted_note = notes.pop(number - 1)

    if save_notes(notes):
        print(f"Note {number} deleted.")


def show_menu():
    """Display the main menu."""
    print("\n========== DIGITAL DIARY ==========")
    print("1. Add note")
    print("2. View all notes")
    print("3. Search notes")
    print("4. Delete note")
    print("5. Exit")
    print("===================================")


def main():
    """Run the application until the user chooses Exit."""
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_note()
        elif choice == "2":
            view_all_notes()
        elif choice == "3":
            search_notes()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            print("Thank you for using Digital Diary. Goodbye!")
            break
        else:
            print("Invalid menu option. Please choose 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
