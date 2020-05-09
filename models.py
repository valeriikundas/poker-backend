import mongoengine as me
import simplejson as json


class Player(me.Document):
    username = me.StringField(required=True)
    stack_size = me.IntField(default=0)
    position = me.IntField(min_value=0, max_value=8)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):

        return super().save(*args, **kwargs)


class Table(me.Document):
    name = me.StringField(required=True)
    players = me.ListField(me.ReferenceField(Player), default=list)

    def as_json(self):
        return json.dumps(
            {
                "id": self.name,
                "button_position": "TODO:",
                "blinds": {"small": 10, "big": 20, "ante": 2},
                "players": [
                    {
                        "username": p.username,
                        "stack_size": p.stack_size,
                        "position": p.position,
                    }
                    for p in self.players
                ],
            }
        )
