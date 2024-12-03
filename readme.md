# End-to-End Backend Solution with Flask, PostgreSQL, and Object-Oriented Programming  

This project demonstrates a robust and modular backend system designed to integrate multiple technologies and best practices. Below is an overview of the key components and features implemented:

## Features  

### 1️⃣ Flask-Powered Web API  
Utilized Flask to create a web API that efficiently processes user-submitted strings, enabling character search functionality with precision.

### 2️⃣ Robust Logging Mechanism  
Implemented a logging system to record each request in a `.log` file, ensuring comprehensive data capture for troubleshooting and analytics.

### 3️⃣ Data Accessibility  
Designed APIs to retrieve data from two sources:  
- `.log` file for raw request logs  
- PostgreSQL database for structured and persistent storage  

### 4️⃣ Object-Oriented Design  
Adopted Object-Oriented Programming (OOP) principles to modularize the backend code, improving maintainability and scalability. Context managers were utilized to streamline resource handling.  

### 5️⃣ Access Control Implementation  
Implemented user-specific access controls, restricting sensitive endpoints (e.g., `view_log`) to authorized users only, enhancing security.  

---

## Technologies Used  

- **Python** (Flask, logging, contextlib)  
- **PostgreSQL** for database management  
- **OOP Principles** for clean, reusable code  

---

## How to Get Started  

1. Clone the repository:  
   ```bash
   git clone [repository-url]
   cd [repository-folder]
