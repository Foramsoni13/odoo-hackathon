import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Notifications
old_notifs = '''        <div class="notif-header">Notifications (2)</div>
        <div class="notif-body">
          <div class="notif-item">
            <div class="notif-icon">🌴</div>
            <div class="notif-text"><strong>Bali Trip</strong><br>Your trip is upcoming in 30 days!</div>
          </div>
          <div class="notif-item">
            <div class="notif-icon">💰</div>
            <div class="notif-text"><strong>Budget Alert</strong><br>You've used 80% of your Bali budget.</div>
          </div>
        </div>'''
new_notifs = '''        <div class="notif-header">Notifications ({{ notifications|length }})</div>
        <div class="notif-body">
          {% for notif in notifications %}
          <div class="notif-item">
            <div class="notif-icon">{{ notif.icon }}</div>
            <div class="notif-text"><strong>{{ notif.title }}</strong><br>{{ notif.message }}</div>
          </div>
          {% else %}
          <div style="padding: 14px 18px; color: var(--muted); font-size: 13px;">No new notifications.</div>
          {% endfor %}
        </div>'''
html = html.replace(old_notifs, new_notifs)

old_badge = '''<div class="notif-btn" id="notifBtn">🔔<span class="notif-badge">2</span></div>'''
new_badge = '''<div class="notif-btn" id="notifBtn">🔔{% if notifications|length > 0 %}<span class="notif-badge">{{ notifications|length }}</span>{% endif %}</div>'''
html = html.replace(old_badge, new_badge)

# 2. Update Destinations
# We need to replace the entire <div class="dest-grid"> content
dest_grid_pattern = re.compile(r'<div class="dest-grid">.*?</div>\n\n  <!-- BUDGET \+ TIPS -->', re.DOTALL)
new_dest_grid = '''<div class="dest-grid">
    {% for dest in destinations %}
    <div class="dest-card" data-name="{{ dest.name }} {{ dest.country }}" data-price="{{ dest.price }}" data-cat="{{ dest.category }}" data-type="dest">
      <img src="{{ dest.image_url }}" alt="{{ dest.name }}">
      <div class="dest-overlay"></div>
      <div class="dest-price">from ₹{{ "{:,}".format(dest.price) }}</div>
      <div class="dest-info">
        <div class="dest-city">{{ dest.name }}</div>
        <div class="dest-country">{{ dest.country }}</div>
        <span class="dest-tag">{{ dest.category.title() }}</span>
      </div>
    </div>
    {% endfor %}
  </div>

  <!-- BUDGET + TIPS -->'''
html = dest_grid_pattern.sub(new_dest_grid, html)

# 3. Update Trips
# We need to replace the entire <div class="trips-grid"> content
trips_grid_pattern = re.compile(r'<div class="trips-grid">.*?</div>\n\n  <!-- QUICK ACTIONS -->', re.DOTALL)
new_trips_grid = '''<div class="trips-grid">
    {% for trip in trips %}
    <div class="trip-card" data-name="{{ trip.name }}" data-price="{{ trip.budget }}" data-status="{{ trip.status }}" data-type="trip">
      <div class="trip-img">
        <img src="{{ trip.image_url }}" alt="{{ trip.name }}">
        <span class="trip-badge badge-{{ trip.status }}">{{ trip.status.title() }}</span>
      </div>
      <div class="trip-body">
        <div class="trip-city">✈️ {{ trip.name }}</div>
        <div class="trip-dates">📅 {{ trip.date_range }}</div>
        <div class="trip-meta">
          <div class="trip-people">
            {% for color in trip.people_avatars.split(',') %}
            <div class="av" style="background:{{ color }};"></div>
            {% endfor %}
          </div>
          <div class="trip-budget">₹{{ "{:,}".format(trip.budget) }}</div>
        </div>
      </div>
    </div>
    {% else %}
    <div style="color: var(--muted); grid-column: 1 / -1; text-align: center; padding: 40px;">No previous trips. <a href="/plan-trip" style="color: var(--accent1);">Plan one now!</a></div>
    {% endfor %}
  </div>

  <!-- QUICK ACTIONS -->'''
html = trips_grid_pattern.sub(new_trips_grid, html)

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated home.html with Jinja logic')
