from functions import *

@app.route('/cancel', methods=['GET', 'POST'])
def index():
    if isLogin():
        return redirect('/manage')
    session.clear()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = refresh_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email = %s LIMIT 1", (email,))
        user = cursor.fetchone()
        if (user != None and verifyPassword(password, user[1])):
            cursor.execute("DELETE FROM users WHERE email = %s LIMIT 1", (email,))
            cursor.execute("DELETE FROM schedule WHERE user_id = %s", (user[0],))
            db.commit()
            flash("SUCC-We've cancelled your notifications.")
            return redirect('/')
        else:
            flash("User not found.")
    return render_template('cancel.html')

@app.route('/', methods=['GET', 'POST'])
def signup():
    if isLogin():
        return redirect('/manage')
    session.clear()
    if request.method == 'POST':
        email = request.form['email']
        password = genHash(request.form['password'])
        db = refresh_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        db.commit()
        cursor.close()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        user_id = cursor.fetchone()[0]
        try:
            # get csv
            csv_file = request.files['schedule']
            filepath = os.path.join('./temp', csv_file.filename)
            csv_file.save(filepath)
            csv_dict = pd.read_csv(filepath)
            periodCodes = csv_dict['Period Day'].tolist()
            for i in range(5):
                tmp_csv = csv_dict[str(i+1)].tolist()
                for j in range(len(tmp_csv)):
                    if not (periodCodes[j].endswith('-t')):
                        if type(tmp_csv[j]) == float:
                            db = refresh_db()
                            cursor = db.cursor(buffered=True)
                            cursor.execute("""
                                INSERT IGNORE INTO schedule
                                (user_id, dow, period, subject, url)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (user_id, str(i+1), periodCodes[j], '--', '--'))
                            db.commit()
                            cursor.close()
                        else:
                            db = refresh_db()
                            cursor = db.cursor(buffered=True)
                            cursor.execute("""
                                INSERT IGNORE INTO schedule
                                (user_id, dow, period, subject)
                                VALUES (%s, %s, %s, %s)
                            """, (user_id, str(i+1), periodCodes[j], tmp_csv[j]))
                            db.commit()
                            cursor.close()
                            if not(periodCodes[j] == 'n'):
                                j += 1
                                db = refresh_db()
                                cursor = db.cursor(buffered=True)
                                cursor.execute("""
                                    UPDATE schedule
                                    SET url = %s
                                    WHERE user_id = %s AND dow = %s AND period = %s
                                """, (tmp_csv[j], user_id, str(i+1), periodCodes[j-1]))
                                db.commit()
                                cursor.close()
                            else:
                                db = refresh_db()
                                cursor = db.cursor(buffered=True)
                                cursor.execute("""
                                    UPDATE schedule
                                    SET url = %s
                                    WHERE user_id = %s AND dow = %s AND period = %s
                                """, ("--", user_id, str(i+1), periodCodes[j]))
                                db.commit()
                                cursor.close()
            os.remove(filepath)
        except Exception as e:
            os.remove(filepath)
            return "Error. Please try again\n("+str(e)+")"
        session['email'] = email
        session['uid'] = user_id
        return render_template("askperms.html")
    return render_template('signup.html')

@app.route('/manifest.json')
def manifest():
    return send_file('static/manifest.json')

@app.route('/sw.js')
def sw():
    return send_file('static/sw.js')

@app.route('/vapidkey')
def vapid():
    return os.environ.get('VAPID_PUBLIC')

@app.route('/storeendpoint', methods=['POST'])
def storeendpoint():
    db = refresh_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET epoint=%s WHERE id=%s AND email=%s LIMIT 1", (json.dumps(request.json['sub']), session['uid'], session['email']))
    db.commit()
    cursor.close()
    return "ok"

@app.route('/sendNotif', methods=['GET'])
def sendNotif():
    session.clear()
    # get current time
    now = datetime.now().strftime('%H:%M')
    # set time to 7:55am
    for key, value in PERIODS.items():
        if now <= value:
            period = key
            break
    db = refresh_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id, subject, url FROM schedule WHERE dow = %s AND period = %s", (str(datetime.today().weekday()+1), period))
    data = cursor.fetchall()
    if data is None:
        abort(404)
    for d in data:
        user_id = d[0]
        subject = d[1]
        url = d[2]
        cursor.execute("SELECT epoint FROM users WHERE id = %s", (user_id,))
        endpoint = cursor.fetchone()[0]
        options = {
            'title': str(period + ': ' + subject),
            'link': url,
        }
        try:
            webpush(subscription_info=json.loads(endpoint), data=json.dumps(options), vapid_private_key=os.environ.get('VAPID_PRIVATE'), vapid_claims={"sub": "mailto:longyklee@gmail.com"})
        except Exception as e:
            return e
    return ("ok")