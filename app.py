from MySQLdb.cursors import Cursor
from flask import Flask, render_template, redirect, flash
from flask.globals import request
from flask.helpers import url_for
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')

app.config['MYSQL_HOST'] = 'bopzzm3wvllhte5nnepy-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'u1abqfyilh7e5mat'
app.config['MYSQL_PASSWORD'] = 'lcnX1iCTWu3kMSoTZtgg'
app.config['MYSQL_DB'] = 'bopzzm3wvllhte5nnepy'

mysql = MySQL(app)

app.secret_key = 'abueno'

def selectUsers():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from usuarios')
    datas = cursor.fetchall()
    return datas

def validateDocument(document):
    datos = selectUsers() 
    for i in datos:
            if document == i[1]:             
                flash('The documento already exist, try again')
                return True
    return False

def validateFields(document, names, surnames, phone, email):            
    if (document == '' or names == '' or surnames == '' or phone == '' or email == ''):
        flash('Please complete all fields')         
        return True
    return False  

@app.route('/')
def index():
    datas = selectUsers()
    return render_template('index.html', datas = datas)

@app.route('/register_user', methods=['POST'])
def register():
    if request.method == 'POST':
        document = request.form['document']
        names = request.form['names']
        surnames = request.form['surnames']
        phone = request.form['phone']
        email = request.form['email']

        result_fields = validateFields(document,names,surnames,phone,email)
        result_document = validateDocument(document)

        if result_fields == False and result_document == False:
            cursor = mysql.connection.cursor()
            cursor.execute("insert into usuarios (documento, nombres,  apellidos, telefono, email) values (%s,%s,%s,%s,%s)",(document,names,surnames,phone,email))
            mysql.connection.commit()
            flash('User added sucesfully')
            return redirect('/')

        return redirect('/')

@app.route('/delete_register/<int:id>')
def delete(id): 
    cursor = mysql.connection.cursor()
    cursor.execute(f"delete from usuarios where id = {id}")
    mysql.connection.commit()

    flash('User removed susesfully')
    return redirect('/')

@app.route('/update_register/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        document = request.form['document']
        names = request.form['names']
        surnames = request.form['surnames']
        phone = request.form['phone']
        email = request.form['email']

        result = validateFields(document,names,surnames,phone,email)

        if result == False:
            cursor = mysql.connection.cursor()
            cursor.execute(f"update usuarios set nombres = '{names}', apellidos = '{surnames}', telefono = '{phone}', email = '{email}' where id = {id}")
            mysql.connection.commit()   
            flash('User modify susesfully')
            return redirect('/') 

        return redirect('/')       
    
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from usuarios where id = {id}")
    datas = cursor.fetchone()
    return render_template('update.html', datas = datas)

if __name__ == '__main__':
    app.run(port = 4000, debug = True)
