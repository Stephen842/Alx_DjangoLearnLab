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

## Blog Post Management (CRUD)

This section of the Django blog project implements **full CRUD functionality** for blog posts, allowing authenticated users to create, edit, and delete their posts while providing all users the ability to read and browse posts.

### Features

- **Create Post**  
  Authenticated users can create new posts. The author is automatically set to the currently logged-in user.

- **Read / List Posts**  
  All users can view a list of posts. Each post displays the title, author, published date, and a snippet of content. Pagination is supported for easy navigation.

- **View Post Details**  
  Users can view the full content of a single post, including metadata such as author and publication date.

- **Update Post**  
  Only the author of a post can edit it. Update operations are handled securely using Django’s `LoginRequiredMixin` and `UserPassesTestMixin`.

- **Delete Post**  
  Only the author of a post can delete it. Users are prompted for confirmation before deletion.

- **Permissions & Security**  
  - Creation, updating, and deletion are restricted to authenticated users and post authors.  
  - List and detail views are publicly accessible.  
  - Unauthorized attempts to edit or delete posts by non-authors result in a `403 Forbidden` response.

### Implementation Details

- **Models**  
  `Post` model contains `title`, `content`, `published_date`, and `author`. The `get_absolute_url` method is used for redirects after creation or updating.

- **Forms**  
  `PostForm` is a `ModelForm` that handles post creation and updating, with TailwindCSS classes applied for clean styling.

- **Views**  
  Class-based views (CBVs) are used:  
  - `PostListView` — displays all posts  
  - `PostDetailView` — shows a single post  
  - `PostCreateView` — create a post  
  - `PostUpdateView` — edit a post  
  - `PostDeleteView` — delete a post  

- **Templates**  
  TailwindCSS is used to style all post templates, ensuring a professional and responsive UI. Templates include:  
  - `post_list.html` — listing all posts  
  - `post_detail.html` — single post view  
  - `post_form.html` — create/update form  
  - `post_confirm_delete.html` — delete confirmation  

- **URLs**  
  Routes for CRUD operations are intuitive:  
  /                 → Post list - Landing Page
  /posts/<pk>/      → Post detail
  /posts/new/       → Create post
  /posts/<pk>/edit/ → Edit post
  /posts/<pk>/delete/ → Delete post

- **Usage**  
- Login to create a new post.
- Browse the homepage to view all posts.
- Click a post title to view its details.
- Edit or delete your own posts via the links on the post detail or list pages.
- Pagination is automatically applied if there are many posts.