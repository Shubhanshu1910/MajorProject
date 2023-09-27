from __future__ import division, print_function

import glob
import os
# config = ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.2
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)
import random
import re
import sys

import numpy as np
# import tensorflow as tf
from flask import Flask, redirect, render_template, request, url_for
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
# from tensorflow.keras.applications.resnet50 import preprocess_input
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

# from tensorflow.compat.v1 import ConfigProto, InteractiveSession



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'user'
import string

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shubhanshum154@gmail.com'
app.config['MAIL_PASSWORD'] = 'jyhluxobrfrxstfy'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

MODEL_PATH ='model.h5'

# Load your trained model
# model = load_model(MODEL_PATH,compile = False)




# def model_predict(img_path, model):
#     print(img_path)
#     img = image.load_img(img_path, target_size=(224, 224))

#     # Preprocessing the image
#     x = image.img_to_array(img)
#     # x = np.true_divide(x, 255)
#     ## Scaling
#     x=x/255
#     x = np.expand_dims(x, axis=0)
   

#     # Be careful how your trained model deals with the input
#     # otherwise, it won't make correct prediction!
#    # x = preprocess_input(x)

#     preds = model.predict(x)
#     preds=np.argmax(preds, axis=1)
#     if preds==0:
#         preds="cat"
#     elif preds==1:
#         preds="dog"
#     elif preds == 2:
#         preds="Not identified"
    
    
    
#     return preds

mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])
def register1():
    if request.method=='GET':
        return render_template('/Homepage/index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('/Register/index.html')
    else:
        Name=request.form.get('name')
        Password=request.form.get('password')
        reenter=request.form.get('re-enter')
        Email=request.form.get('email')
        
        Contact=request.form.get('contact')
        Uid = int(100)
        random="111"
        if  not Name :
            return "Please enter your username"
        if  not Password :
            return "Please enter your password"
        if  not reenter :
            return "Please enter your password again"
        if Password !=reenter:
            return "Password notmatched"
        if  not Email :
            return "Please enter your email"
        if  not Contact :
            return "Please enter your contact"
        else:
            Contact=int(Contact)
        cur = mysql.connection.cursor()
        sql = 'INSERT INTO register(Uid,Name,Password,contact,Email,random) VALUES (%s,%s,%s,%s,%s,%s);'
        cur.execute(sql,(Uid,Name,Password,Contact,Email,random))
        mysql.connection.commit()
        
        return render_template('/Register/login.html')




@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
       return render_template('/Login/index.html')
    else:
        username=request.form.get('username')
        password=request.form.get('password')
        email=request.form.get('email')
        cur = mysql.connection.cursor()
        sql_query=f"""SELECT * FROM register WHERE Name='{username}' AND Password='{password}'"""
        cur.execute(sql_query)
        results=cur.fetchall()
        cur.close()
        if not results:
            return render_template('/Login/index.html')
        return render_template('sucess.html',mylist=results)
    
    
@app.route('/login_Secure/<int:Contact>',methods=['GET','POST'])
def edit_student(Contact):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM register WHERE Contact={Contact} ")
        info_results=cur.fetchall()[0]
        cur.close()
        return render_template('image.html',mylist=info_results)
    # else:
    #     img = request.files['my_image']
    #     problem=request.form.get('problem')
    #     if not img:
    #         return "Image not found"
    #     img.filename = str(Contact)
    #     img_path = "images/"+img.filename+".jpeg"
    #     ui='name'
    #     img.save(img_path)
    #     # f=img.filename+'1'+ui
    #     preds = model_predict(img_path, model)
    #     status1 = "ON"
    #     result=preds
    #     dict ={'status':'ON'}
    #     cur = mysql.connection.cursor()
    #     sql_query = f"""SELECT email FROM query WHERE problem='{result}' ;"""
    #     cur.execute(sql_query)
    #     email=cur.fetchall()
    #     cur.close()
        
    #     cur = mysql.connection.cursor()
    #     sql=f"""UPDATE query SET status='{result}'"""
    #     cur.execute(sql)
    #     result1 = cur.fetchall()
    #     cur.close()
    #     new=email[0]
        
    #     for i in email:
    #         new=i[0]
    #     ema = "shubhanshum154@gmail.com"
        
    #     msg = Message("name", sender = 'shubhanshum154@gmail.com', recipients = [new])
    #     msg.body = " !111"
    #     msg.subject="problem "
    #     src=img_path
    #     with app.open_resource(src) as fp:
    #             msg.attach(src, src, fp.read())
        
    #     mail.send(msg)
       
    #     return render_template('new.html', mylist = email
                               
    #                            )
    
    # return None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
@app.route("/about",methods=['GET'])
def about_shubhanshu():
    return render_template("/about/index.html")

@app.route("/contact",methods=['GET'])
def contact():
    return render_template("/contact/index.html")


if __name__ == "__main__":
    app.run()  # Flask
    run_simple("localhost", 5000, app)
