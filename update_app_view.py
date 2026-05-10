with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

route = '''
# ---------------- VIEW TRIP ----------------
@app.route("/view-trip/<int:trip_id>")
def view_trip(trip_id):
    if session.get("user"):
        user = User.query.filter_by(name=session["user"]).first()
        if not user:
            return redirect("/login")
        trip = Trip.query.filter_by(id=trip_id, user_id=user.id).first()
        if not trip:
            return redirect("/my-trips")
        return render_template("view_trip.html", user=session["user"], trip=trip)
    return redirect("/login")
'''

app_py = app_py.replace('# ---------------- ITINERARY BUILDER ----------------', route + '\n# ---------------- ITINERARY BUILDER ----------------')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)
print("Added view_trip route")
