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




--made by Riyen
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
--made by Riyen
CREATE TABLE Service (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
     HotelID INT,
    service_name VARCHAR(100),
    service_description TEXT,
    price DECIMAL(10, 2),
    FOREIGN KEY ( HotelID) REFERENCES Hotel( HotelID)
);
--Made By Satyam
CREATE TABLE Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
     HotelID INT,
    employee_name VARCHAR(100),
    employee_role VARCHAR(100),
    contact_info VARCHAR(100),
    FOREIGN KEY ( HotelID) REFERENCES Hotel( HotelID)
);

--Made by Satyam
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
    room_id INT,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
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
