create database OYO;
USE OYO;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    user_password VARCHAR(255)
);

CREATE TABLE Admins  (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    admin_password VARCHAR(255)
);

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

--made by Riyen
CREATE TABLE Service_Employee (
    service_id INT,
    employee_id INT,
    PRIMARY KEY (service_id, employee_id),
    FOREIGN KEY (service_id) REFERENCES Service(service_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);
