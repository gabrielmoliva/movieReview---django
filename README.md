# Movie Review Django API

A Django REST Framework project for managing movies, actors, users, and reviews.  
Includes user registration, login/logout, and endpoints for CRUD operations on movies, actors, and reviews.

## Features

- User registration, login, and logout (session-based authentication)
- Submit and view reviews for movies, including a grade and text
- View all users and their reviews
- Add, list, and retrieve movies and actors
- Add actors to movies

## Requirements

- Python 3.10+
- Django 5.x
- Django REST Framework

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd movieReview-django
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   # source .venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

## API Usage

- **Register:** `POST /register`
- **Login:** `POST /login`
- **Logout:** `POST /logout` (requires session cookie and CSRF token)
- **Get current user:** `GET /me`
- **Movies:**  
  - List: `GET /movies`
  - Add: `POST /movies/add`
  - Detail: `GET /movies/<movie_id>`
  - Add actor: `POST /movies/<movie_id>/addActor/<actor_id>`
- **Actors:**  
  - List: `GET /actors`
  - Add: `POST /actors/add`
- **Reviews:**  
  - Add: `POST /movies/review`
  - By movie: `GET /movies/<movie_id>/reviews`
  - By user: `GET /users/<user_id>/reviews`

## Notes

- All POST/PUT/DELETE requests require a valid session cookie and CSRF token.
- Use tools like Postman or httpie for testing endpoints.
- For session authentication, login first and use the same session for further requests.

---