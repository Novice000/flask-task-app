from functools import wraps
from flask import redirect, session
from cs50 import SQL


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

#from cs50 staff
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


#from flask_documentation
def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS)

def get_type(file):
    return file.rsplit('.',1)[1]

            