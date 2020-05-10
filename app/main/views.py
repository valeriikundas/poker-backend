from app.main import blp


@blp.route("/")
def index():
    return "hello world"
