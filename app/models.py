from . import db

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Message %r>' % self.id
