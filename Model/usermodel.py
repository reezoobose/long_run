# import sql alchemy object .
from sql_alchemy_extension import sql_alchemy as db
# we need to store password in salt form .
from werkzeug.security import generate_password_hash, safe_str_cmp


# class must inherit Model from sql Alchemy .
class UserModel(db.Model):
    #  crete the table to store user model.
    __tabalename_ = 'users'
    # columns details contain by table name.
    # is user logged in .
    logged_in = db.Column(db.Boolean,default=False)
    # unique not null username
    username = db.Column(db.String(80))
    # unique not null email id .
    email_id = db.Column(db.String(30), primary_key=True)
    # password
    password = db.Column(db.String(80))
    # user device_id where user is  registering and log in .
    device_id = db.column(db.String(80))
    # user in game money
    us_dollar = db.column(db.Integer)

    # constructor
    def __init__(self, username, email_id, password, us_dollar=0, device_id=None):
        self.username = username
        self.email_id = email_id
        self.password = self.set_password(password)
        self.logged_in = False
        self.us_dollar = us_dollar
        self.device_id = device_id

    # convert the password into salt form to store in database
    @classmethod
    def set_password(cls, password):
            generated_hash = generate_password_hash(password)
            return generated_hash[5:15]

    # check the password that is stored in data base and password enter by user are same or not .
    @classmethod
    def check_password(cls, stored_password_in_db, received_password_from_user):
        return safe_str_cmp(stored_password_in_db, received_password_from_user)

    # To json
    def json(self):
        return {'User_Name': self.username, 'Email': self.email_id, "Joe Games Currency": self.us_dollar}

    # Is user present in DataBase.
    # search is operated using user name and  email id .
    @classmethod
    def find_user(cls, email_id):
        # Select from the table users where  email_id = email_id limit 1 .
        # return a UserModel Object .
        return cls.query.filter_by(email_id=email_id).first()

    # Mark a user as logged in or out .
    def user_logged_in(self, logged_in):
        self.logged_in = logged_in
        self.save_data(),

    # return true if user logged in
    def is_user_logged_in(self):
        return self.logged_in

    # Find the list of users are logged in at this instance .
    @classmethod
    def find_users_logged_in(cls):
        return {'Users': list(map(lambda x: x.json(), cls.query.filter_by(logged_in=True).all()))}

    # Save the Object in the data base .
    def save_data(self):
        db.session.add(self)
        db.session.commit()

    #  Remove the data from the data base .
    def remove_data(self):
        db.session.delete(self)
        db.session.commit()
