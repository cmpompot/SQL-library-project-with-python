-- Library Management System Database Setup

-- drop database if exists and create new one
DROP DATABASE IF EXISTS Library;
CREATE DATABASE Library;
USE Library;

CREATE TABLE IF NOT EXISTS Branch (
    Branch_no INT AUTO_INCREMENT PRIMARY KEY,
    Branch_name VARCHAR(50) NOT NULL,
    Manager_id VARCHAR(10),
    Branch_address VARCHAR(100) NOT NULL,
    Contact_no VARCHAR(15) NOT NULL,
    UNIQUE KEY unique_branch_name (Branch_name)
);

CREATE TABLE IF NOT EXISTS Employee (
    Emp_id INT AUTO_INCREMENT PRIMARY KEY,
    Emp_name VARCHAR(50) NOT NULL,
    Position VARCHAR(30) NOT NULL,
    Salary DECIMAL(10,2) CHECK (Salary > 0),
    Hire_date DATE NOT NULL,
    Branch_no INT,
    Email VARCHAR(100) UNIQUE,
    FOREIGN KEY (Branch_no) REFERENCES Branch(Branch_no) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Customer (
    Customer_Id INT AUTO_INCREMENT PRIMARY KEY,
    Customer_name VARCHAR(50) NOT NULL,
    Customer_address VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    Reg_date DATE NOT NULL,
    Membership_type ENUM('Basic', 'Premium', 'Gold') DEFAULT 'Basic',
    Membership_expiry DATE
);

CREATE TABLE IF NOT EXISTS Books (
    ISBN VARCHAR(20) PRIMARY KEY,
    Book_title VARCHAR(100) NOT NULL,
    Category VARCHAR(30) NOT NULL,
    Rental_Price DECIMAL(10,2) CHECK (Rental_Price >= 0),
    Status ENUM('Available', 'Issued', 'Reserved', 'Under Maintenance') DEFAULT 'Available',
    Author VARCHAR(50) NOT NULL,
    Publisher VARCHAR(50) NOT NULL,
    Published_year smallint,
    Purchase_date DATE,
    Purchase_price DECIMAL(10,2),
    Branch_no INT,
    Shelf_location VARCHAR(20),
    FOREIGN KEY (Branch_no) REFERENCES Branch(Branch_no) ON DELETE SET NULL,
    INDEX idx_category (Category),
    INDEX idx_author (Author)
);

CREATE TABLE IF NOT EXISTS IssueStatus (
    Issue_Id INT AUTO_INCREMENT PRIMARY KEY,
    Issued_cust INT NOT NULL,
    Issued_book_isbn VARCHAR(20) NOT NULL,
    Issue_date DATE NOT NULL,
    Due_date DATE NOT NULL,
    Return_date DATE,
    Fine_amount DECIMAL(10,2) DEFAULT 0,
    Issued_by_emp INT,
    FOREIGN KEY (Issued_cust) REFERENCES Customer(Customer_Id) ON DELETE CASCADE,
    FOREIGN KEY (Issued_book_isbn) REFERENCES Books(ISBN) ON DELETE CASCADE,
    FOREIGN KEY (Issued_by_emp) REFERENCES Employee(Emp_id) ON DELETE SET NULL,
    CHECK (Due_date > Issue_date),
    CHECK (Return_date IS NULL OR Return_date >= Issue_date)
);

CREATE TABLE IF NOT EXISTS Reservations (
    Reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    Customer_id INT NOT NULL,
    Book_isbn VARCHAR(20) NOT NULL,
    Reservation_date DATE NOT NULL,
    Status ENUM('Pending', 'Fulfilled', 'Cancelled') DEFAULT 'Pending',
    Notification_sent BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_Id) ON DELETE CASCADE,
    FOREIGN KEY (Book_isbn) REFERENCES Books(ISBN) ON DELETE CASCADE,
    UNIQUE KEY unique_active_reservation (Customer_id, Book_isbn, Status)
);

CREATE TABLE IF NOT EXISTS Fines (
    Fine_id INT AUTO_INCREMENT PRIMARY KEY,
    Customer_id INT NOT NULL,
    Issue_id INT NOT NULL,
    Fine_date DATE NOT NULL,
    Amount DECIMAL(10,2) NOT NULL CHECK (Amount >= 0),
    Paid BOOLEAN DEFAULT FALSE,
    Payment_date DATE,
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_Id) ON DELETE CASCADE,
    FOREIGN KEY (Issue_id) REFERENCES IssueStatus(Issue_Id) ON DELETE CASCADE
);

