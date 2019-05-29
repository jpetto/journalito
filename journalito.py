# this is the entrypoint to the flask application
from app import create_app, db
from app.models import Post, User


flapp = create_app()


# add the dictionary keys provided to the shell context when running
# `flask shell`
@flapp.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'flapp': flapp,
        'Post': Post,
        'User': User,
    }
