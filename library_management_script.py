import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import sys
class LibraryManagementSystem:
    #connecting to the database or raising an error
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='library',
                user='root',
                password='mysqlcode'
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
                
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

#function to quit at any time
    def check_quit(self, user_input):
        if user_input is None:
            return user_input
            
        normalized = user_input.strip().lower()
        if normalized in ('quit', 'exit', 'q'):
            print("\nGoodbye!")
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("MySQL connection closed")
            sys.exit(0)
        
        return user_input.strip()  



    def add_book(self):
        if not self.connection:
            return
        print("\n--- Add New Book ---")
        #requesting all of the book's information in order to file it

        isbn = self.check_quit(input("Enter ISBN: "))
        title = self.check_quit(input("Enter Title: "))
        author = self.check_quit(input("Enter Author: "))
        category = self.check_quit(input("Enter Category: "))
        publisher = self.check_quit(input("Enter Publisher: "))
        #in each case of input we make sure that it is always valid or quit
        while True:
            rental_input = self.check_quit(input("Enter Rental Price: "))
            try:
                rental_price = float(rental_input)
                break
            except ValueError:
                print("Please enter a valid number for rental price.")
        
        while True:
            year_input = self.check_quit(input("Enter Published Year (YYYY): "))
            if len(year_input) == 4 and year_input.isdigit():
                published_year = int(year_input)
                break
            print("Please enter a valid 4-digit year")
        
        while True:
            purchase_input = self.check_quit(input("Enter Purchase Price: "))
            try:
                purchase_price = float(purchase_input)
                break
            except ValueError:
                print("Please enter a valid number for purchase price.")
    #if user presses enter, it's today's date    
        date_input = self.check_quit(input("Enter Purchase Date (YYYY-MM-DD) or press Enter for today: "))
        if not date_input:
            purchase_date = datetime.now().date()
        else:
            purchase_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        
        while True:
            branch_input = self.check_quit(input("Enter Branch Number: "))
            try:
                branch_no = int(branch_input)
                break
            except ValueError:
                print("Please enter a valid numeric branch number.")
        
        shelf_location = self.check_quit(input("Enter Shelf Location: "))
        
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO books (ISBN, Book_title, Author, Category, Publisher, 
                    Rental_Price, Purchase_price, Published_year, Purchase_date, Branch_no, Shelf_location, Status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Available')"""
            values = (isbn, title, author, category, publisher, rental_price, 
                    purchase_price, published_year, purchase_date, branch_no, shelf_location)
            cursor.execute(query, values)
            self.connection.commit()
            print("Book added successfully!")
            
        except Error as e:
            print(f"Error adding book: {e}")
        finally:
            if cursor:
                cursor.close()

    def search_books(self):
        if not self.connection:
            return
        print("\n--- Search Books ---")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by Category")
        print("4. Search by ISBN")
        search_type = self.check_quit(input("Choose search type (1-4): "))        
        search_term = self.check_quit(input("Enter search term: "))   
        #for each choise we create the right view     
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if search_type == '1':
                query = "SELECT * FROM books WHERE Book_title LIKE %s"
            elif search_type == '2':
                query = "SELECT * FROM books WHERE Author LIKE %s"
            elif search_type == '3':
                query = "SELECT * FROM books WHERE Category LIKE %s"
            elif search_type == '4':
                query = "SELECT * FROM books WHERE ISBN = %s"
            else:
                print("Invalid search type")
                return
                
            values = (f'%{search_term}%',) if search_type != '4' else (search_term,)
            cursor.execute(query, values)
            results = cursor.fetchall()
            
            if results:
                print("\nSearch Results:")
                for book in results:
                    print(f"ISBN: {book['ISBN']}")
                    print(f"Title: {book['Book_title']}")
                    print(f"Author: {book['Author']}")
                    print(f"Category: {book['Category']}")
                    print(f"Status: {book['Status']}")
                    print(f"Rental Price: ${book['Rental_Price']}")
                    print(f"Published Year: {book['Published_year']}")
                    print(f"Branch: {book['Branch_no']}")
                    print(f"Shelf: {book['Shelf_location']}")
                    print("-" * 40)
            else:
                print("No books found matching your search.")
                
        except Error as e:
            print(f"Error searching books: {e}")
        finally:
            if cursor:
                cursor.close()

    def register_customer(self):
        if not self.connection:
            return
            
        print("\n--- Register New Customer ---")
        name = self.check_quit(input("Enter Customer Name: "))
        address = self.check_quit(input("Enter Address: "))
        email = self.check_quit(input("Enter Email: "))
        phone = self.check_quit(input("Enter Phone: "))
        
        #validate membership type
        while True:
            membership_type = self.check_quit(input("Enter Membership Type (Basic/Premium/Gold): ")).capitalize()
            if membership_type in ['Basic', 'Premium', 'Gold']:
                break
            print("Invalid membership type. Please choose from Basic, Premium, or Gold.")
        
        #calculate expiry date (1 year from today)
        reg_date = datetime.now().date()
        expiry_date = reg_date + timedelta(days=365)

        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO Customer (Customer_name, Customer_address, Email, 
                       Phone, Reg_date, Membership_type, Membership_expiry) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (name, address, email, phone, reg_date, membership_type, expiry_date)
            cursor.execute(query, values)
            self.connection.commit()
            
            #get the new customer ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            customer_id = cursor.fetchone()[0]
            print(f"Customer registered successfully! Customer ID: {customer_id}")
            
        except Error as e:
            print(f"Error registering customer: {e}")
        finally:
            if cursor:
                cursor.close()

    def issue_book(self):
        if not self.connection:
            return
            
        print("\n--- Issue Book ---")
        
        #get employee id
        while True:
            try:
                emp_id_input = self.check_quit(input("Enter Your Employee ID: "))               
                if emp_id_input.strip():                    
                    emp_id = int(emp_id_input)
                    break
                else:
                    print("Employee ID cannot be empty. Please enter a valid Employee ID.")
            except ValueError:
                print("Please enter a valid numeric Employee ID.")
        
        #get customer id
        while True:
            try:
                customer_input = self.check_quit(input("Enter Customer ID: "))
                customer_id = int(customer_input)
                break
            except ValueError:
                print("Please enter a valid numeric Customer ID.")
        
        #get ISBN
        isbn = self.check_quit(input("Enter ISBN of book to issue: "))
        
        try:
            cursor = self.connection.cursor()
            
            #check if customer exists and has active membership
            cursor.execute("""SELECT Customer_Id, Membership_expiry 
                        FROM Customer 
                        WHERE Customer_Id = %s AND Membership_expiry >= %s""", 
                        (customer_id, datetime.now().date()))
            customer = cursor.fetchone()
            
            if not customer:
                print("Customer not found or membership has expired!")
                return
                
            #check if employee exists
            cursor.execute("SELECT Emp_id FROM Employee WHERE Emp_id = %s", (emp_id,))
            if not cursor.fetchone():
                print("Invalid Employee ID!")
                return
            
            #check if book is available
            cursor.execute("SELECT Status, Book_title FROM books WHERE ISBN = %s", (isbn,))
            book = cursor.fetchone()
            
            if not book:
                print("Book not found!")
                return
                
            if book[0] != 'Available':
                print("Book is not available for issue!")
                return
                
            #set issue and due dates
            issue_date = datetime.now().date()
            due_date = issue_date + timedelta(days=14)  # 2-week loan period
            
            #finally issue the book
            query = """INSERT INTO IssueStatus (Issued_cust, Issued_book_isbn, Issue_date, 
                    Due_date, Issued_by_emp) 
                    VALUES (%s, %s, %s, %s, %s)"""
            values = (customer_id, isbn, issue_date, due_date, emp_id)
            cursor.execute(query, values)
            
            #update status
            cursor.execute("UPDATE books SET Status = 'Issued' WHERE ISBN = %s", (isbn,))
            
            self.connection.commit()
            print(f"Book '{book[1]}' issued successfully! Due date: {due_date}")
            
        except Error as e:
            print(f"Error issuing book: {e}")
        finally:
            if cursor:
                cursor.close()





    def return_book(self):
        if not self.connection:
            return
            
        print("\n--- Return Book ---")
        
        #customer ID 
        while True:
            try:
                customer_input = self.check_quit(input("Enter Customer ID: "))
                customer_id = int(customer_input)
                break
            except ValueError:
                print("Please enter a valid numeric Customer ID.")
        
        isbn = self.check_quit(input("Enter ISBN of book to return: "))
        
        try:
            cursor = self.connection.cursor()
            
            #active issue record
            query = """SELECT i.Issue_Id, i.Issue_date, i.Due_date, b.Book_title 
                    FROM IssueStatus i
                    JOIN Books b ON i.Issued_book_isbn = b.ISBN
                    WHERE i.Issued_cust = %s AND i.Issued_book_isbn = %s AND i.Return_date IS NULL"""
            cursor.execute(query, (customer_id, isbn))
            issue = cursor.fetchone()
            
            if not issue:
                print("No active issue record found for this book and customer!")
                return
                
            issue_id, issue_date, due_date, book_title = issue
            return_date = datetime.now().date()
            
            #fine if overdue
            fine_amount = 0
            if return_date > due_date:
                days_overdue = (return_date - due_date).days
                fine_amount = days_overdue * 1.00  # $1 per day fine
                print(f"Book '{book_title}' is {days_overdue} days overdue. Fine: ${fine_amount:.2f}")
                
                #record fine
                fine_query = """INSERT INTO Fines (Customer_id, Issue_id, Fine_date, Amount) 
                                VALUES (%s, %s, %s, %s)"""
                fine_values = (customer_id, issue_id, return_date, fine_amount)
                cursor.execute(fine_query, fine_values)
            
            #update issue record with return date and fine
            update_query = """UPDATE IssueStatus 
                            SET Return_date = %s, Fine_amount = %s 
                            WHERE Issue_Id = %s"""
            cursor.execute(update_query, (return_date, fine_amount, issue_id))
            
            #update status
            cursor.execute("UPDATE books SET Status = 'Available' WHERE ISBN = %s", (isbn,))
            
            self.connection.commit()
            print(f"Book '{book_title}' returned successfully!")
            
        except Error as e:
            print(f"Error returning book: {e}")
        finally:
            if cursor:
                cursor.close()

    def view_overdue_books(self):
        if not self.connection:
            return
            
        print("\n--- Currently Overdue Books ---")
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """SELECT c.Customer_name, b.Book_title, i.Issue_date, i.Due_date, 
                              DATEDIFF(CURDATE(), i.Due_date) AS Days_Overdue
                       FROM IssueStatus i
                       JOIN Customer c ON i.Issued_cust = c.Customer_Id
                       JOIN Books b ON i.Issued_book_isbn = b.ISBN
                       WHERE i.Return_date IS NULL AND i.Due_date < CURDATE()"""
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                for book in results:
                    print(f"Customer: {book['Customer_name']}")
                    print(f"Book: {book['Book_title']}")
                    print(f"Issue Date: {book['Issue_date']}")
                    print(f"Due Date: {book['Due_date']}")
                    print(f"Days Overdue: {book['Days_Overdue']}")
                    print("-" * 40)
            else:
                print("No overdue books found.")
                
        except Error as e:
            print(f"Error retrieving overdue books: {e}")
        finally:
            if cursor:
                cursor.close()
    def view_issues(self):
        if not self.connection:
            return
            
        print("\n--- View Issue Records ---")
        print("1. View all issue records")
        print("2. View active issues (not returned)")
        print("3. View issues by customer")
        print("4. View issues by book")
        print("5. View issues by date range")
        view_type = self.check_quit(input("Choose view type (1-5): "))
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            #just all issue records
            if view_type == '1':
                query = """SELECT i.Issue_Id, c.Customer_name, b.Book_title, i.Issue_date, 
                                i.Due_date, i.Return_date, i.Fine_amount, e.Emp_name as Issued_By
                        FROM IssueStatus i
                        JOIN Customer c ON i.Issued_cust = c.Customer_Id
                        JOIN Books b ON i.Issued_book_isbn = b.ISBN
                        LEFT JOIN Employee e ON i.Issued_by_emp = e.Emp_id
                        ORDER BY i.Issue_date DESC"""
                cursor.execute(query)
                #currently issued records
            elif view_type == '2':
                query = """SELECT i.Issue_Id, c.Customer_name, b.Book_title, i.Issue_date, 
                                i.Due_date, i.Fine_amount, e.Emp_name as Issued_By
                        FROM IssueStatus i
                        JOIN Customer c ON i.Issued_cust = c.Customer_Id
                        JOIN Books b ON i.Issued_book_isbn = b.ISBN
                        LEFT JOIN Employee e ON i.Issued_by_emp = e.Emp_id
                        WHERE i.Return_date IS NULL
                        ORDER BY i.Due_date"""
                cursor.execute(query)
                
            elif view_type == '3':
                #by customer
                while True:
                    try:
                        customer_input = self.check_quit(input("Enter Customer ID: "))
                        customer_id = int(customer_input)
                        break
                    except ValueError:
                        print("Please enter a valid numeric Customer ID.")
                
                query = """SELECT i.Issue_Id, c.Customer_name, b.Book_title, i.Issue_date, 
                                i.Due_date, i.Return_date, i.Fine_amount, e.Emp_name as Issued_By
                        FROM IssueStatus i
                        JOIN Customer c ON i.Issued_cust = c.Customer_Id
                        JOIN Books b ON i.Issued_book_isbn = b.ISBN
                        LEFT JOIN Employee e ON i.Issued_by_emp = e.Emp_id
                        WHERE i.Issued_cust = %s
                        ORDER BY i.Issue_date DESC"""
                cursor.execute(query, (customer_id,))
                #by book
            elif view_type == '4':
                isbn = self.check_quit(input("Enter ISBN: "))
                query = """SELECT i.Issue_Id, c.Customer_name, b.Book_title, i.Issue_date, 
                                i.Due_date, i.Return_date, i.Fine_amount, e.Emp_name as Issued_By
                        FROM IssueStatus i
                        JOIN Customer c ON i.Issued_cust = c.Customer_Id
                        JOIN Books b ON i.Issued_book_isbn = b.ISBN
                        LEFT JOIN Employee e ON i.Issued_by_emp = e.Emp_id
                        WHERE i.Issued_book_isbn = %s
                        ORDER BY i.Issue_date DESC"""
                cursor.execute(query, (isbn,))
                #by date range
            elif view_type == '5':
                start_date = self.check_quit(input("Enter start date (YYYY-MM-DD): "))
                end_date = self.check_quit(input("Enter end date (YYYY-MM-DD): "))
                query = """SELECT i.Issue_Id, c.Customer_name, b.Book_title, i.Issue_date, 
                                i.Due_date, i.Return_date, i.Fine_amount, e.Emp_name as Issued_By
                        FROM IssueStatus i
                        JOIN Customer c ON i.Issued_cust = c.Customer_Id
                        JOIN Books b ON i.Issued_book_isbn = b.ISBN
                        LEFT JOIN Employee e ON i.Issued_by_emp = e.Emp_id
                        WHERE i.Issue_date BETWEEN %s AND %s
                        ORDER BY i.Issue_date"""
                cursor.execute(query, (start_date, end_date))
                
            else:
                print("Invalid view type")
                return
                
            results = cursor.fetchall()
            
            if results:
                print("\nIssue Records:")
                print("-" * 100)
                for issue in results:
                    print(f"Issue ID: {issue['Issue_Id']}")
                    print(f"Customer: {issue['Customer_name']}")
                    print(f"Book: {issue['Book_title']}")
                    print(f"Issue Date: {issue['Issue_date']}")
                    print(f"Due Date: {issue['Due_date']}")
                    
                    if 'Return_date' in issue and issue['Return_date']:
                        print(f"Return Date: {issue['Return_date']}")
                    else:
                        print("Status: Still Issued")
                        
                    if issue['Fine_amount'] and issue['Fine_amount'] > 0:
                        print(f"Fine Amount: ${issue['Fine_amount']:.2f}")
                        
                    if issue['Issued_By']:
                        print(f"Issued By: {issue['Issued_By']}")
                        
                    print("-" * 100)
                    
                print(f"Total records found: {len(results)}")
            else:
                print("No issue records found.")
                
        except Error as e:
            print(f"Error viewing issue records: {e}")
        finally:
            if cursor:
                cursor.close()

    def show_menu(self):
        while True:
            print("\n=== Library Management System ===")
            print("1. Add New Book")
            print("2. Search Books")
            print("3. Return Book")
            print("4. Issue Book")
            print("5. View Issue Records")
            print("6. View Overdue Books")
            print("7. Make Reservation")
            print("8. View Reservations")
            print("9. Cancel Reservation")
            print("10. Register Customer")
            print("11. Exit")
            print("\nType 'quit', 'exit', or 'q' at any prompt to exit the program")
            
            
            user_input = input("Enter your choice (1-11): ")
            choice = self.check_quit(user_input)
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.search_books()
            elif choice == '3':
                self.return_book()
            elif choice == '4':
                self.issue_book()
            elif choice == '5':
                self.view_issues()
            elif choice == '6':
                self.view_overdue_books()
            elif choice == '7':
                self.make_reservation()
            elif choice == '8':
                self.view_reservations()
            elif choice == '9':
                self.cancel_reservation()
            elif choice == '10':
                self.register_customer()
            elif choice == '11':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def make_reservation(self):
        if not self.connection:
            return
            
        print("\n--- Make Reservation ---")
        
        #customer id
        while True:
            try:
                customer_input = self.check_quit(input("Enter Customer ID: "))
                customer_id = int(customer_input)
                break
            except ValueError:
                print("Please enter a valid numeric Customer ID.")
        
        isbn = self.check_quit(input("Enter ISBN of book to reserve: "))
        
        try:
            cursor = self.connection.cursor()
            
            #if customer exists and has active membership
            cursor.execute("""SELECT Customer_Id, Membership_expiry 
                        FROM Customer 
                        WHERE Customer_Id = %s AND Membership_expiry >= %s""", 
                        (customer_id, datetime.now().date()))
            customer = cursor.fetchone()
            
            if not customer:
                print("Customer not found or membership has expired!")
                return
                
            #if book exists
            cursor.execute("SELECT Status, Book_title FROM books WHERE ISBN = %s", (isbn,))
            book = cursor.fetchone()
            
            if not book:
                print("Book not found!")
                return
                
            book_status = book[0]
            book_title = book[1]
            
            # if book is already available,can issue it now
            if book_status == 'Available':
                print("This book is currently available. No need to reserve - you can issue it directly.")
                return
                
            #check if book is already reserved by this customer
            cursor.execute("""SELECT Reservation_id FROM Reservations 
                        WHERE Customer_id = %s AND Book_isbn = %s AND Status = 'Pending'""", 
                        (customer_id, isbn))
            existing_reservation = cursor.fetchone()
            
            if existing_reservation:
                print("You already have a pending reservation for this book!")
                return
                
            #make reservation
            reservation_date = datetime.now().date()
            query = """INSERT INTO Reservations (Customer_id, Book_isbn, Reservation_date, Status) 
                    VALUES (%s, %s, %s, 'Pending')"""
            values = (customer_id, isbn, reservation_date)
            cursor.execute(query, values)
            
            #update book status to Reserved if it's not already reserved
            if book_status != 'Reserved':
                cursor.execute("UPDATE books SET Status = 'Reserved' WHERE ISBN = %s", (isbn,))
            
            self.connection.commit()
            print(f"Book '{book_title}' reserved successfully! You will be notified when it becomes available.")
            
        except Error as e:
            print(f"Error making reservation: {e}")
        finally:
            if cursor:
                cursor.close()

    def view_reservations(self):
        if not self.connection:
            return
            
        print("\n--- View Reservations ---")
        print("1. View all reservations")
        print("2. View reservations by customer")
        print("3. View reservations by book")
        view_type = self.check_quit(input("Choose view type (1-3): "))
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            #all reservations
            if view_type == '1':
                query = """SELECT r.Reservation_id, c.Customer_name, b.Book_title, r.Reservation_date, r.Status
                        FROM Reservations r
                        JOIN Customer c ON r.Customer_id = c.Customer_Id
                        JOIN Books b ON r.Book_isbn = b.ISBN
                        ORDER BY r.Reservation_date DESC"""
                cursor.execute(query)

                
            elif view_type == '2':
                # by customer id
                while True:
                    try:
                        customer_input = self.check_quit(input("Enter Customer ID: "))
                        customer_id = int(customer_input)
                        break
                    except ValueError:
                        print("Please enter a valid numeric Customer ID.")
                
                query = """SELECT r.Reservation_id, c.Customer_name, b.Book_title, r.Reservation_date, r.Status
                        FROM Reservations r
                        JOIN Customer c ON r.Customer_id = c.Customer_Id
                        JOIN Books b ON r.Book_isbn = b.ISBN
                        WHERE r.Customer_id = %s
                        ORDER BY r.Reservation_date DESC"""
                cursor.execute(query, (customer_id,))

                #by book
            elif view_type == '3':
                isbn = self.check_quit(input("Enter ISBN: "))
                query = """SELECT r.Reservation_id, c.Customer_name, b.Book_title, r.Reservation_date, r.Status
                        FROM Reservations r
                        JOIN Customer c ON r.Customer_id = c.Customer_Id
                        JOIN Books b ON r.Book_isbn = b.ISBN
                        WHERE r.Book_isbn = %s
                        ORDER BY r.Reservation_date DESC"""
                cursor.execute(query, (isbn,))
                
            else:
                print("Invalid view type")
                return
                
            results = cursor.fetchall()
            
            if results:
                print("\nReservation Results:")
                for reservation in results:
                    print(f"Reservation ID: {reservation['Reservation_id']}")
                    print(f"Customer: {reservation['Customer_name']}")
                    print(f"Book: {reservation['Book_title']}")
                    print(f"Reservation Date: {reservation['Reservation_date']}")
                    print(f"Status: {reservation['Status']}")
                    print("-" * 40)
            else:
                print("No reservations found.")
                
        except Error as e:
            print(f"Error viewing reservations: {e}")
        finally:
            if cursor:
                cursor.close()

    def cancel_reservation(self):
        if not self.connection:
            return
            
        print("\n--- Cancel Reservation ---")
        
        #reservation id
        while True:
            try:
                reservation_input = self.check_quit(input("Enter Reservation ID to cancel: "))
                reservation_id = int(reservation_input)
                break
            except ValueError:
                print("Please enter a valid numeric Reservation ID.")
        
        try:
            cursor = self.connection.cursor()
            
            #reservation details
            cursor.execute("""SELECT r.Book_isbn, b.Book_title 
                        FROM Reservations r
                        JOIN Books b ON r.Book_isbn = b.ISBN
                        WHERE r.Reservation_id = %s""", (reservation_id,))
            reservation = cursor.fetchone()
            
            if not reservation:
                print("Reservation not found!")
                return
                
            book_isbn, book_title = reservation
            
            #cancel the reservation
            cursor.execute("""UPDATE Reservations SET Status = 'Cancelled' 
                        WHERE Reservation_id = %s""", (reservation_id,))
            
            #check if there are other pending reservations for this book
            cursor.execute("""SELECT COUNT(*) FROM Reservations 
                        WHERE Book_isbn = %s AND Status = 'Pending'""", (book_isbn,))
            pending_count = cursor.fetchone()[0]
            
            #if no more pending reservations, set book status back to Available
            if pending_count == 0:
                cursor.execute("""UPDATE Books SET Status = 'Available' 
                            WHERE ISBN = %s AND Status = 'Reserved'""", (book_isbn,))
            
            self.connection.commit()
            print(f"Reservation for '{book_title}' has been cancelled successfully!")
            
        except Error as e:
            print(f"Error cancelling reservation: {e}")
        finally:
            if cursor:
                cursor.close()



#run the application
if __name__ == "__main__":
    library_system = LibraryManagementSystem()
    if library_system.connection:
        library_system.show_menu()