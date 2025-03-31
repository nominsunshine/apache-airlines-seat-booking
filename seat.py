import random
import string

# Define row labels representing the aircraft layout
row_labels = ["A", "B", "C", "X", "D", "E", "F"]

# Generate full seating layout for the aircraft
# Rows A–C and D–F are passenger rows
# Row X is the aisle (non-bookable)
# Columns 77 and 78 (index 76, 77) in rows D–F are storage areas
def create_aircraft_layout():
    layout = [
        ['F'] * 80,  # Row A
        ['F'] * 80,  # Row B
        ['F'] * 80,  # Row C
        ['X'] * 80,  # Aisle row (not bookable)
    ]
    for _ in range(3):  # Create rows D, E, F with storage seats
        row = ['F'] * 80
        row[76] = 'S'  # Storage seat at position 77
        row[77] = 'S'  # Storage seat at position 78
        layout.append(row)
    return layout

# Initialize seating layout and storage
seats = create_aircraft_layout()
used_references = set()  # Tracks used booking references
passenger_db = {}        # Simulated database for passenger records

WINDOW_SEATS = [0, 79]   # Window seat columns (1 and 80)
AISLE_SEATS = [3, 76]    # Aisle-adjacent seat columns (4 and 77)

# Generate a unique 8-character alphanumeric booking reference
def generate_booking_reference():
    while True:
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if ref not in used_references:
            used_references.add(ref)
            return ref

# Display a simplified view of the seating layout
def show_seats(agent=False):
    print("\nSeating Layout (showing first and last 6 seats per row):")
    for i, row in enumerate(seats):
        display = []

        # Show first 6 seats of the row
        for seat in row[:6]:
            if agent:
                display.append(seat)  # Staff sees actual seat values
            else:
                display.append("F" if seat == "F" else "R")  # Customer sees only F or R

        display.append("...")  # Indicate skipped middle seats

        # Show last 6 seats of the row
        for seat in row[-6:]:
            if agent:
                display.append(seat)
            else:
                display.append("F" if seat == "F" else "R")

        # Print row label (A–F or X) and seat view
        print(f"Row {row_labels[i]}: {' '.join(display)}")

# Check if a specific seat is available based on input like '12A'
def check_availability():
    try:
        seat_input = input("Enter seat (e.g., 12A): ").strip().upper()
        col = int(seat_input[:-1]) - 1  # Extract seat number
        row_letter = seat_input[-1]     # Extract row letter
        row = row_labels.index(row_letter)
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

# Recommend a seat based on user preference (window/aisle/none)
def recommend_seat(preference):
    for row_idx, row in enumerate(seats):
        row_label = row_labels[row_idx]

        if row_label == 'X':
            continue  # Skip aisle row

        for col_idx in range(len(row)):
            seat = seats[row_idx][col_idx]

            if seat != "F":
                continue  # Skip non-free seats

            if row_label in ["D", "E", "F"] and col_idx in [76, 77]:
                continue  # Skip storage seats

            # Return seat matching user's preference
            if preference == "window" and col_idx in WINDOW_SEATS:
                return row_idx, col_idx
            elif preference == "aisle" and col_idx in AISLE_SEATS:
                return row_idx, col_idx
            elif preference == "none":
                return row_idx, col_idx

    return None  # No seat found

# Book a seat based on preference and collect passenger details
def book_seat():
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

            # Store passenger details in the database
            passenger_db[booking_ref] = {
                "First Name": first_name,
                "Last Name": last_name,
                "Passport": passport,
                "Seat Row": row_labels[row],
                "Seat Column": col + 1
            }

            # Mark the seat with the booking reference
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
                seats[row_idx][col_idx] = "F"  # Mark as free
                passenger_db.pop(booking_ref, None)  # Remove from database
                print(f"Seat with booking reference {booking_ref} has been freed.")
                found = True
                break
        if found:
            break
    if not found:
        print("Booking reference not found.")

# Show all current bookings (Staff Only)
def show_all_bookings():
    if not passenger_db:
        print("No bookings have been made.")
    else:
        for ref, info in passenger_db.items():
            print(f"\nBooking Ref: {ref}")
            for key, value in info.items():
                print(f"  {key}: {value}")

# Main menu interaction based on user role
def main():
    print("Welcome to Apache Airlines Seat Booking System")
    role = input("Are you a Customer or Staff? ").strip().lower()

    if role not in ["customer", "staff"]:
        print("Invalid role. Please restart the program.")
        return

    while True:
        print("\nMenu:")
        print("1. Check availability")
        print("2. Book seat with preference")
        print("3. Free seat")
        print("4. Show seating status")
        if role == "staff":
            print("5. Show all bookings")
            print("6. Exit")
        else:
            print("5. Exit")

        choice = input("Choose option: ")

        if choice == '1':
            check_availability()
        elif choice == '2':
            book_seat()
        elif choice == '3':
            free_seat()
        elif choice == '4':
            show_seats(agent=(role == "staff"))
        elif choice == '5':
            if role == "staff":
                show_all_bookings()
            else:
                print("Exiting program. Goodbye!")
                break
        elif choice == '6' and role == "staff":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please select again.")

# Start the program
main()

