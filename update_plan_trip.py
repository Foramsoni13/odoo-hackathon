import re

# 1. UPDATE plan_trip.html
with open('templates/plan_trip.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add name attributes
html = html.replace('<form action="/home">', '<form action="/plan-trip" method="POST">')
html = html.replace('<input type="text" class="form-control" placeholder="E.g., Tokyo, Japan" required>', '<input type="text" class="form-control" name="destination" placeholder="E.g., Tokyo, Japan" required>')
html = html.replace('<input type="date" class="form-control" required>', '<input type="date" class="form-control" name="start_date" required>', 1)
html = html.replace('<input type="date" class="form-control" required>', '<input type="date" class="form-control" name="end_date" required>', 1)
html = html.replace('<input type="number" class="form-control" placeholder="2" min="1" required>', '<input type="number" class="form-control" name="people" placeholder="2" min="1" required>')
html = html.replace('<input type="number" class="form-control" placeholder="100000" min="0" required>', '<input type="number" class="form-control" name="budget" placeholder="100000" min="0" required>')
html = html.replace('<select class="form-control">', '<select class="form-control" name="category">')

with open('templates/plan_trip.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. UPDATE app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

old_plan = '''@app.route("/plan-trip")
def plan_trip():
    if session.get("user"):
        return render_template("plan_trip.html", user=session["user"])
    return redirect("/login")'''

new_plan = '''import datetime
@app.route("/plan-trip", methods=["GET", "POST"])
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

app_py = app_py.replace(old_plan, new_plan)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)
print('Updated plan_trip logic')
