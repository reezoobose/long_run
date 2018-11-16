# <editor-fold desc="Import">
# -*- coding: utf-8 -*-
# import sql alchemy object .
from sql_alchemy_extension import sql_alchemy as db
# we need to store password in salt form .
from werkzeug.security import generate_password_hash, safe_str_cmp


# </editor-fold>


# class must inherit Model from sql Alchemy .
class UserModel(db.Model):
    # <editor-fold desc="Database Table Connection and Coloumn Details">
    """
    object representation of the user .
    user is a model stored in database as an object .
    inherit from Sql_alchemy model .
    """

    #  crete the table to store user model.
    __tabalename_ = 'users'
    # columns details contain by table name.
    # is user logged in .
    logged_in = db.Column(db.Boolean, default=False)
    # unique not null username
    username = db.Column(db.String(80))
    # unique not null email id .
    email_id = db.Column(db.String(30), primary_key=True)
    # password
    password = db.Column(db.String(80))
    # user device_id where user is  registering and log in .
    device_id = db.Column(db.String(80))
    # user in game money
    us_dollar = db.Column(db.BigInteger)

    # </editor-fold>

    # <editor-fold desc="Constructor">
    # constructor
    def __init__(self, username, email_id, password, us_dollar=0, device_id=None):
        """
        A user will be created with those parameter present .
        :param username: user name of the user . It will be shown .
        :param email_id: user email id for registration .
        :param password: password for registration . secure salt will be stored in  database .
        :param us_dollar: In game currency
        :param device_id: Device Id from which user is going to register .
        """
        self.username = username
        self.email_id = email_id
        self.password = self.set_password(password)
        self.logged_in = False
        self.us_dollar = us_dollar
        self.device_id = device_id

    # </editor-fold>

    # <editor-fold desc="Class Methods">
    # region for classMethod

    # convert the password into salt form to store in database.
    @classmethod
    def set_password(cls, password):
        """
        Set Password return a secure hash of the password insert by the user .
        :param password: password insert by the user .
        :return:a string ie. secure hash of the password only 10 character from 5 to 15 .
        """
        generated_hash = generate_password_hash(password)
        return generated_hash[5:15]

    # check the password that is stored in data base and password enter by user are same or not .
    @classmethod
    def check_password(cls, stored_password_in_db, received_password_from_user):
        """
        compare the password used by user and the password stored in the database are same or not at the time of login .
        :param stored_password_in_db: password stored in database for the user .
        :param received_password_from_user: password that we received from the user .
        :return: True/False
        """
        return safe_str_cmp(stored_password_in_db, received_password_from_user)

    # Is user present in DataBase.
    # search is operated using user name and  email id .
    @classmethod
    def find_user(cls, email_id):
        """
        Find and user present in the database or not .
        :param email_id:
        :return: None if user not found or UserModel instance with all data .
        """
        # Select from the table users where  email_id = email_id limit 1 .
        # return a UserModel Object .
        return cls.query.filter_by(email_id=email_id).first( )

    # Find the list of users are logged in at this instance .
    @classmethod
    def find_users_logged_in(cls):
        """
        Find the List of users who are currently logged in .
        :return: List of users those who are logged in .
        """
        return {'Users': list(map(lambda x: x.json( ), cls.query.filter_by(logged_in=True).all( )))}

    @classmethod
    def get_leader_board(cls, leader_board_name):
        """
       Newbie - 0 JGD to 500,000 JGD //Ok
       Big Man - 500,001 JGD to 1,000,000 JGD //Ok
       Businessman - 1,000,001 JGD to 5,000,000 JGD //Ok
       Entrepreneur - 5,000,001 JGD to 500,000,000 JGD
       Tycoon - 500,000,001 JGD to 2,000,000,000 JGD //Ok
       :param leader_board_name: name of leader board .
       :return: a list of user under the name of leader board supplied .
        """
        user_leader_board_list = None
        user_leader_board_name = None
        if safe_str_cmp(leader_board_name, "Newbie"):
            upper_limit = 500000
            lower_limit = 0
            user_leader_board_name = 'Newbie'
            user_leader_board_list = cls.query.filter(cls.us_dollar.between(lower_limit, upper_limit))
        elif safe_str_cmp(leader_board_name, "BigMan"):
            upper_limit = 1000000
            lower_limit = 500001
            user_leader_board_name = 'BigMan'
            user_leader_board_list = cls.query.filter(cls.us_dollar.between(lower_limit, upper_limit))
        elif safe_str_cmp(leader_board_name, "Businessman"):
            upper_limit = 1000001
            lower_limit = 5000000
            user_leader_board_name = 'Businessman'
            user_leader_board_list = cls.query.filter(cls.us_dollar.between(lower_limit, upper_limit))
        elif safe_str_cmp(leader_board_name, "Entrepreneur"):
            upper_limit = 500000000
            lower_limit = 5000001
            user_leader_board_name = 'Entrepreneur'
            user_leader_board_list = cls.query.filter(cls.us_dollar.between(lower_limit, upper_limit))
        elif safe_str_cmp(leader_board_name, "Tycoon"):
            upper_limit = 2000000000
            lower_limit = 500000001
            user_leader_board_name = 'Tycoon'
            user_leader_board_list = cls.query.filter(cls.us_dollar.between(lower_limit, upper_limit))
        return {'Leader Board': user_leader_board_name, 'User': [x.json() for x in user_leader_board_list],
                "Success_Code": 1}, 200

    # </editor-fold>

    # <editor-fold desc="Instance Methods">
    # Save the Object in the data base .
    def save_data(self):
        """
        Save data to database .
        :return: null .
        """
        db.session.add(self)
        db.session.commit( )

    #  Remove the data from the data base .
    def remove_data(self):
        """
        Remove data from the database .
        :return: null.
        """
        db.session.delete(self)
        db.session.commit( )

    # To json
    def json(self):
        """
        convert in to json format .
        :return: json formatted user data .
        """
        return {'User_Name': self.username, 'Email': self.email_id, "Joe Games Currency": self.us_dollar}

    # Mark a user as logged in or out .
    def user_logged_in(self, logged_in):
        """
        Make user logged in or logged out and save data .
        :param logged_in: True / False.
        :return: null .
        """
        self.logged_in = logged_in
        self.save_data( )
    # </editor-fold>
