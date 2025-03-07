# 🎬 MovieDB Management System

## 📌 Project Description
MovieDB Management System is a relational database management system designed to efficiently store, manage, and retrieve movie-related data. It follows best practices in database design, security, and optimization, implementing user roles, indexing, automation, and a graphical user interface.

## 🛠️ Tech Stack
- **Database**: Oracle SQL
- **Backend**: SQL Queries, PL/SQL, Python
- **Frontend**: PyQt5 (GUI Application)
- **Tools**: Git, GitHub, SQL Developer, DBMS_OUTPUT
- **Security**: User Management, Role-based Access Control (RBAC)

## 📂 Features
- **Relational Database Schema**: Structured tables for movies, genres, actors, and roles.
- **Secure User Management**: Admin, Manager, and Regular User roles with different privileges.
- **Optimized Queries**: Indexed searches for fast retrieval of movies, genres, and people.
- **Data Persistence**: Ensures database integrity with foreign keys and constraints.
- **Automated Reports**: Monthly reports on movies added.
- **Triggers & Stored Procedures**: Automated updates and batch processing.
- **Graphical User Interface (GUI)**: Built with PyQt5 for an interactive experience.

## 🚀 Installation & Setup
### Prerequisites
- Oracle Database installed
- SQL Developer or any SQL IDE
- Python 3 and required libraries (`cx_Oracle`, `PyQt5`)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/SiddarthaNanuvala/MovieDB-Management-System.git
   cd MovieDB-Management-System
   ```
2. **Set Up Database**
   - Execute the `schema.sql` file to create tables.
   - Populate tables using the provided SQL scripts.
3. **Configure User Roles**
   - Run `user_management.sql` to create admin and user roles.
4. **Run Queries & Reports**
   - Execute optimization queries and generate reports using stored procedures.
5. **Run GUI Application**
   - Install dependencies:
     ```bash
     pip install cx_Oracle PyQt5
     ```
   - Run the application:
     ```bash
     python GUI_representation.py.py
     ```

## 📝 Usage
- **Retrieve Top Movies**: `SELECT * FROM mv_top_movies;`
- **Check User Access**: `SELECT * FROM DBA_USERS;`
- **Generate Monthly Reports**: `EXEC generate_monthly_report;`
- **Use GUI for Queries**: Interactive search and query execution.


## 📜 License
This project is open-source and available under the **MIT License**.

---

🔹 *Feel free to contribute and enhance the project!* 🚀
