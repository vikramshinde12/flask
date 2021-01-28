from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"ItemModel(name:{self.name}, items: {self.items})"

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        item = cls.query.filter_by(name=name).first()
        return item

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(f'error:: {e}')

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
