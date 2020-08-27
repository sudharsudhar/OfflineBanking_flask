from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = r'sqlite:////Users/Sudharsan/PycharmProjects/Offline_Banking/runner/db_module/demo_123.db'
db = SQLAlchemy(app)

app.secret_key = 'hello'


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    phonenumber = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))


class acc_details(db.Model):
    acc_id = db.Column(db.Integer, primary_key=True)
    acc_numb = db.Column(db.String(80))
    acc_holder_name = db.Column(db.String(80))
    credit = db.Column(db.String(80))
    debit  = db.Column(db.String(80))
    acc_email = db.Column(db.String(120))

    balance = db.Column(db.Integer)

class main_balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acc_holder_name = db.Column(db.String(80))
    acc_email = db.Column(db.String(120))
    main_money_balance = db.Column(db.Integer)

    # balance_id = db.Column(db.Integer, db.ForeignKey('balance.id'),nullable=False)
    # balance = db.Column(db.Integer)


# @app.route("/")
# def delete():
# acc_details.query.filter_by(balance=500).delete()
#     db.session.commit()
#     return render_template("index.html")

globalvariable = []


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        session['uname'] = uname
        print('session---' * 10)
        print(session['uname'])
        globalvariable.append(uname)

        login = user.query.filter_by(username=uname, password=passw).first()
        print('#--' * 20)
        print(login)
        print('#--' * 20)
        if login is not None:
            jj = user.query.filter_by(username=session['uname'])

            ss = jj.one().email
            vv = jj.one().username
            ll = jj.one().phonenumber
            show_balance = main_balance.query.filter_by(acc_holder_name=session['uname']).first()



            ba = show_balance.main_money_balance


            # return redirect(url_for("showdetails"))
            transhistroy()
            return render_template('homepage.html', globalvariable=globalvariable, vv=vv, ss=ss, ll=ll, ba=ba)
        else:
            alert = 'Check Username & Password'
            return render_template("loginpage.html", alert=alert)
    return render_template("loginpage.html")


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        lastname = request.form['lname']
        phonenumber = request.form['phonenumber']
        mail = request.form['mail']
        passw = request.form['passw']
        balance = 1000
        # alreadyexesist = user.query.filter_by(mail=mail).first()
        alreadyexesist = user.query.filter_by(email=mail).first()
        if alreadyexesist is not None:
            message = 'Sorry! Email already EXIST'
            return render_template("register.html", message=message)
        else:
            register = user(username=uname, lname=lastname, phonenumber=phonenumber, email=mail, password=passw)
            # REGISTER FOR BALANCE acc_details
            register_acc = acc_details(acc_numb=phonenumber, acc_holder_name=uname, acc_email=mail, balance=balance,credit="Bonus")
            # REGISTER FOR BALANCE acc_details
            db.session.add(register)
            db.session.commit()
            db.session.add(register_acc)
            db.session.commit()
            original_balance = main_balance(acc_holder_name=uname, acc_email=mail, main_money_balance=balance)
            db.session.add(original_balance)
            db.session.commit()
            return redirect(url_for("login"))
        # return render_template ("loginpage.html")
    return render_template("register.html")


#####################################################################################
@app.route("/<username>")  # , methods=["GET", "POST"])
def show_user(username):
    allemail = acc_details.query.filter(acc_details.acc_holder_name.endswith(session['uname'])).all()
    print('EEEE--' * 10)
    #allemaillll = acc_details.query.filter(acc_details.acc_holder_name.endswith(session['uname'])).all()
    trans = []
    keyvalue1 = []




    # print(u.acc_email)
    print('EEEEE--' * 10)
    for k in allemail:
        print(k.acc_email)
        print("-"*20)
        CountryCodeDict1 = {k.acc_holder_name: [k.acc_email,k.credit,k.debit,k.balance]}
        count = { "Name :": k.acc_holder_name,
                  "Email :" :k.acc_email,
                  "Credit :" :k.credit,
                  "Debit :" : k.debit,
                  "Balance" : k.balance

        }
        keyvalue1.append(count)
        trans.append(CountryCodeDict1)



        print("-" * 50)
        trans.append(k.acc_email)
        trans.append(k.acc_holder_name)
        print(k.acc_holder_name)
        trans.append(k.balance)
        print(k.balance)



    return render_template('show_user.html',len = len(trans), trans = trans,CountryCodeDict1=CountryCodeDict1,
                           leen =len(keyvalue1), keyvalue1=keyvalue1
                           )


@app.route("/showdetails", methods=["GET", "POST"])
def showdetails():
    if request.method == 'POST':
        username = request.form['USERNAME']
        print(username)
        acc = user.query.filter_by(username=username)
        acc_holder_name = acc.one().username
        acc_email = acc.one().email
        acc_numb = acc.one().phonenumber
        balance = 1000
        print(acc_holder_name)
        print(acc_email)
        print(acc_numb)
        print(type(acc_numb))


        # showdetails = acc_details(acc_numb=acc_numb, acc_holder_name=acc_holder_name, acc_email=acc_email,
        #                           balance=balance)
        # db.session.add(showdetails)
        # db.session.commit()
        # print(acc, acc_holder_name, acc_email, acc_numb, balance)
        return render_template('show_user.html', acc=acc, acc_holder_name=acc_holder_name, acc_email=acc_email,
                               acc_numb=acc_numb,
                               balance=balance)

    return render_template('homepage.html')


