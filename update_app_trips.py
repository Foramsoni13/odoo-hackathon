with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

new_routes = '''# ---------------- MY TRIPS ----------------
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

# ---------------- LOGOUT ----------------'''

app_py = app_py.replace('# ---------------- LOGOUT ----------------', new_routes)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)
print('Updated app.py with my-trips routes')
