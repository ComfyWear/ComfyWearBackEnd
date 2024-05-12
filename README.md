# ComfyWearBackEnd
[![Django CI](https://github.com/ComfyWear/ComfyWearBackEnd/actions/workflows/django.yml/badge.svg)](https://github.com/ComfyWear/ComfyWearBackEnd/actions/workflows/django.yml)
## Technology Stack
- Django REST Framework
- Sqlite3
- Python3.9 or newer
- Other Python libraries and tools in `requirements.txt`

## Installation
Follow these steps to set up the backend environment for ComfyWare:

1. **Clone the Repository**
   - Open your terminal.
   - Clone the repository using Git:
     ```
     git clone https://github.com/ComfyWear/ComfyWearBackEnd.git
     ```
   - Navigate into the cloned directory:
     ```
     cd ComfyWearBackEnd
     ```

2. **Set Up a Virtual Environment (Optional)**
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       venv\Scripts\activate
       ```
     - On MacOS/Linux:
       ```
       source venv/bin/activate
       ```

3. **Install Dependencies**
     ```
     pip install -r requirements.txt
     ```
4. **Environment Variables**
   - Set up your environment variables in `.env` files (This should be a secrets).

## Running the Application
1. **Database Migrations**
   - Before using the application, you need to apply database migrations. Run the following command:
     ```
     python manage.py migrate
     ```

2. **Running Application**
   - After the migration is complete, start the application:
     ```
     python manage.py runserver
     ```

## Testing
   - To run the tests, run the following command:
    ```
    python manage.py test app.tests
    ```


## API Endpoints Document
Example endpoints:
https://documenter.getpostman.com/view/21095095/2sA3Bj7Dax