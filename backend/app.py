from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

# @app.route("/students")
# def get_students():
#     """
#     Route to fetch all students from the database
#     return: Array of student objects
#     """
#     # TODO: replace with your implementation. This is a mock response
#     return jsonify([
#         {'course': 'COMP1531', 'id': 1, 'mark': 85, 'name': 'Alice Zhang'},
#         {'course': 'COMP1531', 'id': 2, 'mark': 72, 'name': 'Bob Smith'}
#     ]), 200

@app.route("/students")
def get_students():
    return jsonify(db.get_all_students()), 200


# @app.route("/students", methods=["POST"])
# def create_student():
#     """
#     Route to create a new student
#     param name: The name of the student (from request body)
#     param course: The course the student is enrolled in (from request body)
#     param mark: The mark the student received (from request body)
#     return: The created student if successful
#     """

#     # Getting the request body - replace with your implementation
#     student_data = request.json

#     pass
@app.route("/students", methods=["POST"])
def create_student():
    data = request.json or {}

    name = data.get("name")
    course = data.get("course")
    mark = data.get("mark")

    if not name or not course:
        return jsonify({"error": "name and course are required"}), 404

    if mark is None or mark == "":
        mark = 0

    try:
        mark = int(mark)
    except (TypeError, ValueError):
        return jsonify({"error": "mark must be an integer"}), 404

    student = db.insert_student(name, course, mark)
    return jsonify(student), 200

# @app.route("/students/<int:student_id>", methods=["PUT"])
# def update_student(student_id):
#     """
#     Route to update student details by id
#     param name: The name of the student (from request body)
#     param course: The course the student is enrolled in (from request body)
#     param mark: The mark the student received (from request body)
#     return: The updated student if successful
#     """
#     pass  # replace with your implementation

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student_data = request.json or {}

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if mark is not None:
        try:
            mark = int(mark)
        except ValueError:
            return jsonify({"error": "mark must be an integer"}), 404

        if mark < 0 or mark > 100:
            return jsonify({"error": "mark must be between 0 and 100"}), 404

    student = db.update_student(student_id, name, course, mark)

    if student is None:
        return jsonify({"error": "student not found"}), 404

    return jsonify(student), 200

# @app.route("/students/<int:student_id>", methods=["DELETE"])
# def delete_student(student_id):
#     """
#     Route to delete student by id
#     return: The deleted student
#     """
#     pass  # replace with your implementation

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    deleted = db.delete_student(student_id)

    if deleted is None:
        return jsonify({"error": "student not found"}), 404

    return jsonify(deleted), 200


# @app.route("/stats")
# def get_stats():
#     """
#     Route to show the stats of all student marks 
#     return: An object with the stats (count, average, min, max)
#     """
#     pass  # replace with your implementation

@app.route("/stats")
def get_stats():
    students = db.get_all_students()

    if len(students) == 0:
        return jsonify({
            "count": 0,
            "average": 0,
            "min": None,
            "max": None,
        }), 200

    marks = [student["mark"] for student in students]

    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks),
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
