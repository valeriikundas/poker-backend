from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    stack_size = db.Column(db.Integer, default=0)
    position = db.Column(db.Integer)

    table_id = db.Column(db.Integer, db.ForeignKey("table.id"))
    # table = db.relationship("Table", backref=db.backref("players"))

    def __repr__(self):
        return f"Player(id={self.id}, name={self.name}, stack_size={self.stack_size}, position={self.position})"


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)  # todo:remove.not needed

    players = db.relationship("User", backref="table")

    def __repr__(self):
        return f"Table({self.id}, {self.name}, {self.players})"

