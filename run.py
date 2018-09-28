# import app .
from app import app
# import sql alchemy object from sql alchemy extension .
from sql_alchemy_extension import sql_alchemy
# initialize .
sql_alchemy.init_app(app)


# decorator  runs before app first api is fired .
@app.before_first_request
# create all tables .
def create_tables():
    """
    Create Tables in database .
    :return: null.
    """
    # create all columns and details of the  empty table .
    sql_alchemy.create_all()