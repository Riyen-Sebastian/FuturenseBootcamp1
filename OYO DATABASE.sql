create database OYO;
USE OYO;
-- MADE BY ARCHIE
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    user_password VARCHAR(255)
);
-- MADE BY ARCHIE
CREATE TABLE Admins  (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    admin_password VARCHAR(255)
);

-- MADE BY SCHOLAR
CREATE TABLE Hotel (
    HotelID INT PRIMARY KEY,
    HotelName VARCHAR(50) NOT NULL,
    HotelAddress VARCHAR(100) NOT NULL,
    City VARCHAR(30) NOT NULL,
    State VARCHAR(30) NOT NULL,
    Country VARCHAR(30) NOT NULL,
    ZipCode VARCHAR(10) NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL
);
-- MADE BY SCHOLAR
-- Create the Rooms table
CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY,
    HotelID INT NOT NULL,
    RoomType VARCHAR(20) NOT NULL,
    RoomRate DECIMAL(10, 2) NOT NULL,
    IsAvailable BIT NOT NULL,
    FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID)
);



-- made by Riyen
CREATE TABLE Review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
     HotelID INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    complaint TEXT,
    review_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY ( HotelID) REFERENCES Hotel( HotelID)
);
-- made by Riyen
CREATE TABLE Service (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
     HotelID INT,
    service_name VARCHAR(100),
    service_description TEXT,
    price DECIMAL(10, 2),
    FOREIGN KEY ( HotelID) REFERENCES Hotel( HotelID)
);
-- Made By Satyam
CREATE TABLE Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
     HotelID INT,
    employee_name VARCHAR(100),
    employee_role VARCHAR(100),
    contact_info VARCHAR(100),
    FOREIGN KEY ( HotelID) REFERENCES Hotel( HotelID)
);

