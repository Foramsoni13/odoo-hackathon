from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import random

app = Flask(__name__)
app.secret_key = "hackathon_secret_key_123"

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hack_user:hack123@localhost/hackathon_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODEL
class User(db.Model):
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
    description = db.Column(db.String(500))
    stops = db.relationship('Stop', backref='trip', lazy=True, cascade='all, delete-orphan')


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    city_name = db.Column(db.String(100))
    arrival_date = db.Column(db.String(50))
    departure_date = db.Column(db.String(50))
    activities = db.relationship('Activity', backref='stop', lazy=True, cascade="all, delete-orphan")

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stop.id'))
    name = db.Column(db.String(150))
    cost = db.Column(db.Integer)
    time_of_day = db.Column(db.String(50))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    icon = db.Column(db.String(10))
    title = db.Column(db.String(100))
    message = db.Column(db.String(255))


with app.app_context():
    db.create_all()

# ---------------- SPLASH ----------------
@app.route("/")
def splash():
    return render_template("splash.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email")

        if not email:
            return render_template("login.html", error="Enter email first")

        user = User.query.filter_by(email=email).first()

        # LOGIN
        if action == "login":
            password = request.form.get("password")

            if not user:
                return render_template("login.html", error="Email not registered")

            if not bcrypt.checkpw(password.encode('utf-8'), user.password):
                return render_template("login.html", error="Wrong password")

            session["user"] = user.name
            return redirect("/home")

        # FORGOT PASSWORD
        if action == "forgot":

            if not user:
                return render_template("login.html", error="Email not registered")

            otp = str(random.randint(100000, 999999))

            session["otp"] = otp
            session["reset_email"] = email

            print("OTP:", otp)

            return redirect("/verify-otp")

    return render_template("login.html")


# ---------------- VERIFY OTP ----------------
@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if "otp" not in session:
        return redirect("/login")

    if request.method == "POST":
        otp = request.form.get("otp")

        if otp == session.get("otp"):
            return redirect("/reset-password")
        else:
            return render_template("verify_otp.html", error="Invalid OTP")

    return render_template("verify_otp.html")


