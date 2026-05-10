with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

# 1. Update Trip model to have stops relationship
old_trip = "people_avatars = db.Column(db.String(255))"
new_trip = "people_avatars = db.Column(db.String(255))\n    stops = db.relationship('Stop', backref='trip', lazy=True, cascade='all, delete-orphan')"
app_py = app_py.replace(old_trip, new_trip)

# 2. Add Stop and Activity models
models = '''
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
'''

app_py = app_py.replace('class Notification(db.Model):', models + '\nclass Notification(db.Model):')

# 3. Add Routes
routes = '''# ---------------- ITINERARY BUILDER ----------------
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

'''

app_py = app_py.replace('# ---------------- LOGOUT ----------------', routes + '# ---------------- LOGOUT ----------------')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)
print('Updated app.py with itinerary routes and models')
