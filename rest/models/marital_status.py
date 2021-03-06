from db import db
from models.employee import EmployeeModel
from models.mixin import ModelMixin


class MaritalStatusModel(ModelMixin, db.Model):
    __tablename__ = 'marital_status'
    exclude_from_update = ()

    id = db.Column(db.Integer, primary_key=True)
    status_feminine = db.Column(db.String(25), nullable=False)
    status_masculine = db.Column(db.String(25), nullable=False)

    employees = db.relationship(EmployeeModel,
                                backref='marital_status',
                                lazy='joined')

    def __init__(self, status_feminine, status_masculine):
        self.status_feminine = status_feminine
        self.status_masculine = status_masculine

    @classmethod
    def find_all(cls, _):
        return cls.query.order_by('status_feminine').all()
