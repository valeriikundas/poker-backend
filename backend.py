from app import db, create_app
from app import socketio
from app.models import User, Table

# import threading


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
