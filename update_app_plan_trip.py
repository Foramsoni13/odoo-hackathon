import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

# 1. Add description to Trip model
old_trip_model = '''class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    date_range = db.Column(db.String(50))
    budget = db.Column(db.Integer)
    status = db.Column(db.String(20))
    image_url = db.Column(db.String(255))
    people_avatars = db.Column(db.String(255))
    stops = db.relationship('Stop', backref='trip', lazy=True, cascade='all, delete-orphan')'''

new_trip_model = '''class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    date_range = db.Column(db.String(50))
    budget = db.Column(db.Integer)
    status = db.Column(db.String(20))
    image_url = db.Column(db.String(255))
    people_avatars = db.Column(db.String(255))
    description = db.Column(db.String(500))
    stops = db.relationship('Stop', backref='trip', lazy=True, cascade='all, delete-orphan')'''

app_py = app_py.replace(old_trip_model, new_trip_model)

# 2. Update /plan-trip route
old_route = '''@app.route("/plan-trip", methods=["GET", "POST"])
def plan_trip():
    if not session.get("user"):
        return redirect("/login")

    user = User.query.filter_by(name=session["user"]).first()
    if not user:
        return redirect("/login")

    if request.method == "POST":
        destination = request.form.get("destination")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        people = int(request.form.get("people", 1))
        budget = int(request.form.get("budget", 0))
        
        # Format dates (e.g., "2025-06-15" to "Jun 15")
        try:
            sd = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            ed = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            date_range = f"{sd.strftime('%b %d')} – {ed.strftime('%b %d, %Y')}"
        except:
            date_range = f"{start_date} to {end_date}"
        
        # Generate random avatars
        colors = ["#6366f1", "#f472b6", "#34d399", "#8b5cf6", "#f59e0b", "#0ea5e9"]
        import random
        avatars = ",".join([random.choice(colors) for _ in range(min(people, 4))])

        trip = Trip(
            user_id=user.id,
            name=destination,
            date_range=date_range,
            budget=budget,
            status="planned",
            image_url="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400&q=80",
            people_avatars=avatars
        )
        db.session.add(trip)
        db.session.commit()
        
        return redirect("/home")

    return render_template("plan_trip.html", user=session["user"])'''

new_route = '''@app.route("/plan-trip", methods=["GET", "POST"])
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
    return render_template("plan_trip.html", user=session["user"], destinations=destinations)'''

app_py = app_py.replace(old_route, new_route)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)
print("Updated app.py for /plan-trip route")
