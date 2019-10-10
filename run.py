from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from flask import Flask, render_template, redirect, url_for, request


# Every website is application in 'flask'
app = Flask(__name__, template_folder='template')
# Database access through 'username'= root  and 'password'= None
# My username is 'root' cause I'm on the local host and I'd set any password
# One more thing password is after two dots :


Base = declarative_base()

class detail(Base):
    __tablename__='detail'
    id = Column('No.', Integer, primary_key=True)
    name = Column('Name', String(15), nullable=True)
    email = Column('Email', String(20), nullable=True)
    phone = Column('Phone', String(14), nullable=True)
    date = Column('Date', String, default=datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y   %I:%M:%S'))

engine = create_engine('mysql://root:@localhost/flask')
Base.metadata.create_all = engine


database = sessionmaker(bind=engine)
session = database()

# data = detail(name='anonymous', email='anonymous@gmail.com', phone='4444444444')
# session.add(data)
# session.commit()



# routing( setting end points in website) with ['post', 'get'] method
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        try:
            # commit to add value in database
            data = detail(name=name, email=email, phone=phone)
            session.add(data)
            session.commit()
            # after commit redirect to this page
            return redirect(url_for('index'))

        except Exception as e:
            print(e)

    else:
        # Get data from database and put it 'index.html'
        items = session.query(detail).order_by(detail.date)
        return render_template('index.html', items=items)




if __name__ == '__main__':
    # run flask app and you might be thinking debug mean, It mean that if you'll do any change in your application It'll grab automatically
    app.run(debug=True)
