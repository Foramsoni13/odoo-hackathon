import re
with open('templates/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS
css_to_add = '''
/* CONTROL BAR */
.control-bar{display:flex;align-items:center;gap:12px;margin-bottom:40px;}
.ctrl-search{flex:1;position:relative;background:var(--surface);border:1px solid var(--border);border-radius:14px;display:flex;align-items:center;padding:0 16px;height:48px;}
.ctrl-search input{background:none;border:none;color:#fff;font-size:15px;width:100%;outline:none;margin-left:10px;font-family:'Outfit',sans-serif;}
.ctrl-search input::placeholder{color:var(--muted);}
.ctrl-btn{height:48px;padding:0 20px;background:var(--surface);border:1px solid var(--border);border-radius:14px;color:#fff;font-size:14px;font-weight:500;cursor:pointer;font-family:'Outfit',sans-serif;transition:.2s;}
.ctrl-btn:hover{background:rgba(255,255,255,0.08);}

/* FLOATING BTN */
.floating-btn{position:fixed;bottom:30px;right:30px;background:linear-gradient(135deg,#db2777,#7c3aed);border:none;border-radius:99px;padding:16px 28px;color:#fff;font-family:'Outfit',sans-serif;font-size:16px;font-weight:600;box-shadow:0 10px 25px rgba(219,39,119,0.4);cursor:pointer;text-decoration:none;z-index:100;transition:.3s;display:flex;align-items:center;gap:8px;}
.floating-btn:hover{transform:translateY(-3px);box-shadow:0 15px 35px rgba(219,39,119,0.5);}
'''
html = html.replace('/* LAYOUT */', css_to_add + '\n/* LAYOUT */')

# 2. Remove nav search
nav_search = '''  <div class="nav-search">
    <span>🔍</span>
    <input type="text" placeholder="Search destinations, trips...">
  </div>'''
html = html.replace(nav_search, '')

# 3. Add Control Bar under Hero
ctrl_bar = '''  <!-- CONTROL BAR -->
  <div class="control-bar">
    <div class="ctrl-search">
      <span>🔍</span>
      <input type="text" placeholder="Search destinations, trips..." id="searchBox">
    </div>
    <button class="ctrl-btn">Group by ▾</button>
    <button class="ctrl-btn">Filter ▾</button>
    <button class="ctrl-btn">Sort by... ▾</button>
  </div>
'''
html = html.replace('<!-- QUICK ACTIONS -->', ctrl_bar + '\n  <!-- QUICK ACTIONS -->')

# 4. Rename Sections
html = html.replace('🌟 Recommended Destinations', 'Top Regional Selections')
html = html.replace('Upcoming Trips', 'Previous Trips')
html = html.replace('upcoming trips and 5 saved destinations', 'previous trips and top regional selections')

# 5. Add floating button at the end before </body>
floating_btn = '''  <a href="/plan-trip" class="floating-btn">+ Plan a trip</a>\n</body>'''
html = html.replace('</body>', floating_btn)

# 6. Swap Quick Actions/Upcoming Trips with Recommended Destinations
parts = re.split(r'<!-- (QUICK ACTIONS|Previous Trips|Top Regional Selections|BUDGET OVERVIEW) -->', html)
if len(parts) == 9:
    new_html = parts[0] + '<!-- ' + parts[5] + ' -->' + parts[6] + '<!-- ' + parts[3] + ' -->' + parts[4] + '<!-- ' + parts[1] + ' -->' + parts[2] + '<!-- ' + parts[7] + ' -->' + parts[8]
    html = new_html

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated home.html')
