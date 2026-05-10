import sys
sys.stdout.reconfigure(encoding='utf-8')
from app import app, db, User, Destination, Trip, Stop, Activity, Notification

with app.app_context():
    print('='*60)
    print('USERS')
    print('='*60)
    for u in User.query.all():
        print(f'  ID:{u.id} | Name:{u.name} | Email:{u.email}')
    
    print()
    print('='*60)
    print('DESTINATIONS')
    print('='*60)
    for d in Destination.query.all():
        print(f'  ID:{d.id} | {d.name} ({d.country}) | Rs.{d.price} | {d.category}')
    
    print()
    print('='*60)
    print('TRIPS')
    print('='*60)
    for t in Trip.query.all():
        print(f'  ID:{t.id} | {t.name} | {t.date_range} | Budget:{t.budget} | Status:{t.status}')
    
    print()
    print('='*60)
    print('STOPS')
    print('='*60)
    for s in Stop.query.all():
        print(f'  ID:{s.id} | Trip#{s.trip_id} | {s.city_name} | {s.arrival_date} - {s.departure_date}')
    
    print()
    print('='*60)
    print('ACTIVITIES')
    print('='*60)
    for a in Activity.query.all():
        print(f'  ID:{a.id} | Stop#{a.stop_id} | {a.name} | Rs.{a.cost} | {a.time_of_day}')
    
    print()
    print('='*60)
    print('NOTIFICATIONS')
    print('='*60)
    for n in Notification.query.all():
        print(f'  ID:{n.id} | {n.icon} {n.title}: {n.message}')
