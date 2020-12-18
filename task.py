from flask import Flask,render_template,url_for,session,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:sravani@localhost/library"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Sample(db.Model):
    __tablename__= "book_details"
    id = db.Column(db.Integer,primary_key = True)
    bookname=db.Column(db.String(100))
    ISBNno=db.Column(db.String(50),unique=True)
    department=db.Column(db.String(100))
class Sample1(db.Model):
    __tablename__="std_details"
    id = db.Column(db.Integer,primary_key = True)
    studentname=db.Column(db.String(100))
    studentnumber=db.Column(db.String(100),unique=True)
    bookname=db.Column(db.String(100))
    ISBNno=db.Column(db.String(90),unique=True)
    department=db.Column(db.String(100))
    
@app.route('/',methods=["POST","GET"])
def clg():
     return render_template("library.html")

@app.route('/booklist',methods=["POST","GET"])
def boolist():
    if request.method=="POST":
        if request.form['submit']== 'submit':
            search = request.form['search']

            result = Sample.query.filter_by(department = search).all()
            print(result) #result.id
            
            conn = psycopg2.connect(database = 'library', user = 'postgres', password = 'sravani', host = '127.0.0.1', port = '5432')
            cursor = conn.cursor()
            conn.autocommit = True
            cursor.execute('select * from book_details')
            result = cursor.fetchall()
            length=len(result)

            print(result)
            # flash("book is successfully added")
            return render_template("bt.html",result=result,length = length)
        # return redirect(url_for("",result=result))
    return render_template('book.html')

    #     if request.form['submit'] == 'add':
    #         bookname= request.form["name"]
    #         ISBNno= request.form["num"]
    #         department= request.form["dept"]
    #         data=Sample(bookname=bookname.upper(),ISBNno=ISBNno,department=department.upper())

    #         db.session.add(data)
    #         db.session.commit()
    #         print(ISBNno,bookname)
    #         # return  render_template('task.html')
    #         return  render_template('login4.html')
    # return render_template('task.html')
@app.route('/addbook' ,methods=["POST","GET"])
def addbook():
    if request.method=="POST":
        if request.form['submit'] == 'add':
            bookname= request.form["name"]
            ISBNno= request.form["num"]
            department= request.form["dept"]
            data=Sample(bookname=bookname.upper(),ISBNno=ISBNno,department=department.upper())

            db.session.add(data)
            db.session.commit()
            print(ISBNno,bookname)
            # return  render_template('task.html')
            # flash("book added successfully")
            return  redirect('/')
        return render_template('login4.html')

    return render_template('login4.html')

@app.route('/takebook' ,methods=["POST","GET"])
def takebook():
    if request.method=="POST":
        if request.form['sub'] == 'take':
            studentname=request.form["studentname"]
            studentnumber=request.form["studentnumber"]
            bookname= request.form["name"]
            department= request.form["dept"]
            ISBNno= request.form["num"]
            details=Sample1(studentname=studentname,studentnumber=studentnumber.upper(),bookname=bookname.upper(),ISBNno=ISBNno,department=department.upper())
            # details1=Sample()
            Sample.query.filter_by(ISBNno = ISBNno).delete()
            db.session.add(details)
            db.session.commit()
            print(studentnumber,studentname)
            # return "dfghj,"
            return redirect('/')
        return "dsfgtyhu"
    return render_template("take.html")
@app.route('/delete',methods=["POST","GET"])
def delete():
    if request.method=="POST":
    
        ISBNno=request.form["num"]
        print(ISBNno)
        Sample.query.filter_by(ISBNno = ISBNno).delete()
        db.session.commit()
        
        # return "gsdis"
        return render_template("delete.html")
    return render_template('delete.html')
   
if __name__=="__main__":
    db.create_all()
    app.run(debug=True)



