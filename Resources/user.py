# Import Flask Rest Full.
from flask_restful import Resource, reqparse
from Model.usermodel import UserModel


# User class must inherit Resource to implement Post Methods .
class UserRegister(Resource):
    # create a parser.
    register_parser = reqparse.RequestParser( )
    # add arguments
    register_parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    register_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    register_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")

    # post method .
    @staticmethod
    def post():
        # get data from json.
        input_data = UserRegister.register_parser.parse_args( )
        # corresponding user exist in database
        if UserModel.find_user(input_data['email_id']) is None:
            # create user.
            user = UserModel(**input_data)
            # save user.
            user.save_data( )
            return {'message': 'user created ', 'Success_Code': 1}, 201
        else:
            return {'message': 'user already present with the email id', 'Success_Code': 0}, 400


# UserSignUp class must inherit Resource to implement Post Methods .
class UserLogin(Resource):
    # create a parser.
    login_parser = reqparse.RequestParser( )
    # add arguments
    login_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    login_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")

    # post method .
    @staticmethod
    def post():
        # get data from json.
        input_data = UserLogin.login_parser.parse_args( )
        # corresponding user exist in database
        user = UserModel.find_user(input_data['email_id'])
        if user is not None:
            print('user found progressing for password check')
            # we need to check for the password .
            if user.check_password(user.password, UserModel.set_password(input_data['password'])):
                # Mark user as a logged in .
                user.user_logged_in(True)
                # return success .
                return {'user': user.json(), 'Login': 'Success', 'Success_Code': 1}, 200
            else:
                return {'Login': 'UnSuccessful wrong password . ', 'Success_Code': 0}, 404
        else:
            return {'Login': 'UnSuccessful no user found with this email id .', 'Success_Code': 0}, 404


# class for Getting all log in user at this instance .
class LoginUserList(Resource):
    @classmethod
    def get(cls):
        return UserModel.find_users_logged_in( )


# check user exist.
class FindUser(Resource):
    # create a parser.
    Find_user_parser = reqparse.RequestParser( )
    # add arguments
    Find_user_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")

    @classmethod
    def post(cls):
        # get data from json.
        input_data = FindUser.Find_user_parser.parse_args( )
        # corresponding user exist in database
        user = UserModel.find_user(input_data['email_id'])
        # if user null return error .
        if user is None:
            return {'message': 'No user found with this email id', 'Success_Code': 0}, 404
        else:
            return {'message': 'User found', 'Success_Code': 1}, 200


# update user password.
class UpdateUser(Resource):
    # create a parser.
    update_user_parser = reqparse.RequestParser( )
    # add arguments
    update_user_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")
    update_user_parser.add_argument('new_password', type=str, required=True, help="This field cannot be blank.")

    @classmethod
    def post(cls):
        # input data.
        input_data = UpdateUser.update_user_parser.parse_args( )
        # get user with email id .
        user = UserModel.find_user(input_data['email_id'])
        # update user password
        user.password = UserModel.set_password(input_data['new_password'])
        # save it in data base.
        user.save_data( )
        return {'message': 'User password updated', 'Success_Code': 1}, 200


# Log out user .
class Logout(Resource):
    # create a parser.
    logout_user_parser = reqparse.RequestParser()
    logout_user_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")

    @classmethod
    def post(cls):
        # input data.
        input_data = Logout.logout_user_parser.parse_args( )
        # get user with email id .
        user = UserModel.find_user(input_data['email_id'])
        # if user is not none .
        if user is not None:
            user.logged_in = False
            user.save_data()
            return {'message': 'User Logged out . ', 'Success_Code': 1}, 200
        else:
            return {'message': 'User not Logged out . ', 'Success_Code': 0}, 404
