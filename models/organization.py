from db import db
from models.mixin import ModelsMixin


class OrganizationModel(ModelsMixin, db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    users = db.relationship('UserModel',
                            backref='organization',
                            lazy='dynamic')

    def __init__(self, name, is_active):
        self.name = name
        self.is_active = is_active

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()