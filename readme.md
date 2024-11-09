# MOTIVE: Goal Sharing Web App

**MOTIVE** is a goal-sharing web application designed to help users set, share, and track personal goals. The app allows users to post goals, mark them as achieved, and view others' achievements, providing a shared space for mutual inspiration and accountability. Randomly generated motivational quotes further encourage users on their goal journeys.

## Features

- **Goal Posting and Sharing**: Post your own goals, and see a community-wide archive of goals to get inspired by others’ achievements.
- **Goal Tracking**: Mark goals as achieved, and let others acknowledge the same by marking those goals achieved if they share similar goals.
- **User Authentication**: Register, log in, and manage your profile, including a profile photo.
- **Pagination and Search**: View goals with paginated tables and search functionality to find specific goals.
- **Random Motivation**: Get randomly generated motivational quotes on each page to stay inspired.

## Files/Folders

### Template Folder

The templates folder contains the HTML files that define the structure of each page.

- **`layout.html`**: The base layout for all pages, featuring:
  - Bootstrap styling and JavaScript for responsive design.
  - A customizable navbar with links to different pages, including a dropdown menu that adapts based on user login status.
  - Template blocks for `title` and `main` content, allowing child templates to insert their page-specific content.
  - JavaScript to enable tooltips for an enhanced user experience.

- **`index.html`**: 
  - Displays the main archive of all user-posted goals, where users can view and add goals to their own achievement list.
  - Contains a search bar for filtering goals by name, pagination controls, and randomly generated motivational quotes.
  - Allows users to add new goals directly from the homepage.

- **`login.html`**: 
  - Provides a login form with fields for username and password.
  - Redirects users here if they attempt to access restricted pages without logging in.
  - Displays motivational quotes for encouragement.

- **`profile.html`**:
  - A user-specific profile page, showing the user’s profile photo, username, and a personal list of goals.
  - Lists all goals posted by the user, with options to mark them as achieved, remove them, or delete them entirely.
  - Contains pagination and randomly generated motivational quotes, along with a form to add new goals.

- **`register.html`**: 
  - Contains a registration form with input fields for username, password, password confirmation, and profile photo upload.
  - Motivational quotes are displayed to encourage new users during the registration process.

- **`error.html`**: 
  - A simple error page that uses Jinja templating to display user-friendly error messages and allows users to return to the previous page.

### Static Folder

- **`style.css`**: Custom CSS for the project, defining styles for pagination links, background color, and other elements across all pages.
- **Image Folder**: Stores user-uploaded profile pictures and any other images used in the project.

### Database (`motive.db`)

The application uses SQLite for all data storage needs. The database includes several tables:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY NOT NULL,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    gender TEXT
);

CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal TEXT NOT NULL,
    status TEXT,
    date_added DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE attained (
    goal_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (goal_id) REFERENCES goals (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT goal_user UNIQUE (goal_id, user_id)
);

CREATE TABLE quotes (
    id INTEGER PRIMARY KEY,
    author TEXT,
    quote TEXT NOT NULL
);
```

### Python Files

- **`app.py`**: The main Flask application file, containing all view functions and routes for login, logout, registration, goal posting, deletion, and more. It is the central script managing user interaction and database transactions.
  
- **`helper.py`**: Contains helper functions, including:
  - **`login_required`**: A decorator provided by CS50 staff to restrict access to certain routes for logged-in users only.
  - **`allowed_file`**: A function from the Flask documentation to validate uploaded file types.
  - **`get_type`**: A utility to detect file types for uploads.

### `requirements.txt`

A list of all dependencies for the project, which can be installed by running:
```bash
pip install -r requirements.txt
```

### Future Improvements

While the current version of **MOTIVE** is functional, there are several enhancements I plan to implement:
- **Enhanced Notifications**: Notifications for when others achieve goals you've set.
- **Goal Categories**: Categorize goals for better organization.
- **Improved UX**: Additional features to improve user engagement and ease of navigation.

## Acknowledgments

This project includes foundational code provided by the CS50 staff, specifically for the login-required functionality and guidance on structuring a web application with Flask. Custom features and design choices, including Bootstrap styling and additional functionalities, were added based on my own preferences.

## License

This project is licensed under the MIT License. Please follow CS50’s [academic honesty policy](https://cs50.harvard.edu/x/2023/honesty/) if referencing or using parts of this code for academic or project purposes.
