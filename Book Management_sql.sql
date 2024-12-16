
CREATE DATABASE Book_management;

Use Book_management;

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    published_year INT,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    genre VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from books;

select title, author
from books
where published_year > 2000;

select * 
from books
order by published_year;

drop database book_management;
