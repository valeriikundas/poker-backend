from app import create_app, db
from app.models import User, Table

from app import socketio

# import threading
from app.main.sockets import start_games


app = create_app()


# threading.Thread(target=start_games).start()
# exit(0)

# FIXME: uncomment and make it work
# start_games()

# socketio.start_background_tasks(target)

if __name__ == "__main__":
    # socketio.start_background_task(start_games)
    socketio.run(app, debug=True)
    # app.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Table": Table}
