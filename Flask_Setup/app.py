from flask import Flask, render_template, request, session, flash, redirect, url_for, g
from flask_bcrypt import bcrypt
from flask_sqlalchemy import SQLAlchemy
# from models import User


app = Flask(__name__)
app.secret_key = 'somesecretkeyiknow'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return f"User('{self.email})'"

# class User:
#     def __init__(self,id,email,password):
#         self.id=id
#         self.email=email
#         self.password=password
    
#     def __repr__(self):
#         return f'<User:{self.email}>'

# users=[]
# users.append(User(id=1, email='mad@gmail.com', password='madhu001'))
# print(users)



# @app.before_request
# def before_request():
#     if 'user_id' in session:
#         user = [x for x in users if x.id==session['user_id']][0]
#         g.user = user
#     else:
#         g.user = None


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id',None)

        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        # user =[x for x in users if x.email==email][0]
        if user and user.password == password:
            # session['user_id']=user.id
            return redirect(url_for('profile'))
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        email = request.form['email']
        password= request.form['password']
        # hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, password=password)
        db.create_all()
        db.session.add(user)
        db.session.commit()
        flash('Your registersuccesss!')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/profile')
def profile():
    # if not g.user:
    #     return redirect(url_for('login'))

    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)