# ---------------- RESET PASSWORD ----------------
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if "reset_email" not in session:
        return redirect("/login")

    if request.method == "POST":
        new_password = request.form.get("password")

        if not new_password:
            return render_template("reset_password.html", error="Enter password")

        user = User.query.filter_by(email=session["reset_email"]).first()

        hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_pw
        db.session.commit()

        session.clear()

        # Redirect to home after reset, logging them in could also be done here but for now just redirect to login so they can log in with new password
        return redirect("/login")

    return render_template("reset_password.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name") or request.form.get("firstname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password != confirm:
            return "Passwords do not match"

        if User.query.filter_by(email=email).first():
            return "User already exists"

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        db.session.add(User(name=name, email=email, password=hashed_pw))
        db.session.commit()
        
        # Log the user in after registration
        session["user"] = name

        return redirect("/home")

    return render_template("register.html")


# ---------------- HOME ----------------
@app.route("/home")
def home():
    if session.get("user"):
        user = User.query.filter_by(name=session["user"]).first()
        if not user:
            return redirect("/login")
        
        destinations = Destination.query.all()
        trips = Trip.query.filter_by(user_id=user.id).all()
        notifications = Notification.query.filter_by(user_id=user.id).all()
        
        return render_template("home.html", user=session["user"], destinations=destinations, trips=trips, notifications=notifications)
    return redirect("/login")

# ---------------- PLAN A TRIP ----------------
import datetime
@app.route("/plan-trip", methods=["GET", "POST"])
def plan_trip():
    if not session.get("user"):
        return redirect("/login")

    user = User.query.filter_by(name=session["user"]).first()
    if not user:
        return redirect("/login")

    if request.method == "POST":
        trip_name = request.form.get("trip_name")
        destination = request.form.get("destination")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        description = request.form.get("description")
        cover_photo = request.form.get("cover_photo")
        
        if not cover_photo:
            cover_photo = "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400&q=80"
            
        try:
            sd = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            ed = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            date_range = f"{sd.strftime('%b %d')} – {ed.strftime('%b %d, %Y')}"
        except:
            date_range = f"{start_date} to {end_date}"
        
        colors = ["#6366f1", "#f472b6", "#34d399", "#8b5cf6", "#f59e0b", "#0ea5e9"]
        import random
        avatars = ",".join([random.choice(colors) for _ in range(2)]) # Default to 2 avatars

        trip = Trip(
            user_id=user.id,
            name=trip_name or destination,
            date_range=date_range,
            budget=0,
            status="planned",
            image_url=cover_photo,
            people_avatars=avatars,
            description=description
        )
        db.session.add(trip)
        db.session.commit()
        
        return redirect("/home")

    destinations = Destination.query.all()
    return render_template("plan_trip.html", user=session["user"], destinations=destinations)


# ---------------- MY TRIPS ----------------
@app.route("/my-trips")
def my_trips():
    if session.get("user"):
        user = User.query.filter_by(name=session["user"]).first()
        if not user:
            return redirect("/login")
        trips = Trip.query.filter_by(user_id=user.id).all()
        return render_template("my_trips.html", user=session["user"], trips=trips)
    return redirect("/login")

# ---------------- DELETE TRIP ----------------
@app.route("/delete-trip/<int:trip_id>", methods=["POST"])
def delete_trip(trip_id):
    if session.get("user"):
        user = User.query.filter_by(name=session["user"]).first()
        if user:
            trip = Trip.query.filter_by(id=trip_id, user_id=user.id).first()
            if trip:
                db.session.delete(trip)
                db.session.commit()
    return redirect("/my-trips")


# ---------------- VIEW TRIP (PUBLIC) ----------------
@app.route("/view-trip/<int:trip_id>")
def view_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return "Trip not found", 404
        
    is_owner = False
    current_user = None
    if session.get("user"):
        current_user = User.query.filter_by(name=session["user"]).first()
        if current_user and trip.user_id == current_user.id:
            is_owner = True
            
    # For a public page, we might want to know who created it
    creator = User.query.get(trip.user_id)
            
    return render_template("view_trip.html", user=session.get("user"), trip=trip, is_owner=is_owner, creator=creator)

# ---------------- ITINERARY BUILDER ----------------
@app.route("/itinerary-builder/<int:trip_id>")
def itinerary_builder(trip_id):
    if session.get("user"):
        user = User.query.filter_by(name=session["user"]).first()
        if not user:
            return redirect("/login")
        trip = Trip.query.filter_by(id=trip_id, user_id=user.id).first()
        if not trip:
            return redirect("/my-trips")
        return render_template("itinerary_builder.html", user=session["user"], trip=trip)
    return redirect("/login")

@app.route("/add-stop/<int:trip_id>", methods=["POST"])
def add_stop(trip_id):
    if session.get("user"):
        user = User.query.filter_by(name=session["user"]).first()
        trip = Trip.query.filter_by(id=trip_id, user_id=user.id).first()
        if trip:
            city_name = request.form.get("city_name")
            arrival_date = request.form.get("arrival_date")
            departure_date = request.form.get("departure_date")
            if city_name and arrival_date and departure_date:
                # Basic formatting just to keep it nice looking
                try:
                    import datetime
                    ad = datetime.datetime.strptime(arrival_date, "%Y-%m-%d").strftime("%b %d")
                    dd = datetime.datetime.strptime(departure_date, "%Y-%m-%d").strftime("%b %d, %Y")
                except:
                    ad = arrival_date
                    dd = departure_date
                
                stop = Stop(trip_id=trip.id, city_name=city_name, arrival_date=ad, departure_date=dd)
                db.session.add(stop)
                db.session.commit()
    return redirect(f"/itinerary-builder/{trip_id}")

@app.route("/add-activity/<int:stop_id>", methods=["POST"])
def add_activity(stop_id):
    if session.get("user"):
        user = User.query.filter_by(name=session["user"]).first()
        stop = Stop.query.get(stop_id)
        if stop and stop.trip.user_id == user.id:
            name = request.form.get("name")
            cost = int(request.form.get("cost", 0))
            time_of_day = request.form.get("time_of_day")
            if name and time_of_day:
                activity = Activity(stop_id=stop.id, name=name, cost=cost, time_of_day=time_of_day)
                db.session.add(activity)
                db.session.commit()
    return redirect(request.referrer)

# ---------------- SEARCH ----------------
@app.route("/search")
def search():
    if not session.get("user"):
        return redirect("/login")

    query = request.args.get("q", "").strip()
    group_by = request.args.get("group_by", "")
    filter_by = request.args.get("filter", "")
    sort_by = request.args.get("sort_by", "")

    destinations = Destination.query

    if query:
        destinations = destinations.filter(
            db.or_(
                Destination.name.ilike(f"%{query}%"),
                Destination.country.ilike(f"%{query}%"),
                Destination.category.ilike(f"%{query}%")
            )
        )

    if filter_by:
        destinations = destinations.filter(Destination.category.ilike(f"%{filter_by}%"))

    if sort_by == "price_low":
        destinations = destinations.order_by(Destination.price.asc())
    elif sort_by == "price_high":
        destinations = destinations.order_by(Destination.price.desc())
    elif sort_by == "name":
        destinations = destinations.order_by(Destination.name.asc())

    results = destinations.all()

    grouped = {}
    if group_by == "country":
        for d in results:
            grouped.setdefault(d.country, []).append(d)
    elif group_by == "category":
        for d in results:
            grouped.setdefault(d.category.title(), []).append(d)

    categories = db.session.query(Destination.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return render_template("search.html", user=session["user"], results=results,
                           query=query, group_by=group_by, filter_by=filter_by,
                           sort_by=sort_by, grouped=grouped, categories=categories)

# ---------------- COMMUNITY ----------------
@app.route("/community")
def community():
    if not session.get("user"):
        return redirect("/login")
        
    # Get all trips (in a real app this would filter for is_public=True)
    all_trips = Trip.query.all()
    
    # We need to pass creator info for each trip
    trips_data = []
    for trip in all_trips:
        creator = User.query.get(trip.user_id)
        if creator:
            trips_data.append({
                "trip": trip,
                "creator": creator
            })
            
    return render_template("community.html", user=session["user"], trips_data=trips_data)

# ---------------- PROFILE ----------------
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("user"):
        return redirect("/login")

    user = User.query.filter_by(name=session["user"]).first()
    if not user:
        return redirect("/login")

    if request.method == "POST":
        new_name = request.form.get("name")
        new_email = request.form.get("email")
        if new_name:
            user.name = new_name
            session["user"] = new_name
        if new_email:
            user.email = new_email
        db.session.commit()
        return redirect("/profile")

    all_trips = Trip.query.filter_by(user_id=user.id).all()
    preplanned_trips = [t for t in all_trips if t.status in ("planned", "upcoming", "ongoing")]
    previous_trips = [t for t in all_trips if t.status == "completed"]

    return render_template("profile.html", user=session["user"], user_obj=user,
                           preplanned_trips=preplanned_trips, previous_trips=previous_trips)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)