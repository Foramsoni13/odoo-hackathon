import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

old_route = '''# ---------------- VIEW TRIP ----------------
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
    return redirect("/login")'''

new_route = '''# ---------------- VIEW TRIP (PUBLIC) ----------------
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
            
    return render_template("view_trip.html", user=session.get("user"), trip=trip, is_owner=is_owner, creator=creator)'''

app_py = app_py.replace(old_route, new_route)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)
print("Updated /view-trip route to be public")
