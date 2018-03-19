from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.user import AppUserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True)
    parser.add_argument('password',
                        type=str,
                        required=True)
    parser.add_argument('email',
                        type=str,
                        required=True)
    parser.add_argument('is_super',
                        default=False,
                        type=bool,
                        required=False)
    parser.add_argument('is_owner',
                        default=False,
                        type=bool,
                        required=False)
    parser.add_argument('is_active',
                        default=True,
                        type=bool,
                        required=False)
    parser.add_argument('organization_id',
                        type=int,
                        required=True)

    @jwt_required()
    def get(self, username):
        user = AppUserModel.find_by_username(username)
        if user:
            return user.to_dict()

        return {'message': 'User not found.'}, 404

    @staticmethod
    @jwt_required()
    def post():
        data = User.parser.parse_args()

        if AppUserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400

        if (current_identity.organization_id == data['organization_id'] and
                current_identity.is_owner) or current_identity.is_super:
            user = AppUserModel(**data)

            try:
                user.save_to_db()
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while creating '
                                   'the user.'}, 500

            return {
                       'message': 'User created successfully.',
                       'user': AppUserModel.find_by_id(
                           user.id
                       ).to_dict()
                   }, 201

        return {'message': 'You are not allowed to create users in your '
                           'organization.'}, 403

    @jwt_required()
    def put(self, username):
        data = User.parser.parse_args()

        user = AppUserModel.find_by_username(username)

        if user:
            try:
                _, user = user.update(data, ('is_active', 'organization_id'))
                return {
                           'message': 'User updated successfully.',
                           'user': user.to_dict()
                       }, 200
            except exc.SQLAlchemyError:
                return {'message': 'An error occurred while updating '
                                   'the user.'}, 500

        return {'message': 'User not found.'}, 404

    @jwt_required()
    def delete(self, username):
        user = AppUserModel.find_by_username(username)

        if user:
            if user.is_active:
                try:
                    user.inactivate()
                    return {'message': 'User is now inactive.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while inactivating'
                                       'the user.'}, 500
            else:
                return {'message': 'User was already inactive.'}, 400

        return {'message': 'User not found.'}, 404


class ActivateUser(Resource):
    @jwt_required()
    def put(self, username):
        user = AppUserModel.find_by_username(username)

        if user:
            if not user.is_active:
                try:
                    user.activate()
                    return {'message': 'User is now active.'}, 200
                except exc.SQLAlchemyError:
                    return {'message': 'An error occurred while activating'
                                       'the user.'}, 500
            else:
                return {'message': 'User was already active.'}, 400
        else:
            return {'message': 'User not found.'}, 404
