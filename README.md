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
     This going to take some time when you do the first prediction (It is downloading the model's weights).

## Testing
   - To run the tests, read the "Note" section below and run the following command:
    ```
    python manage.py test app.tests
    ```


## API Endpoints Document
Example endpoints:
https://documenter.getpostman.com/view/21095095/2sA3Bj7Dax

## Note
To reduce the memory needed to store the source code, we remove all of the model's weights and let it download when we first predict things in the application. (This is the problem we faced when trying to upload the source code into ecourse).

This might cause the tests to fail until you download all of the model's weight. In case the test is failed (it shouldn't), there are 2 ways you can automatically download the model's weight
- Run `ComfyWareFrontEnd` with `ComfyWareBackEnd` and try to send the image (Just use the application like usual).
- Or, run only `ComfyWareBackEnd` and do the post request to `app/api/predict/`. This will download all of the model's weights from Onedrive.

After you get all of the model's weights. You can test the application using the above instructions.