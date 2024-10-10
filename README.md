# UniSystem

Purpose: The application provides an API for comprehensive management of the university system, enabling administration of students, courses, subjects, and other resources.

### Key features
- **Student management** -> adding, updating and deleting student data
- **Course management** -> info about every course as well as all students that enrolled for that specific course
- **User roles** -> students, professors, admins etc..
- **Authentication** -> for all users of the system

### Technologies

- **FastApi** -> python framework
- **Docker** -> for app containerization
- **JWT** -> (JSON Web Token) for authentication

## :memo: Installation

### Prerequisites
- Python 3.8+
- pip3

To run the application, follow these steps:

1. **Clone the Repository**:
   Clone the repository to your local machine:
   ```bash
   git clone <repo_url>
   cd <project_directory>

2. **Set up environment variables**: Before running the application, you need to create a `.env` file in the root 
   directory of the project. This file should contain the following environment variables:
   - **DATABASE_URL**: The URL for connecting to your PostgreSQL database. For example: `postgresql://username:password@localhost:5432/dbname`
  
   - **DB_USER**: The username for accessing the database. 

   - **DB_PASSWORD**: The password associated with the database user.

   - **DB_PORT**: The port number on which your database is running (default is usually `5432` for PostgreSQL).

      #### Example `.env` File
   
      Here is an example of how your `.env` file should look:
   
      ```env
      DATABASE_URL=postgresql://your_user:your_password@localhost:5432/your_database
      DB_USER=your_user
      DB_PASSWORD=your_password
      DB_PORT=5432
  
3. **Create virtual environment**: Run the following command to create a virtual environment named venv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

4. **Installing all required dependencies**
   ```bash
   pip install -r requirements.txt

5. **Run the app**
   ```bash
   python3 app/run.py

#### Note: if your app have trouble finding app module run this command:
   ```bash
   export PYTHONPATH=<absolute path to your project>
   python3 app/run.py
   ```

### Project structure:

```markdown
AdvanceFastapi/
│
├── app/
│   ├── __init__.py
│   ├── run.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── custom_exceptions.py
│   │   ├── services.py
│   │   ├── session.py
│   │   └── base.py
│   ├── api/
│   │   ├── Course/
│   │   └── Student/
│   ├── models/
│   │   ├── course.py
│   │   ├── student.py
│   │   └── __init__.py
│   └── schemas/
│
├── requirements.txt
├── requirements.lock
├── Dockerfile
└── README.md
```