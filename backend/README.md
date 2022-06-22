# Trivia API

## Description
Trivia api is a web application that allows people to hold trivia on a regular basis using a webpage to manage the trivia app and play the game.

The application does the following:

1. **Display questions** - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. **Delete questions**
3. **Add questions** and require that they include question and answer text.
4. **Search** for questions based on a text query string.
5. **Play the quiz game**, randomizing either all questions or within a specific category.

## Getting Started
### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
create database trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql -U <username> trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```json
drop database trivia_test
create database trivia_test
psql -U <username> trivia_test < trivia.psql
python test_flaskr.py
```

## Setting up Frontend 
The frontend app was built using create-react-app. You can change the script in the package.json file.

Navigate to the frontend directory and install the npm package if you haven't 

```javascript
npm install
```
In order to run the app in development mode, use
```javascript
npm start
```
Open `http://localhost:3000` to view it in the browser. The page will reload if you make edits.

## API Reference
### Getting Started
 - Backend Base URL: `http://127.0.0.1:5000/`
 - Frontend Base URL: `http://127.0.0.1:3000/`
 - Authentication: No Authentication or API keys used in the project yet.

### Error Handling
Errors are returned in the following json format:
```json
    {
        "success": "False",
        "error": 404,
        "message": "resource not found",
      }
```
The error codes currently returned are:
  *  400 – *bad request*
  *  404 – *resource not found*
  *  405 – *method not allowed*
  *  422 – *unprocessable*
 
 ## Endpoints

### **1. Categories**
### `GET '/categories'`

- Returns a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

> **Sample:** `curl http://127.0.0.1:5000/categories`
```json
 {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_categories": 6
}

```
### **2. Questions**
### `GET '/questions'`

- Returns all questions 
- Questions are paginated (i.e 10 questions per page)
- Other pages could be requested by a query string ```curl http://127.0.0.1:5000/questions?page=2```
- Total questions found are also displayed 

 > **Sample:** `curl http://127.0.0.1:5000/questions`
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": " ",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 23
}


```
### **3. Delete a question**
### `DELETE '/questions/<int:question_id>'`

- Permanently removes a question by id passed through the ur; 

> **Sample** `curl http://127.0.0.1:5000/questions/6 -X DELETE`
```json
    {
        "success":true,
        "deleted":6,
    }

```
### **4. Create Question**
### `POST '/questions'`

- Creates a new question

>  **Sample:** `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "What is the Capital of Lagos?", "answer": "Ikeja", "difficulty": 2, "category": "3" }'`
```json
    {
        "success":true,
        "deleted":"Question has been added!",
    }

```
### **5. Search** 
### `POST '/questions/search'`

- All questions that contains the search substring are returned

> **Sample:** `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Africa"}'`

```json
    
{
    "questions": [
        {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
        }
    ],
    "success": true,
    "total_questions": 1
}


```

### **6. Get questions by category**

### `GET 'categories/<int:category_id>/questions'`

- Returns all questions by category using the category_id from the url parameter

> **Sample:** `curl http://127.0.0.1:5000/categories/3/questions`
```json
{
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "6",
      "category": 3,
      "difficulty": 1,
      "id": 29,
      "question": "What is my house name?"
    }
  ],
  "success": true,
  "total_questions": 23,
  "total_questions_in_category": 4
}
```
### **7. Play Quiz**
### `POST '/quizzes'`
- Takes the category and previous questions in the request.
- Return random question not in previous questions.

> **Sample:** `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [16, 18], "quiz_category": {"type": "Art", "id": "2"}}'`

```json
{
  "question": {
    "answer": "Mona Lisa",
    "category": 2,
    "difficulty": 3,
    "id": 17,
    "question": "La Giaconda is better known as what?"
  },
  "success": true
}
```

## Authors
**Oluseyi Olaleye** implemented the API and testing.

**Udacity** provided the starter files for the project.



