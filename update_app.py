import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

# 1. Inject Models
models_code = '''class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.LargeBinary)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    country = db.Column(db.String(50))
    price = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50))

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    date_range = db.Column(db.String(50))
    budget = db.Column(db.Integer)
    status = db.Column(db.String(20))
    image_url = db.Column(db.String(255))
    people_avatars = db.Column(db.String(255))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    icon = db.Column(db.String(10))
    title = db.Column(db.String(100))
    message = db.Column(db.String(255))
'''

# Find the User model and replace it with all models
app_py = re.sub(r'class User\(db\.Model\):.*?(?=\nwith app\.app_context\(\):)', models_code + '\n', app_py, flags=re.DOTALL)

# 2. Update home route
old_home = '''@app.route("/home")
def home():
    if session.get("user"):
        return render_template("home.html", user=session["user"])
    return redirect("/login")'''

new_home = '''@app.route("/home")
def home():
    if session.get("user"):
        user = User.query.filter_by(name=session["user"]).first()
        if not user:
            return redirect("/login")
        
        destinations = Destination.query.all()
        trips = Trip.query.filter_by(user_id=user.id).all()
        notifications = Notification.query.filter_by(user_id=user.id).all()
        
        return render_template("home.html", user=session["user"], destinations=destinations, trips=trips, notifications=notifications)
    return redirect("/login")'''

app_py = app_py.replace(old_home, new_home)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)
print('Updated app.py')
