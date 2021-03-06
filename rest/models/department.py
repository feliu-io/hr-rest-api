from sqlalchemy import UniqueConstraint

from db import db
from models.employee import EmployeeModel
from models.mixin import ModelMixin


class DepartmentModel(ModelMixin, db.Model):
    __tablename__ = 'department'
    __table_args__ = (UniqueConstraint('department_name', 'organization_id',
                                       name='department_department_name_'
                                            'organization_id_uindex'),)
    exclude_from_update = ('organization_id', 'is_active')

    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False, index=True)

    employees = db.relationship(EmployeeModel,
                                backref='department',
                                lazy='joined')

    def __init__(self, department_name, organization_id, is_active):
        self.department_name = department_name
        self.organization_id = organization_id
        self.is_active = is_active

    @classmethod
    def find_by_id(cls, _id, user):
        from models.organization import OrganizationModel

        record = cls.query.filter_by(id=_id).first()

        if record:
            if OrganizationModel.find_by_id(record.organization_id, user):
                return record

    @classmethod
    def find_all(cls, user):
        return cls.query.filter_by(organization_id=user.organization_id).all()
