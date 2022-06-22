import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# create and configure the app
app = Flask(__name__)
setup_db(app)


"""
@TODO: Set up CORS. Allow '*' for origins.
Delete the sample route after completing the TODOs
"""
CORS(app, resources={'/': {'origins': '*'}})

# PAGINATE QUESTIONS


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


"""
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response


"""
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """


@app.route('/categories')
def retrieve_categories():
    try:
        selection = Category.query.order_by(Category.id).all()
        categories = {category.id: category.type for category in selection}

        if len(categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': len(Category.query.all())
        }), 200
    except:
        abort(404)


"""
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.


    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """


@app.route('/questions')
def retrieve_questions():

    try:

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        all_categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            category.id: category.type for category in all_categories}
        print(formatted_categories)
        if len(current_questions) == 0:
            abort(404)
        else:

            return jsonify({
                'success': True,
                'questions': current_questions,
                'categories': formatted_categories,
                'total_questions': len(Question.query.all()),
                'current_category': " "
            }), 200
    except:
        abort(404)


"""

    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """


@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        else:
            question.delete()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
        })
    except:
        abort(422)


"""
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the
    end of the last page of the questions list in the "List" tab.
    """


@app.route('/questions', methods=['POST'])
def create_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    if (new_question == '') or (new_answer == '') or (new_category == '') or (new_difficulty == ''):
        abort(422)
    try:
        question = Question(question=new_question, answer=new_answer,
                            category=new_category, difficulty=new_difficulty)
        question.insert()

        return jsonify({
            'success': True,
            'message': 'Question has been added!'
        }), 201
    except:
        abort(422)


"""
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """


@app.route("/questions/search", methods=['POST'])
def search_questions():
    data = request.get_json()
    search_term = data.get('searchTerm', None)

    try:
        search_result = Question.query.filter(
            Question.question.ilike('%'+search_term+'%')).all()
        formatted_result = [search.format() for search in search_result]
        if len(search_result) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': formatted_result,
            'total_questions': len(search_result)

        }), 200
    except:
        abort(404)


"""
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """


@app.route("/categories/<int:id>/questions")
def get_category_questions(id):

    category = Category.query.filter(Category.id == id).one_or_none()

    if category is None:
        abort(422)

    get_questions = Question.query.filter(
        Question.category == str(id)).order_by(Question.id).all()
    paginated_questions = paginate_questions(request, get_questions)
    return jsonify({
        'success': True,
        'questions': paginated_questions,
        'current_category': category.type,
        'total_questions_in_category': len(get_questions),
        'total_questions': len(Question.query.all())
    })


"""
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """


@app.route('/quizzes', methods=['POST'])
def start_quiz():
    try:

        data = request.get_json()
        quiz_category = data.get('quiz_category')
        previous_questions = data.get('previous_questions')
        if ((quiz_category is None) or (previous_questions is None)):
            abort(400)

        # Get questions from the category selected
        if(int(quiz_category['id']) > 0):
            questions = Question.query.filter_by(
                category=quiz_category['id']).all()
        else:
            questions = Question.query.all()

        # Get a random question

        question = random.choice(questions)

        check = True

        # Ensure that should not get repeated in the quiz.
        while check:
            if question.id in previous_questions:
                # Criteria to end the quiz
                if len(questions) == len(previous_questions):
                    break
                question = random.choice(questions)
            else:
                check = False

        return jsonify({
            'success': True,
            'question': question.format(),
        }), 200

    except:
        abort(400)


"""
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found',
    }), 404


@app.errorhandler(422)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable',
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request',
    }), 400


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500
