# 'less .flaskenv' to see/create env variables 

from app import app, db
from app.models import User, Post

# decorator registers func as as shell context func
# when 'flask shell' cmd ran, this invoked and items returned are registered in shell session
# FLAKS_APP must be env var in order to run, else NameError
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}

