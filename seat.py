import random
import string

# Define row labels corresponding to the aircraft layout
row_labels = ["A", "B", "C", "X", "D", "E", "F"]

# Generate full seating layout for the aircraft
# Each row has 80 seats. Rows D, E, F contain storage seats at positions 77 and 78.
def create_aircraft_layout():
    layout = [
        ['F'] * 80,  # Row A
        ['F'] * 80,  # Row B
        ['F'] * 80,  # Row C
        ['X'] * 80,  # Aisle Row (non-bookable)
    ]
    for _ in range(3):  # Create Rows D, E, F (same structure)
        row = ['F'] * 80  # Start with all seats free
        row[76] = 'S'     # Storage at column 77
        row[77] = 'S'     # Storage at column 78
        layout.append(row)
    return layout

# Initialize the seating layout
seats = create_aircraft_layout()

# Track used booking references to ensure uniqueness
used_references = set()
# Simulate a database of bookings using a dictionary
passenger_db = {}

WINDOW_SEATS = [0, 79]  # Window seats at the ends of the row
AISLE_SEATS = [3, 76]   # Seats near the aisle for preference logic

# Generate a unique 8-character booking reference
def generate_booking_reference():
    """
    Generates an 8-character alphanumeric booking reference.
    Ensures the reference is unique by checking against used_references.
    """
    while True:
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if ref not in used_references:
            used_references.add(ref)
            return ref

# Display a condensed version of the seating layout
def show_seats():
    print("\nSeating Layout (showing first and last 6 seats per row):")
    for i, row in enumerate(seats):
        # Show only the beginning and end of each row to keep output clean
        display = row[:6] + ['...'] + row[-6:]
        print(f"Row {row_labels[i]}: {' '.join(display)}")

# Check if a specific seat is available using seat input like '12A'
def check_availability():
    try:
        seat_input = input("Enter seat (e.g., 12A): ").strip().upper()
        col = int(seat_input[:-1]) - 1  # Extract column (seat number)
        row_letter = seat_input[-1]     # Extract row letter (A–F)
        row = row_labels.index(row_letter)  # Convert letter to index
    except (ValueError, IndexError):
        print("Invalid input. Use format like 12A.")
        return

    if 0 <= row < len(seats) and 0 <= col < 80:
        seat = seats[row][col]
        if seat == "F":
            print("Seat is available.")
        elif seat in ["X", "S"]:
            print("This seat is not bookable.")
        else:
            print(f"Seat is booked. Booking reference: {seat}")
    else:
        print("Seat does not exist.")

# Recommend a seat based on passenger preference (window/aisle/none)
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

# Book a seat and collect passenger details
def book_seat():
    """
    Recommends a seat based on preference and confirms booking.
    Collects passenger details and stores them with the generated reference.
    """
    preference = input("Enter seat preference (Window/Aisle/None): ").lower()
    recommended = recommend_seat(preference)
    if recommended:
        row, col = recommended
        print(f"Recommended seat: {col + 1}{row_labels[row]}")
        confirm = input("Confirm booking? (y/n): ").lower()
        if confirm == 'y':
            booking_ref = generate_booking_reference()
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            passport = input("Enter Passport Number: ")

            # Store passenger details
            passenger_db[booking_ref] = {
                "First Name": first_name,
                "Last Name": last_name,
                "Passport": passport,
                "Seat Row": row_labels[row],
                "Seat Column": col + 1
            }

            # Update the seat layout with the booking reference
            seats[row][col] = booking_ref
            print(f"Seat booked! Your booking reference is: {booking_ref}")
        else:
            print("Booking cancelled.")
    else:
        print("No available seats matching your preference.")

# Free a seat using a booking reference
def free_seat():
    booking_ref = input("Enter booking reference to free: ").upper()
    found = False
    for row_idx, row in enumerate(seats):
        for col_idx, value in enumerate(row):
            if value == booking_ref:
                seats[row_idx][col_idx] = "F"  # Reset seat to Free
                passenger_db.pop(booking_ref, None)  # Remove passenger record
                print(f"Seat with booking reference {booking_ref} has been freed.")
                found = True
                break
        if found:
            break
    if not found:
        print("Booking reference not found.")

# Display all passenger bookings with their details
def show_all_bookings():
    if not passenger_db:
        print("No bookings have been made.")
    else:
        for ref, info in passenger_db.items():
            print(f"\nBooking Ref: {ref}")
            for key, value in info.items():
                print(f"  {key}: {value}")

# Main user interaction menu
def main():
    while True:
        print("\nMenu:")
        print("1. Check availability")
        print("2. Book seat with preference")
        print("3. Free seat")
        print("4. Show seating status")
        print("5. Show all bookings")
        print("6. Exit")
        choice = input("Choose option (1-6): ")

        if choice == '1':
            check_availability()
        elif choice == '2':
            book_seat()
        elif choice == '3':
            free_seat()
        elif choice == '4':
            show_seats()
        elif choice == '5':
            show_all_bookings()
        elif choice == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please select again.")

# Start the program
main()

