# Project Name

## Description
A brief description of the project, its purpose, and key features.

## Prerequisites
Make sure you have the following installed before running the project:
- [Python](https://www.python.org/downloads/) (if applicable)
- [pip](https://pip.pypa.io/en/stable/)
- Other dependencies listed in `requirements.txt`

## Setting Up the Environment

### Creating a `.env` File
1. Create a `.env` file in the root directory of the project.
2. Add the required environment variables in the following format:

   ```
   SQLALCHEMY_DATABASE_URI = ''
   SECRET_KEY = ''
   SEND_GRID_API_CLIENT = ''
   MONGO_CONN_URL = ''
   ```

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/mihajlovoleg/clone_forbes_project
   cd clone_forbes_project
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python run.py
   ```

## Running the App
- Start the app with:
  ```sh
  python run.py
  ```
- Access the application at `http://localhost:5000` (or specified port)