-- Made by Satyam
CREATE TABLE Service_Employee (
    service_id INT,
    employee_id INT,
    PRIMARY KEY (service_id, employee_id),
    FOREIGN KEY (service_id) REFERENCES Service(service_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);




-- Bookings Table by Yashasvi Singh
CREATE TABLE Bookings (
    booking_id INT PRIMARY KEY ,
    user_id INT,
    RoomID INT,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

-- Payments Table by Yashasvi Singh
CREATE TABLE Payments (
    payment_id INT PRIMARY KEY,
    booking_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50) NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
);

CREATE TABLE Service_Avail (
    service_avail_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    service_id INT NOT NULL,
    booking_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (service_id) REFERENCES Service(service_id),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
);

-- Users
INSERT INTO Users (user_name, email, user_password) VALUES
('John Doe', 'john.doe@example.com', 'password123'),
('Jane Smith', 'jane.smith@example.com', 'qwerty456'),
('Michael Johnson', 'michael.johnson@example.com', 'abc123def'),
('Emily Davis', 'emily.davis@example.com', 'password!@#$'),
('David Wilson', 'david.wilson@example.com', 'securepassword');

-- Admins
INSERT INTO Admins (admin_name, email, admin_password) VALUES
('Admin1', 'admin1@oyo.com', 'admin123'),
('Admin2', 'admin2@oyo.com', 'admin456'),
('Admin3', 'admin3@oyo.com', 'admin789'),
('Admin4', 'admin4@oyo.com', 'admin012'),
('Admin5', 'admin5@oyo.com', 'admin345');

-- Hotel
INSERT INTO Hotel (HotelID, HotelName, HotelAddress, City, State, Country, ZipCode, PhoneNumber) VALUES
(1, 'Grand Palace Hotel', '123 Main St', 'New York', 'New York', 'USA', '10001', '1234567890'),
(2, 'Hilton Luxury Resort', '456 Oak Ave', 'Los Angeles', 'California', 'USA', '90001', '9876543210'),
(3, 'Marriott Beach Resort', '789 Ocean Blvd', 'Miami', 'Florida', 'USA', '33101', '5678901234'),
(4, 'Hyatt Regency', '234 Park Ln', 'Chicago', 'Illinois', 'USA', '60601', '3456789012'),
(5, 'Ritz-Carlton', '567 Maple Rd', 'Boston', 'Massachusetts', 'USA', '02101', '7890123456');

-- Rooms
INSERT INTO Rooms (RoomID, HotelID, RoomType, RoomRate, IsAvailable) VALUES
(101, 1, 'Standard', 100.00, 1),
(102, 1, 'Deluxe', 150.00, 0),
(201, 2, 'Suite', 200.00, 1),
(202, 2, 'Standard', 120.00, 1),
(301, 3, 'Oceanview', 180.00, 0),
(302, 3, 'Deluxe', 160.00, 1),
(401, 4, 'Standard', 110.00, 1),
(402, 4, 'Suite', 220.00, 0),
(501, 5, 'Luxury', 300.00, 1),
(502, 5, 'Deluxe', 180.00, 1);

-- Review
INSERT INTO Review (user_id, HotelID, rating, comment, complaint, review_date) VALUES
(1, 1, 4, 'Great hotel, clean and comfortable rooms.', NULL, '2023-06-01'),
(2, 2, 3, 'Average experience, could be better.', 'Slow service', '2023-05-15'),
(3, 3, 5, 'Excellent beachfront property, highly recommended.', NULL, '2023-06-10'),
(4, 4, 2, 'Disappointing stay, rooms need renovation.', 'Noisy and outdated rooms', '2023-04-20'),
(5, 5, 4, 'Luxurious hotel, great amenities.', 'Expensive parking', '2023-06-05');

-- Service
INSERT INTO Service (HotelID, service_name, service_description, price) VALUES
(1, 'Spa Treatment', 'Relaxing massage and facial services', 100.00),
(2, 'Airport Shuttle', 'Shuttle service to and from the airport', 20.00),
(3, 'Beach Cabana Rental', 'Rent a private cabana on the beach', 75.00),
(4, 'Room Service', 'In-room dining service available 24/7', 5.00),
(5, 'Concierge Services', 'Personal concierge assistance for guests', 50.00);

-- Employee
INSERT INTO Employee (HotelID, employee_name, employee_role, contact_info) VALUES
(1, 'Emily Johnson', 'Front Desk Manager', 'emily.johnson@grandpalace.com'),
(2, 'Michael Smith', 'Housekeeping Supervisor', 'michael.smith@hiltonluxury.com'),
(3, 'Sarah Davis', 'Concierge', 'sarah.davis@marriottbeach.com'),
(4, 'David Wilson', 'Bellhop', 'david.wilson@hyattregency.com'),
(5, 'Jessica Lee', 'Spa Therapist', 'jessica.lee@ritzcarlton.com');

-- Service_Employee
INSERT INTO Service_Employee (service_id, employee_id) VALUES
(1, 5),
(2, 4),
(3, 3),
(4, 2),
(5, 1);

-- Bookings
INSERT INTO Bookings (booking_id, user_id, RoomID, check_in, check_out, status) VALUES
(1, 1, 101, '2023-07-01', '2023-07-05', 'Confirmed'),
(2, 2, 201, '2023-06-15', '2023-06-20', 'Confirmed'),
(3, 3, 301, '2023-08-01', '2023-08-07', 'Pending'),
(4, 4, 401, '2023-07-10', '2023-07-15', 'Cancelled'),
(5, 5, 501, '2023-09-01', '2023-09-05', 'Confirmed');

ALTER TABLE Bookings
ADD COLUMN actual_checkout DATE;

UPDATE Bookings
SET actual_checkout = CASE
                        WHEN booking_id = 1 THEN '2023-07-07' -- Different from check_out
                        WHEN booking_id = 3 THEN '2023-08-09' -- Different from check_out
                        ELSE check_out
                      END;
-- Payments
INSERT INTO Payments (payment_id, booking_id, amount, payment_method) VALUES
(1, 1, 500.00, 'Credit Card'),
(2, 2, 800.00, 'Debit Card'),
(3, 3, 1200.00, 'PayPal'),
(4, 4, 600.00, 'Credit Card'),
(5, 5, 1500.00, 'Bank Transfer');

-- Service_Avail
INSERT INTO Service_Avail (user_id, service_id, booking_id) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(5, 5, 5);

ALTER TABLE Review
MODIFY COLUMN review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE Payments DROP PRIMARY KEY;
ALTER TABLE Payments MODIFY COLUMN  payment_id INT AUTO_INCREMENT PRIMARY KEY;

