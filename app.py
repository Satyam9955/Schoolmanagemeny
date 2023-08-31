from flask import Flask,render_template,request,session
import requests
from passlib.hash import hex_sha1 as sha
import pymysql as sql
app = Flask(__name__)
app.secret_key='gjgsk_-6546787698nbcvmnsbkjlkuifaDFH8989YJak;l'
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/signup/')
def signup():
    return render_template('signup.html')  
@app.route('/aftersignup/',methods=['GET','POST'])
def aftersignup():
    name=request.form.get('name')
    father=request.form.get('father')
    mother=request.form.get('mother')
    clas=request.form.get('clas')
    email=request.form.get('email')
    passwd=sha.hash(request.form.get('pass'))
    db = sql.connect(host='localhost',port=3306,user='root',database='school')
    cur = db.cursor()
    cmd = f"insert into signupinfo(Name,Father,Mother,Class,Email,password) values('{name}','{father}','{mother}','{clas}','{email}','{passwd}')"
    cur.execute(cmd)
    db.commit()
    cmd = 'select * from signupinfo order by Admission_No desc limit 1'
    cur.execute(cmd)
    data=cur.fetchone()
    data={
        'Admission':data[0],
        'Name':data[1],
        "Father's Name":data[2],
        "Mother's Name":data[3],
        'Class':data[4],
        'Email':data[5],
        'Password':data[6],
    }
    return render_template('aftersignup.html',data=data)
@app.route('/login/')
def login():
    if session.get('account'):
        return render_template('afterlogin.html')
    else:
        return render_template('login.html')    
    

@app.route('/afterlogin',methods=['GET','POST'] )    
def afterlogin():
    acc=request.form.get('acc')
    passwd=request.form.get('pass')
    db = sql.connect(host='localhost',port=3306,user='root',password='',database='school')
    cur = db.cursor()
    cmd=f'select * from signupinfo where Admission_no={acc}'
    cur.execute(cmd)
    data=cur.fetchone()
    if data:
        if sha.verify(passwd,data[6]):
            session['account']=acc
            session['passwd']=passwd
            return f'<h1>{acc},{passwd} logged in.</h1>'
            
        else:
            error='Invalid Password Please Try Again!!!'
        return render_template('login.html',error=error) 
                
    else:
        error=' Account Does Not Exits Please Try Again!!!'
        return render_template('login.html',error=error)  

@app.route('/logout/')
def logout():
    del session['account']
    del session['passwd']
    return '<h1>LOgged out</h1>'    

@app.route('/weather/',methods=["GET","POST"])
def weather():
    if request.method=='GET':
        return render_template('weather.html')
    else:
        city=request.form.get('city')
        
        url=f"http://api.openweathermap.org/data/2.5/weather?appid=6722dad84bee0048e9bee0e7c96de5ae&q={city}"
        page=requests.get(url)
        data=page.json()
        data1={'name :' :data.get('name'),
            'coordination(longitude,altitude) :' :data.get('coord'),
                    'weather :' :data.get('weather'),
                    'base :' :data.get('base'),
                    'main :' :data.get('main'),
                    'visibility :' :data.get('visiblity'),
                    'wind :' :data.get('wind'),
                    'clouds :' :data.get('clouds'),
                    'dt :' :data.get('dt'),
                    'sys :' :data.get('sys'),
                    'timezone :' :data.get('timezone'),
                    'id :' :data.get('id'),
                    
                    'cod :' :data.get('cod'),
               }
        
        return render_template('weather1.html',data=data1)
    



app.run(host='localhost',port=80,debug=True)