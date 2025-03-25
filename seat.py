# Seat Booking Application for Apache Airlines (Enhanced)

# Initial seating layout: F=Free, R=Booked, X=Aisle, S=Storage (Unbookable)
seats = [
    ["F", "F", "F", "F", "X", "F", "F", "F"],  # Row 1
    ["F", "F", "F", "F", "X", "F", "F", "F"],  # Row 2
    ["F", "F", "F", "F", "X", "F", "F", "F"],  # Row 3
    ["X", "X", "X", "X", "X", "X", "X", "X"],  # Row 4 (Aisle)
    ["F", "F", "F", "F", "X", "S", "F", "F"],  # Row 5
    ["F", "F", "F", "F", "X", "S", "F", "F"],  # Row 6
    ["F", "F", "F", "F", "X", "S", "F", "F"]   # Row 7
]

seat_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
WINDOW_SEATS = [0, 7]
AISLE_SEATS = [3, 5]

# Display seating layout clearly
def show_seats():
    print("\nSeating Layout (F=Free, R=Booked, X=Aisle, S=Storage):")
    for i, row in enumerate(seats):
        print(f"Row {i + 1}: {' '.join(row)}")

# Check seat availability with robust input handling
def check_availability():
    try:
        row = int(input("Enter row number: ")) - 1
        col = int(input("Enter column number: ")) - 1
    except ValueError:
        print("Please enter valid numbers for row and column.")
        return

    if 0 <= row < len(seats) and 0 <= col < len(seats[row]):
        seat = seats[row][col]
        if seat == "F":
            print("Seat is available.")
        elif seat == "R":
            print("Seat is already booked.")
        elif seat in ["X", "S"]:
            print("This seat is not bookable (aisle/storage).")
    else:
        print("Invalid seat position entered.")

# Recommend seat based on preference clearly and centrally
def recommend_seat(preference):
    for row_idx, row in enumerate(seats):
        for col_idx, seat in enumerate(row):
            if seat == "F":
                if preference == "window" and col_idx in WINDOW_SEATS:
                    return row_idx, col_idx
                elif preference == "aisle" and col_idx in AISLE_SEATS:
                    return row_idx, col_idx
                elif preference == "none":
                    return row_idx, col_idx
    return None

# Book seat based on preference clearly
def book_seat():
    preference = input("Enter seat preference (Window/Aisle/None): ").lower()
    recommended = recommend_seat(preference)
    if recommended:
        print(f"Recommended seat: Row {recommended[0]+1}, Seat {seat_labels[recommended[1]]}")
        confirm = input("Confirm booking? (y/n): ").lower()
        if confirm == 'y':
            seats[recommended[0]][recommended[1]] = "R"
            print("Seat successfully booked.")
        else:
            print("Booking cancelled.")
    else:
        print("No available seats matching your preference.")

# Free booked seat clearly with validation
def free_seat():
    try:
        row = int(input("Enter row number to free: ")) - 1
        col = int(input("Enter column number to free: ")) - 1
    except ValueError:
        print("Please enter valid numbers for row and column.")
        return

    if 0 <= row < len(seats) and 0 <= col < len(seats[row]) and seats[row][col] == "R":
        seats[row][col] = "F"
        print("Seat successfully freed.")
    else:
        print("Seat cannot be freed (it may not be booked or is unbookable).")

# Main interaction menu clearly defined
def main():
    while True:
        print("\nMenu:")
        print("1. Check availability")
        print("2. Book seat with preference")
        print("3. Free seat")
        print("4. Show seating status")
        print("5. Exit")
        choice = input("Choose option (1-5): ")

        if choice == '1':
            check_availability()
        elif choice == '2':
            book_seat()
        elif choice == '3':
            free_seat()
        elif choice == '4':
            show_seats()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please select again.")

# Start the program
main()

