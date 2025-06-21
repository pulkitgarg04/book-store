# Bookstore Web Application

![LICENSE](https://img.shields.io/badge/LICENSE-MIT-blue) ![Built with](https://img.shields.io/badge/Built_with-Flask-red)

![book-store](https://socialify.git.ci/pulkitgarg04/book-store/image?custom_language=Python&language=1&name=1&owner=1&theme=Dark)

A simple Flask-based web application to browse books, add them to a cart, and view the cart. This project features a clean UI with support for book images, uses a SQLite database, and Flask-Session for managing user sessions.

## Features
- **Books Page**: View a list of books with images, titles, and authors.
- **Cart Functionality**: Add books to a cart and view them in a dedicated cart page.
- **Database**: Uses `SQLite` for storing book details.
- **Session Management**: `Flask-Session` is used for persistent cart data.

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS (with a responsive grid layout)
- **Session Management**: Flask-Session
- **Virtual Environment**: Python venv

## Getting Started
1. Prerequisites
- Python 3.8+ installed on your machine.
- SQLite installed (if not already included with Python).

2. Clone the Repository
    ```bash
    git clone https://github.com/pulkitgarg04/book-store
    cd book-store
    ```

3. Create and Activate Virtual Environment
    1. Create the virtual environment:
        ```bash
        python3 -m venv venv
        ```

    2. Activate the virtual environment:
        ```bash
        source venv/bin/activate
        ```

4. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```

5. Initialize the Database
    - Run the `init_db.py` script to set up the database and populate it with sample data:

        ```bash
        python init_db.py
        ```

6. Run the Application
    - Start the Flask server:
        ```bash
        python app.py
        ```

7. The application will be accessible at:
    ```
    http://127.0.0.1:5000/
    ```

## Contributing
Contributions are welcome! If you encounter any issues or have suggestions, feel free to open an issue or submit a pull request.


## License
This project is licensed under the MIT [License](LICENSE). You are free to use, modify, and distribute this project.