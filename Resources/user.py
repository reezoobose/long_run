# <editor-fold desc="Import .">
# -*- coding: utf-8 -*-
# Import Flask Rest Full.
from flask_restful import Resource, reqparse
from Model.usermodel import UserModel
# </editor-fold>


# <editor-fold desc="User Registration .">
# User class must inherit Resource to implement Post Methods .
class UserRegister(Resource):
    """
    Register an user to a database if user do not present with the email address.
    """
    # create a parser.
    register_parser = reqparse.RequestParser( )
    # add arguments
    register_parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    register_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    register_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")
    register_parser.add_argument('us_dollar', type=str, required=True, help="This field cannot be blank.")
    register_parser.add_argument('device_id', type=str, required=True, help="This field cannot be blank.")

    # post method .
    @staticmethod
    def post():
        """
        Post Method for user registration.
        :return: Success code 1 on successful registration .
        """
        # get data from json.
        input_data = UserRegister.register_parser.parse_args( )
        # corresponding user exist in database
        if UserModel.find_user(input_data['email_id']) is None:
            # create user.
            user = UserModel(input_data['username'],
                             input_data['email_id'],
                             input_data['password'],
                             int(input_data['us_dollar']),
                             input_data['device_id'],
                            )
            # save user.
            user.save_data()
            return {'message': 'user created ', 'Success_Code': 1}, 201
        else:
            return {'message': 'user already present with the email id', 'Success_Code': 0}, 400
# </editor-fold>


# <editor-fold desc="User Login .">
# UserSignUp class must inherit Resource to implement Post Methods .
class UserLogin(Resource):
    """
    Check user login with email address and password .
    """
    # create a parser.
    login_parser = reqparse.RequestParser()
    # add arguments
    login_parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    login_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")

    # post method .
    @staticmethod
    def post():
        """
        Post method for user login .
        :return: Success code 1 on successful login  .
        """
        # get data from json.
        input_data = UserLogin.login_parser.parse_args( )
        # corresponding user exist in database
        user = UserModel.find_user(input_data['email_id'])
        if user is not None:
            # print('user found progressing for password check')
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
# </editor-fold>


# <editor-fold desc="Logged in user List .">
# class for Getting all log in user at this instance .
class LoginUserList(Resource):
    """
    Get User Log In List .
    """
    @classmethod
    def get(cls):
        """
        Get Method .
        :return: Users List those who are currently logged in .
        """
        return UserModel.find_users_logged_in()
# </editor-fold>


# <editor-fold desc="Find User With a mail id .">
# check user exist.
class FindUser(Resource):
    """
    Find user with a email id .
    """
    # create a parser.
    Find_user_parser = reqparse.RequestParser( )
    # add arguments
    Find_user_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")

    @classmethod
    def post(cls):
        """
        Post method.
        :return: Success code 1 when user is found .
        """
        # get data from json.
        input_data = FindUser.Find_user_parser.parse_args( )
        # corresponding user exist in database
        user = UserModel.find_user(input_data['email_id'])
        # if user null return error .
        if user is None:
            return {'message': 'No user found with this email id', 'Success_Code': 0}, 404
        else:
            return {'message': 'User found', 'Success_Code': 1}, 200
# </editor-fold>


# <editor-fold desc="Update User with new password. ">
# update user password.
class UpdateUser(Resource):
    """
    Update user with new password .
    """
    # create a parser.
    update_user_parser = reqparse.RequestParser( )
    # add arguments
    update_user_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")
    update_user_parser.add_argument('new_password', type=str, required=True, help="This field cannot be blank.")

    @classmethod
    def post(cls):
        """
        Post method .
        :return: Success_Code : 1 when password updated successfully.
        """
        # input data.
        input_data = UpdateUser.update_user_parser.parse_args( )
        # get user with email id .
        user = UserModel.find_user(input_data['email_id'])
        # update user password
        user.password = UserModel.set_password(input_data['new_password'])
        # save it in data base.
        user.save_data( )
        return {'message': 'User password updated', 'Success_Code': 1}, 200
# </editor-fold>


# <editor-fold desc="Log out.">
# Log out user .
class Logout(Resource):
    """
    Make user Log out if logged in .
    """
    # create a parser.
    logout_user_parser = reqparse.RequestParser()
    logout_user_parser.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")

    @classmethod
    def post(cls):
        """
        post method .
        :return: 'Success_Code': 1 if log out successful .
        """
        # input data.
        input_data = Logout.logout_user_parser.parse_args( )
        # get user with email id .
        user = UserModel.find_user(input_data['email_id'])
        # if user is not none .
        if user is not None:
            # check user is logged in or not .
            if user.logged_in:
                user.logged_in = False
                user.save_data()
                return {'message': 'User Logged out . ', 'Success_Code': 1}, 200
            else:
                return {'message': 'User is already Logged out . ', 'Success_Code': 1}, 400
        else:
            return {'message': 'User not Logged out . ', 'Success_Code': 0}, 404
# </editor-fold>


# <editor-fold desc="Leader Board">
# Fetch data for leader Board
class LeaderBoard(Resource):
    """
    Leader Board Resources .
    contain  a post method .
    """
    # create a parser.
    leader_board_user_parser = reqparse.RequestParser()
    leader_board_user_parser.add_argument('leader_board_name', type=str, required=True, help="This field cannot be left blank")

    @classmethod
    def post(cls):
        """
        Post method
        Example : { "leader_board_name" : "BigMan"}
        """
        # input data.
        input_data = LeaderBoard.leader_board_user_parser.parse_args()
        # return list of  users
        return UserModel.get_leader_board(input_data['leader_board_name'])
# </editor-fold>


# <editor-fold desc="update In game currency">
class UpdateUserMoney(Resource):
    """
    update user Money .
    """
    # create a parser.
    update_user_money = reqparse.RequestParser()
    # add arguments
    update_user_money.add_argument('us_dollar', type=int, required=True, help="This field cannot be blank.")
    update_user_money.add_argument('email_id', type=str, required=True, help="This field cannot be blank.")

    @classmethod
    def post(cls):
        """
        make a post with email id and updated money .
        it will update the us_dollar value in the database .
        :return: update user .
        Example: post contain json {'email_id':'reezoobose@rediffmail.com','us_dollar':'1000000000000'}
        """
        # input data.
        input_data = UpdateUserMoney.update_user_money.parse_args()
        # email id .
        user = UserModel.find_user(input_data['email_id'])
        # if user found.
        if user is not None:
            user.us_dollar = input_data['us_dollar']
            user.save_data()
            return {'message': user.json(), 'Success_Code': 1}, 200
        return {'message': 'No user found with this email id ', 'Success_Code': 0}, 404
# </editor-fold>