-- view for available books
CREATE OR REPLACE VIEW Available_Books AS
SELECT ISBN, Book_title, Author, Category, Rental_Price, Publisher, Branch_no, Shelf_location
FROM Books
WHERE Status = 'Available';

-- view for currently issued books
CREATE OR REPLACE VIEW Currently_Issued_Books AS
SELECT i.Issue_Id, i.Issued_cust, c.Customer_name, i.Issued_book_isbn, b.Book_title, 
       i.Issue_date, i.Due_date, i.Fine_amount
FROM IssueStatus i
JOIN Customer c ON i.Issued_cust = c.Customer_Id
JOIN Books b ON i.Issued_book_isbn = b.ISBN
WHERE i.Return_date IS NULL;

-- insert into Branch
INSERT INTO Branch (Branch_name, Manager_id, Branch_address, Contact_no) VALUES
('Central Library', 'M101', '123 Main St, City Center', '555-0101'),
('North Branch', 'M102', '456 North Ave, North District', '555-0102'),
('South Branch', 'M103', '789 South Rd, South District', '555-0103')
ON DUPLICATE KEY UPDATE Branch_name = VALUES(Branch_name);

-- insert data into employee
INSERT INTO Employee (Emp_name, Position, Salary, Hire_date, Branch_no, Email) VALUES
('John Doe', 'Head Librarian', 65000.00, '2020-01-15', 1, 'john.doe@library.com'),
('Jane Smith', 'Assistant Librarian', 48000.00, '2021-03-22', 1, 'jane.smith@library.com'),
('Robert Johnson', 'Library Clerk', 42000.00, '2022-05-10', 2, 'robert.j@library.com'),
('Emily Davis', 'Library Assistant', 38000.00, '2022-08-14', 3, 'emily.d@library.com')
ON DUPLICATE KEY UPDATE Emp_name = VALUES(Emp_name);

-- insert into customer
INSERT INTO Customer (Customer_name, Customer_address, Email, Phone, Reg_date, Membership_type, Membership_expiry) VALUES
('Alice Johnson', '123 Oak St, City Center', 'alice@email.com', '555-1001', '2023-01-15', 'Gold', '2024-01-15'),
('Bob Williams', '456 Pine Rd, North District', 'bob@email.com', '555-1002', '2023-02-20', 'Premium', '2024-02-20'),
('Carol Davis', '789 Elm Ave, South District', 'carol@email.com', '555-1003', '2023-03-10', 'Basic', '2024-03-10'),
('David Brown', '321 Maple St, City Center', 'david@email.com', '555-1004', '2023-04-05', 'Gold', '2024-04-05'),
('Eva Wilson', '654 Cedar Rd, North District', 'eva@email.com', '555-1005', '2023-05-12', 'Premium', '2024-05-12')
ON DUPLICATE KEY UPDATE Customer_name = VALUES(Customer_name);

-- Insert books data BEFORE IssueStatus
INSERT INTO Books (ISBN, Book_title, Category, Rental_Price, Status, Author, Publisher, Published_year, Purchase_date, Purchase_price, Branch_no, Shelf_location) VALUES
('978-0-7432-7356-4', 'The Great Gatsby', 'Fiction', 2.50, 'Issued', 'F. Scott Fitzgerald', 'Scribner', 1925, '2023-01-01', 10.00, 1, 'A1'),
('978-0-312-42743-7', 'The Hobbit', 'Fantasy', 3.00, 'Issued', 'J.R.R. Tolkien', 'Houghton Mifflin', 1937, '2023-01-01', 12.00, 1, 'A2'),
('978-0-618-34625-6', 'The Catcher in the Rye', 'Fiction', 2.50, 'Issued', 'J.D. Salinger', 'Little, Brown and Company', 1951, '2023-01-01', 11.00, 1, 'A3'),
('978-0-06-231500-7', 'The Alchemist', 'Fiction', 2.00, 'Reserved', 'Paulo Coelho', 'HarperCollins', 1988, '2023-01-01', 9.00, 1, 'A4'),
('978-0-7653-2595-7', 'The Name of the Wind', 'Fantasy', 3.50, 'Reserved', 'Patrick Rothfuss', 'DAW Books', 2007, '2023-01-01', 15.00, 1, 'A5')
ON DUPLICATE KEY UPDATE Book_title = VALUES(Book_title);


