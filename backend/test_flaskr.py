import os
import unittest
import json
from flask import request
from flask_sqlalchemy import SQLAlchemy

from flaskr import app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            os.environ.get('DB_USER'), 
            os.environ.get('DB_PASS'), 
            'localhost:5432', 
            self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 10)

    def test_404_out_of_bound_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_categories'], 6)

    def test_delete_question(self):
        res = self.client().delete("/questions/34")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 34).one_or_none()
        # If question does not exist
        if question is None:
            self.assertEqual(data['success'], False)
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['message'], "unprocessable")

        # If question exists
        else:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], 34)
            self.assertTrue(data['total_questions'])
            self.assertEqual(question, None)

    def test_delete_invalid_question(self):
        res = self.client().delete("/questions/fhdjjsks")
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")

    def test_create_new_question(self):
        mock_question = {
            'question': 'What is the Capital of Nigeria',
            'answer': 'Abuja',
            'category': '3',
            'difficulty': 1

        }
        res = self.client().post('/questions', json=mock_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_create_question_with_incomplete_data(self):

        mock_question = {
            'question': '',
            'answer': '',
            'category': '3',
            'difficulty': 1
        }

        res = self.client().post('/questions', json=mock_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_405_if_book_creation_not_allowed(self):

        mock_question = {
            'question': 'What is the Capital of Nigeria',
            'answer': 'Abuja',
            'category': '3',
            'difficulty': 1

        }

        res = self.client().post("/questions/1000", json=mock_question)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_questions_by_category(self):

        res = self.client().get("/categories/1/questions")

        data = json.loads(res.data)
        current_category = Category.query.get(1).format()['type']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], current_category)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions_in_category'])
        self.assertTrue(data['total_questions'])

    def test_search_questions(self):
        """Test for searching for a question."""

        mock_search = {
            'searchTerm': 'Who invented Peanut Butter?',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=mock_search)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_invalid_search(self):

        mock_search = {
            'searchTerm': 'asasasasasasas',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=mock_search)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_quiz(self):

        mock_data = {
            'previous_questions': [20, 21],
            'quiz_category': {
                'type': 'Science',
                'id': '1'
            }
        }
        res = self.client().post("/quizzes", json=mock_data)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_play_quiz_with_empty_data(self):
        
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
# Make tests conveniently executable
if __name__ == "__main__":
    unittest.main()
