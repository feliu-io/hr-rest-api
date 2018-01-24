from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models.mixin import ModelsMixin


class AppUserModel(ModelsMixin, db.Model):
    __tablename__ = 'app_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    is_owner = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=True)
    is_super = db.Column(db.Boolean, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           server_default=text("timezone('utc'::text, now())"))
    current_login = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False, index=True)

    def __init__(self, username, password, email, organization_id,
                 is_super=False, is_owner=False, is_active=True):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email
        self.organization_id = organization_id
        self.is_super = is_super
        self.is_owner = is_owner
        self.is_active = is_active

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_organization_id(cls, _id):
        return cls.query.filter_by(organization_id=_id).order_by(cls.id).all()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)
