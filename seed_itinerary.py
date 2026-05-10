from app import app, db, User, Trip, Stop, Activity

with app.app_context():
    user = User.query.filter_by(name="Kushal").first()
    if user:
        # Find Bali trip
        trip = Trip.query.filter_by(user_id=user.id, name="Bali, Indonesia").first()
        if trip:
            # Clear existing stops
            for stop in trip.stops:
                db.session.delete(stop)
            db.session.commit()

            # Add Stop 1: Ubud
            s1 = Stop(trip_id=trip.id, city_name="Ubud", arrival_date="Jun 15", departure_date="Jun 18, 2025")
            db.session.add(s1)
            db.session.commit() # commit to get s1.id

            # Add Activities for Ubud
            a1 = Activity(stop_id=s1.id, name="Visit Sacred Monkey Forest", cost=500, time_of_day="Morning")
            a2 = Activity(stop_id=s1.id, name="Tegallalang Rice Terrace Trek", cost=200, time_of_day="Afternoon")
            a3 = Activity(stop_id=s1.id, name="Dinner at Locavore", cost=4500, time_of_day="Evening")
            db.session.add_all([a1, a2, a3])

            # Add Stop 2: Seminyak
            s2 = Stop(trip_id=trip.id, city_name="Seminyak", arrival_date="Jun 18", departure_date="Jun 22, 2025")
            db.session.add(s2)
            db.session.commit()

            a4 = Activity(stop_id=s2.id, name="Potato Head Beach Club", cost=3000, time_of_day="Afternoon")
            db.session.add(a4)

            db.session.commit()
            print("Seeded itinerary for Bali!")
