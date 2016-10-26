"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = :github
        """
    db_cursor = db.session.execute(QUERY, {'github': github})
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])

    return row


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """INSERT INTO Students VALUES (:first_name, :last_name, :github) """
    db.session.execute(QUERY, {'first_name': first_name,
                               'last_name': last_name, 'github': github})
    db.session.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""

    QUERY = """
        SELECT title, description, max_grade
        FROM projects
        WHERE title = :title
        """
    db_cursor = db.session.execute(QUERY, {'title': title})
    row = db_cursor.fetchone()
    print "Title: %s\nDescription: %s\nMaximum Grade: %s" % (row[0], row[1], row[2])    



def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""

    QUERY = """
        SELECT grade
        FROM grades
        WHERE project_title = :title AND student_github = :github
        """
    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title})
    row = db_cursor.fetchone()
    print "%s got this grade: %s for the project %s" % (github, row[0], title)    



def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    
    QUERY = """INSERT INTO Grades (student_github, project_title, grade) 
               VALUES (:github, :title, :grade) """
    db.session.execute(QUERY, {'github': github,
                               'title': title,
                               'grade': grade})
    db.session.commit()
    print "Successfully added grade %s for %s on project %s" % (grade, github, title)


def make_new_project(title, description, max_grade):
    """ Adds a new project to the project table. """

    QUERY = """INSERT INTO Projects (title, description, max_grade) 
               VALUES (:title, :description, :max_grade) """
    db.session.execute(QUERY, {'title': title,
                               'description': description,
                               'max_grade': max_grade})
    db.session.commit()
    print "Successfully added project %s with max_grade %s and description %s" % (title, max_grade, description)



def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            project = args[0]
            get_project_by_title(project)

        elif command == "student_grade":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == "new_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

        elif command == "new_project":
            title = args[0]
            description = ' '.join(args[1:-1])
            max_grade = args[-1]
            make_new_project(title, description, max_grade)

        else:
            if command != "quit":
                print "Invalid Entry. Try again."

if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    db.session.close()
