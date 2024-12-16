Book Management System Using FastAPI

**Introduction**

The Book Management System is a web-based application built with FastAPI. It allows users to manage a collection of books, providing CRUD (Create, Read, Update, Delete) functionality. The application is powered by a MySQL database and follows modern development practices using Pydantic models for validation and SQLAlchemy for database interactions.


**Features**

Core Functionalities

- Add New Books: Users can add books with details such as title, author, published year, genre, and ISBN.
- View All Books : Retrieve a list of all books in the system, displayed with complete details.
- Search by ID : Look up a specific book by its unique ID.
- Update Book Details : Modify existing book information like title, author, or published year.
- Delete Books : Remove books from the database permanently using their ID.


**Data Validation and Security**

- Input validation using Pydantic models ensures data integrity.
- Database interactions are managed using SQLAlchemy, preventing SQL injection attacks.


**Technology Stack**

- Backend
  FastAPI: For building the API endpoints.
  SQLAlchemy: ORM for database interactions.
  Pydantic: For data validation and schema definitions.

- Database
  MySQL: Stores book information in a relational structure.

- Development Environment
  Python 3.8+ required.

**Installation and Setup**

**Prerequisites**
   Python 3.8+
   MySQL Database
   pip package manager

**Steps to Run Locally**
 
1. Clone the repository:

2. Install dependencies:
    pip install fastapi sqlalchemy pymysql uvicorn

4. Set up the database:
   Create a MySQL database named book_management.
   Update the DATABASE_URL in the code to reflect your credentials.

5. Run the application:
    uvicorn main:app --reload

6. Test the functions using POSTMAN