-- insert into issuestatus
INSERT INTO IssueStatus (Issued_cust, Issued_book_isbn, Issue_date, Due_date, Issued_by_emp) VALUES
(1, '978-0-7432-7356-4', '2023-10-01', '2023-10-15', 1),
(2, '978-0-312-42743-7', '2023-10-05', '2023-10-19', 2),
(3, '978-0-618-34625-6', '2023-10-10', '2023-10-24', 3)
ON DUPLICATE KEY UPDATE Issue_date = VALUES(Issue_date);

-- insert into reservations
INSERT INTO Reservations (Customer_id, Book_isbn, Reservation_date, Status) VALUES
(4, '978-0-06-231500-7', '2023-10-12', 'Pending'),
(5, '978-0-7653-2595-7', '2023-10-13', 'Pending')
ON DUPLICATE KEY UPDATE Reservation_date = VALUES(Reservation_date);

-- insert sample data into fines
INSERT INTO Fines (Customer_id, Issue_id, Fine_date, Amount, Paid) VALUES
(1, 1, '2023-10-16', 2.00, TRUE),
(2, 2, '2023-10-20', 1.00, FALSE)
ON DUPLICATE KEY UPDATE Fine_date = VALUES(Fine_date);



-- books that are currently available
SELECT b.ISBN, b.Book_title, b.Author, b.Category, b.Rental_Price, br.Branch_name, b.Shelf_location
FROM Books b
JOIN Branch br ON b.Branch_no = br.Branch_no
WHERE b.Status = 'Available'
ORDER BY b.Category, b.Book_title;

-- total revenue by branch for the current month
SELECT br.Branch_name, SUM(i.Fine_amount) as Total_Fines, COUNT(i.Issue_Id) as Total_Issues
FROM IssueStatus i
JOIN Books b ON i.Issued_book_isbn = b.ISBN
JOIN Branch br ON b.Branch_no = br.Branch_no
WHERE i.Return_date IS NOT NULL
  AND MONTH(i.Return_date) = MONTH(CURRENT_DATE())
  AND YEAR(i.Return_date) = YEAR(CURRENT_DATE())
GROUP BY br.Branch_name;

-- customers with currently overdue books and their fines
SELECT 
    c.Customer_name, 
    c.Email, 
    c.Phone,
    b.Book_title,
    i.Issue_date,
    i.Due_date,
    DATEDIFF(CURDATE(), i.Due_date) AS Days_Overdue,
    (DATEDIFF(CURDATE(), i.Due_date) * 1.00) AS Calculated_Fine
FROM IssueStatus i
JOIN Customer c ON i.Issued_cust = c.Customer_Id
JOIN Books b ON i.Issued_book_isbn = b.ISBN
WHERE i.Return_date IS NULL 
AND i.Due_date < CURDATE();

-- most popular book categories by branch
SELECT 
    br.Branch_name,
    b.Category,
    COUNT(i.Issue_Id) AS Times_Borrowed
FROM IssueStatus i
JOIN Books b ON i.Issued_book_isbn = b.ISBN
JOIN Branch br ON b.Branch_no = br.Branch_no
WHERE i.Issue_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY br.Branch_name, b.Category
ORDER BY br.Branch_name, Times_Borrowed DESC;

-- employee performance by books issued
SELECT 
    e.Emp_name,
    br.Branch_name,
    COUNT(i.Issue_Id) AS Books_Issued,
    SUM(i.Fine_amount) AS Fines_Collected
FROM IssueStatus i
JOIN Employee e ON i.Issued_by_emp = e.Emp_id
JOIN Branch br ON e.Branch_no = br.Branch_no
WHERE i.Issue_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
GROUP BY e.Emp_id, e.Emp_name, br.Branch_name
ORDER BY Books_Issued DESC;

--  number of data from each table
SELECT 'Branch' AS Table_Name, COUNT(*) AS Row_Count FROM Branch
UNION ALL
SELECT 'Employee', COUNT(*) FROM Employee
UNION ALL
SELECT 'Customer', COUNT(*) FROM Customer
UNION ALL
SELECT 'Books', COUNT(*) FROM Books
UNION ALL
SELECT 'IssueStatus', COUNT(*) FROM IssueStatus
UNION ALL
SELECT 'Reservations', COUNT(*) FROM Reservations
UNION ALL
SELECT 'Fines', COUNT(*) FROM Fines;
