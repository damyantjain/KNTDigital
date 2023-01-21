from kntdigital import db


class action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actionName = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Action('{self.id}', '{self.actionName}')"
