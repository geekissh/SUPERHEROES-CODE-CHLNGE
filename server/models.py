from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'super_name': self.super_name}

    def to_dict_with_powers(self):
        return {'id': self.id, 'name': self.name, 'super_name': self.super_name, 'hero_powers': [hp.to_dict() for hp in self.hero_powers.all()]}

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete='CASCADE'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete='CASCADE'))

    def to_dict(self):
        return {'id': self.id, 'strength': self.strength, 'hero_id': self.hero_id, 'power_id': self.power_id}
