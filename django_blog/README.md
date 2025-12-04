# Django Blog Application

## Overview

This is a fully functional **Django Blog Application** designed for learning and practice purposes.  
The project includes essential blogging functionalities such as creating, reading, updating, and deleting posts, as well as user authentication with registration, login, logout, and profile management.

This project provides hands-on experience with Django development and demonstrates real-world practices in building a web application.

---

## Features

### Blog Functionality
- Create, read, update, and delete blog posts (CRUD)
- Posts are associated with authenticated users
- Timestamps for post creation (`published_date`)

### User Authentication
- **User Registration:** Custom registration form with username and email
- **Login/Logout:** Secure authentication using Django's built-in system
- **Profile Management:** Users can view and update their email
- CSRF protection enabled for all forms
- Passwords securely hashed using Django's default hashing system

### Templates and Styling
- Base HTML template (`base.html`) for consistent layout
- Individual templates for registration, login, and profile pages
- Static files for CSS, JavaScript, and images structured in `blog/static/blog/`

---
