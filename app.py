from flask import Flask, render_template, request, make_response, session, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost:3306/ajax1'
app.config['SECRET_KEY'] = 'I love XWZ'

db = SQLAlchemy(app)


# 创建用户表
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(18), unique=True, nullable=True)
    password = db.Column(db.String(32), nullable=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<users:%r>' % self.username


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     else:
#         try:
#             if 'username' in request.form:
#                 username = request.form.get('username')
#                 print(username)
#                 un = db.session.query('Users').filter_by(username=username).first()
#                 print(un)
#             if un:
#                 return render_template('register.html', ts="alert('用户名已存在')")
#             else:
#                 password = request.form.get('password')
#                 us = Users(username, password)
#                 db.session.add(us)
#                 db.session.commit()
#                 ts = '注册成功,跳转至登陆界面'
#                 return render_template('login.html', ts=ts)
#         except:
#             return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'id' in session and 'username' in session:
            return redirect('/')
        elif 'id' in request.cookies and 'username' in request.cookies:
            session['id'] = request.args.get('id')
            session['username'] = request.args.get('username')
            return redirect('/')
        return render_template('login.html')
    else:
        # 接收用户名密码
        uname = request.form.get('username')
        password = request.form.get('password')
        print(uname, password)
        # 验证数据库
        us = db.session.query(Users).filter_by(username=uname, password=password).first()
        if us:
            # 存入session以保存登陆状态
            session['id'] = us.id
            session['username'] = uname
            print(session['id'])
            # 查看是否记住账号密码
            if 'rmpwd' in request.form:
                resp = make_response('登陆成功')
                resp.set_cookie('username', uname, max_age=60 * 30)
                print('登陆了')
            print('登陆了')
            return redirect('/')
        else:
            return render_template('login.html')


@app.route('/')
def index():
    if 'id' in session and 'username' in session:
        uname = session['username']
        print('这是', uname)
    return render_template('index.html', arg=locals())


@app.route('/log_out')
def log_out():
    if 'id' in session and 'username' in session:
        del session['id']
        del session['username']
    return redirect('/')


db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
