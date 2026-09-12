# Blog Application (Django)

A simple blog platform where users can register, log in, and manage their own blog posts.

## Features

### Core
- **User Authentication**: Registration, login, logout (Django's built-in auth system)
- **Blog Post CRUD**: Authenticated users can create, view, update, and delete posts
- **Ownership Protection**: Users can only edit/delete their *own* posts. Other users can view but not modify someone else's post.
- **Pages**: Home (all posts), Post Detail, Register, Login, Create Post, Edit Post, Delete Confirmation, My Posts
- Pagination on the home page and a responsive Bootstrap layout

### Bonus features implemented
- **Categories + filtering**: posts can be tagged with a category and filtered from the home page (`?category=<id>`). Manage categories from `/admin/`.
- **Search**: search posts by title/content from the home page (`?q=...`).
- **Post image upload**: optional image field on posts, shown on the home page and detail page (requires Pillow).
- **Comments**: authenticated users can comment on any post; comments show under the post detail page.
- **Like system**: authenticated users can like/unlike a post; like counts show on the home page and post detail page.

## Tech Stack

- Python 3
- Django 6.1
- SQLite (default Django DB)
- Django Templates + Django Forms
- Bootstrap 5 (via CDN) for styling
- Pillow (for image uploads)

## Project Structure

```
blog-project/
├── blog/               # Blog app: BlogPost model, CRUD views, forms
├── users/              # Users app: registration, login/logout routing
├── blogproject/        # Project settings, root urls
├── templates/          # HTML templates (base, blog/, users/)
├── static/css/         # Custom CSS
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd blog-project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **(Optional) Create a superuser to access /admin/**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000/` in your browser.

## App Routes

| URL | Description | Auth required |
|---|---|---|
| `/` | Home page, lists all posts | No |
| `/post/<id>/` | View a single post | No |
| `/post/new/` | Create a new post | Yes |
| `/post/<id>/edit/` | Edit a post (owner only) | Yes |
| `/post/<id>/delete/` | Delete a post (owner only) | Yes |
| `/my-posts/` | View your own posts | Yes |
| `/register/` | Create an account | No |
| `/login/` | Log in | No |
| `/logout/` | Log out | Yes |
| `/admin/` | Django admin | Superuser |

## Ownership Enforcement

The `PostUpdateView` and `PostDeleteView` use an `OwnerRequiredMixin` (`UserPassesTestMixin`) that checks `post.author == request.user`. Anyone who is not the post's author is redirected back to the post detail page with an error message, and cannot submit edits or deletions even by directly POSTing to the URL.

## Notes

- This submission covers all **required features** plus 5 bonus features (categories/filtering, search, post images, comments, likes). Remaining bonus features (profile page, profile picture, draft/published status) were left out due to time constraints.
- `db.sqlite3`, `.env`, and uploaded `media/` files are git-ignored; run `migrate` to generate a fresh local database. To add categories, log into `/admin/` with a superuser account and create them there (no dedicated UI page was built for managing categories, since it wasn't required by the assignment).
