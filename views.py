from flask import  Response, render_template, request ,redirect, send_file, url_for , session, flash
import base64
import smtplib
from flask import Blueprint
from elecdetails import *
from login import *
from register import *
from activity import *
from create import *
from mail import *
from info import *
from flask_wtf import FlaskForm
from wtforms import DateField,TimeField , RadioField, validators,SubmitField,SelectField,StringField
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
from test import *

LOCKOUT_THRESHOLD = 3  # Number of failed attempts to trigger lockout
LOCKOUT_DURATION_MINUTES = 15  # Lockout duration in minutes
failed_login_attempts = {}

views = Blueprint(__name__,"views")

class CreateElection(FlaskForm):
    title =  StringField('Title of Election', validators=(validators.DataRequired(),),description='Title of the Election')
    s_date = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    s_time = TimeField('Start Time', format='%H:%M', validators=(validators.DataRequired(),))
    e_date = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    e_time = TimeField('End Time', format='%H:%M', validators=(validators.DataRequired(),))
    no_candidates = SelectField(u'No of candidates', choices=[('2', '2'),('3', '3'),('4', '4')],validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')

class VoteCasting(FlaskForm):
    candidate = RadioField('Candidate ID', choices=[])
    submit = SubmitField('Vote')

@views.route("/")
def home():
    return render_template('home.html')

@views.route("/voting")
def voting():
    return render_template("voting.html")

@views.route("/signup")
def signup():
    return render_template("signup.html")

@views.route("/login")
def login():
    return render_template("login.html")

@views.route("/user", methods=['POST','GET'])
def user():
    if request.method == 'POST':
        email = request.form['email']
        psw = request.form['password']
        loggedin,id,uname = loginf(email,psw)
        if loggedin:
            session['username'] = uname
            session['id'] = id
            flash('login successful')
            return redirect(url_for('views.activity'))
        else:
            return "login failed"
        
@views.route("/success", methods=['POST','GET'])
def success():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        pno = request.form['pno']
        psw = request.form['password']
        psw_repeat = request.form['c_password']
        if psw != psw_repeat:
            flash('Password do not match')
            return redirect(url_for('views.login'))
        else:
            psw = sha256_crypt.encrypt(psw)
            register(email,pno,username,psw)
            flash('registered successfully')
            return redirect(url_for('views.home'))
        
@views.route("/activity")
def activity():
    uid = session['id']
    elections = activity_elc(uid)
    return render_template("activity.html",elections=elections)

@views.route("/create", methods=['POST','GET'])
def create():
    form = CreateElection()
    if request.method == 'POST':
        uid = session['id']
        title,s_date,s_time,e_date,e_time,no_candidates = request.form['title'], request.form['s_date'], request.form['s_time'], request.form['e_date'], request.form['e_time'], request.form['no_candidates']
        create_el(uid,no_candidates,title,s_date,s_time,e_date,e_time)
        return render_template('election.html')
    else:
        return render_template('create.html',form=form)
    
@views.route("/profile",methods=['POST','GET'])
def profile():
    if session.get('id') != None:
        uid = session['id']
        return render_template('profile.html',uid=uid)
    else:
        return "Not logged in"

@views.route('logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))

@views.route("/candidates")
def candidates():
    if request.args.get('eid') != None:
        eid = request.args.get('eid')
        session['eid'] = eid
    eid=session['eid'] 
    data = elecdetails(eid)
    no_of_c = data[0][3]
    c_info = cad_details(eid)
    c_registered = len(c_info)
    if c_registered == no_of_c:
        return render_template('candidates.html',data=c_info,regis_full=True)
    return render_template('candidates.html',data=c_info)

@views.route("/r_cad",methods=['POST','GET'])
def r_cad():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        email = request.form['email']
        slogan = request.form['slogan']
        eid = session['eid']
        rcad(eid, first_name, last_name, age, email, slogan)
        flash("Candidate Added Successfully")
        return redirect(url_for('views.candidates'))

@views.route("/voters",methods=['POST','GET'])
def voters():
    eid = session['eid']
    regis_full = False
    if request.method=='POST':
        vid = request.form['vid']
        vkey = request.form['vkey']
        vemail = request.form['vemail']
        vname = request.form['vname']
        if len(vid) == 10 and len(vkey) == 10:
            send_mail(vemail, "Voting", vname, vid, vkey)
            vkey = sha256_crypt.encrypt(vkey)
            r_voter(eid,vid,vkey,vemail,vname)
            data=voter_info(eid)
            if data != None:
                if len(data) == 20:
                    regis_full= True
                return render_template('voters.html',data=data,regis_full=regis_full )
        else:
            flash('VID or VKey not upto 10 characters')
            data = voter_info(eid)
            if data != None:
                if len(data) == 20:
                    regis_full= True
                return render_template('voters.html',data=data,regis_full=regis_full )
            return render_template('voters.html',data=data,regis_full=regis_full )
    else:
        data = voter_info(eid)
        if data != None:
            if len(data) == 20:
                regis_full= True
            data = voter_info(eid)
        return render_template('voters.html',data=data,regis_full=regis_full )

@views.route("/vote",methods=['POST','GET'])
def vote():
    if request.method=='POST':
        vid = request.form['vid']
        vkey = request.form['vkey']
        if vid in failed_login_attempts and failed_login_attempts[vid]['count'] >= LOCKOUT_THRESHOLD:
            lockout_time = failed_login_attempts[vid]['time']
            if datetime.now() - lockout_time < timedelta(minutes=LOCKOUT_DURATION_MINUTES):
                flash(f"Account locked due to too many failed login attempts. Try again later.")
                return render_template('home.html')
        verified,eid = verify(vid,vkey)
        if verified:
            session['vid'] = vid
            if vid in failed_login_attempts:
                failed_login_attempts[vid]['count'] = 0
            form = VoteCasting()
            data = cad_info(eid)
            det = elecdetails(eid)
            # if det[0][4] > datetime.now():
            #     flash("election is not started")
            #     return render_template('voting.html')
            # elif det[0][5] < datetime.now():
            #     flash("election has ended")
            #     return render_template('voting.html')
            # else: 
            form.candidate.choices = [(d[0],d[2] +" "+ d[3]) for d in data]
            flash('Verification successful')
            return render_template('casting.html',data=data)
        else:
            print(failed_login_attempts)
            if vid in failed_login_attempts:
                failed_login_attempts[vid]['count'] += 1  # Increment the count by 1
            else:
                failed_login_attempts[vid] = {'count': 1, 'time': datetime.now()}
            return render_template('voting.html')

@views.route("/cast_vote",methods=['POST','GET'])
def cast_vote():
    if request.method=="POST":
        cid = int(request.form["Candidate"])
        print(cid)
        data = cad_info(cid)
        print(data)
        votes = data[0][7]
        votes += 1
        sql1 = "UPDATE candidate_info SET no_of_votes = %s WHERE cid = %s;"
        val1 = (votes,cid)
        mycursor.execute(sql1, val1)
        vid = session['vid']
        sql2 = "DELETE from voter_info WHERE `vid`=%s"
        val2 = (vid,)
        mycursor.execute(sql2,val2)
        mydb.commit()
        return "Voting Successful"

@views.route("/test")
def test():
    d = test_t()
    return d