@app.route('/withdrawal', methods=['GET', 'POST'])
def withdrawal():
    if request.method == 'POST':
        withdrawal = request.form['WITHDRAWAL']

        jj = withdrawal

        # jj = acc_details.query.filter_by(acc_email='sudharsanpilot@gmail.com')
        jjj = main_balance.query.filter_by(acc_holder_name=session['uname'])
        print(session['uname'])
        # print(jj.one().balance)
        oldbalance = jjj.one().main_money_balance
        print(oldbalance)
        if int(withdrawal) > int(oldbalance) :
            message = "Sorry "+ str(withdrawal)+" out of balance, Your Account Balance is = "+ str(oldbalance)
            return render_template('withdrawal.html', message=message)
        else:
            print('#--' * 20)
            print(withdrawal)
            Newbalance = int(oldbalance) - int(withdrawal)
            print(Newbalance)
            print('#--' * 20)
            acc = user.query.filter_by(username=session['uname'])
            acc_holder_name = acc.one().username
            acc_email = acc.one().email
            acc_numb = acc.one().phonenumber

            withdrawal = acc_details(acc_numb=acc_numb, acc_holder_name=acc_holder_name, acc_email=acc_email,
                                     balance=Newbalance, debit="debit")
            db.session.add(withdrawal)
            db.session.commit()
            updatee = main_balance.query.filter_by(acc_holder_name=session['uname']).first()
            updatee.main_money_balance = Newbalance
            db.session.commit()
            message = "Successfully "+ str(jj) +" withdrawal"
            show_balance = main_balance.query.filter_by(acc_holder_name=session['uname']).first()

            ba = show_balance.main_money_balance

            return render_template('withdrawal.html', message=message,ba=ba)


    return render_template('homepage.html')


@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        deposit = request.form['DEPOSIT']
        # jj = acc_details.query.filter_by(acc_email='sudharsanpilot@gmail.com')
        jjj = main_balance.query.filter_by(acc_holder_name=session['uname'])
        print(session['uname'])
        # print(jj.one().balance)
        oldbalance = jjj.one().main_money_balance
        print(oldbalance)
        amo = deposit

        print('#--' * 20)
        print(deposit)
        Newbalance = int(oldbalance) + int(deposit)
        print(Newbalance)
        print('#--' * 20)
        acc = user.query.filter_by(username=session['uname'])
        acc_holder_name = acc.one().username
        acc_email = acc.one().email
        acc_numb = acc.one().phonenumber

        deposit = acc_details(acc_numb=acc_numb, acc_holder_name=acc_holder_name, acc_email=acc_email,
                              balance=Newbalance,credit="credit")
        db.session.add(deposit)
        db.session.commit()
        updatee = main_balance.query.filter_by(acc_holder_name=session['uname']).first()
        updatee.main_money_balance = Newbalance
        db.session.commit()
        show_balance = main_balance.query.filter_by(acc_holder_name=session['uname']).first()

        ba = show_balance.main_money_balance

        return render_template('deposit.html',ba=ba,amo=amo)
    return render_template('homepage.html')

@app.route("/transhistroy")
def transhistroy():
    allemail = acc_details.query.filter(acc_details.acc_holder_name.endswith(session['uname'])).all()
    print('EEEE--' * 10)
    # allemaillll = acc_details.query.filter(acc_details.acc_holder_name.endswith(session['uname'])).all()
    trans = []
    keyvalue1 = []

    # print(u.acc_email)
    print('EEEEE--' * 10)
    for k in allemail:
        print(k.acc_email)
        print("-" * 20)
        CountryCodeDict1 = {k.acc_holder_name: [k.acc_email, k.credit, k.debit, k.balance]}
        count = {"Name :": k.acc_holder_name,
                 "Email :": k.acc_email,
                 "Credit :": k.credit,
                 "Debit :": k.debit,
                 "Balance": k.balance

                 }
        keyvalue1.append(count)
        trans.append(CountryCodeDict1)

        print("-" * 50)
        trans.append(k.acc_email)
        trans.append(k.acc_holder_name)
        print(k.acc_holder_name)
        trans.append(k.balance)
        print(k.balance)

    return render_template('transhistroy.html',leen=len(keyvalue1), keyvalue1=keyvalue1)


@app.route("/returnpage")
def returnpage():
    jj = user.query.filter_by(username=session['uname'])
    ss = jj.one().email
    vv = jj.one().username
    ll = jj.one().phonenumber
    show_balance = main_balance.query.filter_by(acc_holder_name=session['uname']).first()

    ba = show_balance.main_money_balance


    return render_template('homepage.html', vv=vv, ss=ss, ll=ll,ba=ba)

@app.route("/features")
def features():
    jj = user.query.filter_by(username=session['uname'])
    ss = jj.one().email
    vv = jj.one().username
    ll = jj.one().phonenumber


    return render_template('features.html', vv=vv, ss=ss, ll=ll)







@app.route("/logout")
def logout():
    session.pop("uname", None)
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5016)
