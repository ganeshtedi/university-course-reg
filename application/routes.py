
from application import app, db
from application.forms import Loginform,Regform
from application.models import User,Course,Enrollment
from flask import render_template,json,Response,request,flash,redirect,session,jsonify
#from flask_restplus import Resource

coursedata= [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route("/")
@app.route("/index")
@app.route("/home")

def index():
    return render_template("index.html",index=True)
@app.route("/courses")
@app.route("/courses/<term>")
def courses(term = None):
    if not session.get('username'):
        return redirect("/login")
    classs= Course.objects.order_by('-courseID')
    term= 'spring 2019'
    return render_template("course.html",coursedata=classs,course=True,term=term)
@app.route("/login",methods=['GET','POST'])
def login():
    if   session.get('username'):
        return redirect("/index")
    lform=Loginform()
    if lform.validate_on_submit():
        email = lform.email.data
        password = lform.password.data
        
        user = User.objects(email=email).first()
        if user and user.getpass(password) :    
            flash(f'{user.fname},you are successfully logged in','success')
            session['userid']=user.userid
            session['username']=user.fname           
            return redirect("/index")
        else:
            flash('you  are not successfully logged in','danger')   
    return render_template("login.html",login=True,title='Login', form=lform)
@app.route("/logout")
def logout():
    session['userid']=False
    session.pop('username',None)
    return redirect("/index")

@app.route("/register",methods=['GET','POST'])
def register():
    if session.get('username'):
        return redirect("/index")
    form = Regform()
    if form.validate_on_submit():
        userid=User.objects.count()
        userid +=1
        email = form.email.data
        password = form.password.data
        fname= form.fname.data
        lname= form.lname.data

        user =User(userid=userid,email=email,fname=fname,lname=lname)
        user.setpass(password)
        user.save()
        flash(f'{user.fname},you are successfully registered in','success')
        return redirect("/index")
    return render_template("register.html",register=True,form=form)

@app.route("/enrollment",methods=['GET','POST'])
def enrollment():
    if not session.get('username'):
        return redirect("/login")
    id= request.form.get('courseID')
    title=request.form.get('title')
    term=request.form.get('term')

    userid=session.get('userid')
    if id:
        if Enrollment.objects(userid=userid,courseID=id):
            flash('ALREADY REGISTERED')
            return redirect("/courses")
        else:
            Enrollment(userid=userid,courseID=id,title=title).save()
            flash(f'you are enrolled in this {title}','success')
    classs=list(User.objects.aggregate(*[
    {
        '$lookup': {
            'from': 'enrollment', 
            'localField': 'userid', 
            'foreignField': 'userid', 
            'as': 'r1'
        }
    }, {
        '$unwind': {
            'path': '$r1', 
            'includeArrayIndex': 'r1_id', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$lookup': {
            'from': 'course', 
            'localField': 'r1.courseID', 
            'foreignField': 'courseID', 
            'as': 'r2'
        }
    }, {
        '$unwind': {
            'path': '$r2', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'userid': userid
        }
    }, {
        '$sort': {
            'courseID': -1
        }
    }
]))
    return render_template("enrollment.html",enrollment=True,classes=classs,title=title)
@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if idx==None:
        jdata=coursedata
    else:
        jdata=coursedata[int(idx)]
    return Response(json.dumps(jdata),mimetype="application/json")


@app.route("/user")
def user():
    users = User.objects.all()
    return render_template('user.html',users=users)
