from app import app, db, User, Destination, Trip, Notification

with app.app_context():
    db.create_all()

    # Clear existing data
    Destination.query.delete()
    Trip.query.delete()
    Notification.query.delete()

    user = User.query.filter_by(name="Kushal").first()
    if not user:
        user = User.query.first() # fallback if Kushal doesn't exist

    if user:
        print(f"Seeding data for user: {user.name}")
        
        # 1. Destinations
        d1 = Destination(name="Venice", country="Italy 🇮🇹", price=70000, category="romantic", image_url="https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=400&q=80")
        d2 = Destination(name="Santorini", country="Greece 🇬🇷", price=95000, category="scenic", image_url="https://images.unsplash.com/photo-1580674285054-bed31e145f59?w=400&q=80")
        d3 = Destination(name="Dubai", country="UAE 🇦🇪", price=60000, category="luxury", image_url="https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&q=80")
        d4 = Destination(name="Rio de Janeiro", country="Brazil 🇧🇷", price=78000, category="adventure", image_url="https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=400&q=80")
        db.session.add_all([d1, d2, d3, d4])

        # 2. Trips
        t1 = Trip(user_id=user.id, name="Bali, Indonesia", date_range="Jun 15 – Jun 22, 2025", budget=95000, status="upcoming", image_url="https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=400&q=80", people_avatars="#6366f1,#f472b6,#34d399")
        t2 = Trip(user_id=user.id, name="Paris, France", date_range="Aug 5 – Aug 12, 2025", budget=225000, status="planned", image_url="https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&q=80", people_avatars="#8b5cf6,#f59e0b")
        t3 = Trip(user_id=user.id, name="Tokyo, Japan", date_range="May 8 – May 18, 2025", budget=250000, status="ongoing", image_url="https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&q=80", people_avatars="#0ea5e9")
        db.session.add_all([t1, t2, t3])

        # 3. Notifications
        n1 = Notification(user_id=user.id, icon="🌴", title="Bali Trip", message="Your trip is upcoming in 30 days!")
        n2 = Notification(user_id=user.id, icon="💰", title="Budget Alert", message="You've used 80% of your Bali budget.")
        db.session.add_all([n1, n2])

        db.session.commit()
        print("Database seeded successfully!")
    else:
        print("No users found to seed trips/notifications.")
