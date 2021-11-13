from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt

engine=create_engine("mysql+pymysql://root:Rishu0703@localhost/register")
db=scoped_session(sessionmaker(bind=engine))

app=Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

# register here
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        firstname=request.form.get("firstname")
        lastname=request.form.get("lastname")
        email=request.form.get("email")
        password=request.form.get("password")
        confirm=request.form.get("confirm")
        usertype=request.form.get("usertype")
        secure_password=sha256_crypt.encrypt(str(password))

        emailData=db.execute("SELECT email from users WHERE email=:email",{"email":email}).fetchone()
        
       
        if emailData!=None:
             flash("This email is already registered,try to login with your passwod","danger")
             return redirect(url_for('login'))


        if password==confirm:
            db.execute("INSERT INTO users(firstname,lastname,email,password,usertype) VALUES(:firstname,:lastname,:email,:password,:usertype)",
            {"firstname":firstname,"lastname":lastname,"email":email,"password":secure_password,"usertype":usertype})
            db.commit()
            flash("you are registered and can login now","success")
            return redirect(url_for('login'))
        else:
            flash("Password does not match","danger")
            return render_template("register.html")


    return render_template("register.html")

# login here
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
         email=request.form.get("email")
         password=request.form.get("password")
         emailData=db.execute("SELECT email from users WHERE email=:email",{"email":email}).fetchone()
         passwordData=db.execute("SELECT password from users WHERE email=:email",{"email":email}).fetchone()

         if emailData is None:
             flash("Email is not registered","danger")
             return render_template("login.html")
         else:
             for pswd in passwordData:
                 if sha256_crypt.verify(password,pswd):
                     flash("You are now login","success")
                     return redirect(url_for('waiting'))
                 else:
                     flash("Incorrect Password","danger")
                     return render_template("login.html")
                     
                       
    return render_template("login.html")




 #waiting room
@app.route("/waiting",methods=["GET","POST"])
def waiting():
     return render_template("waiting.html")   



if __name__=="__main__":
    app.secret_key="rishurishu"
    app.run(debug=True)