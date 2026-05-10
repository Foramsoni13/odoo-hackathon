import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS
old_css = '''.notif-btn{width:38px;height:38px;background:var(--surface);border:1px solid var(--border);border-radius:10px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px;transition:.2s;}
.notif-btn:hover{background:rgba(255,255,255,0.1);}'''

new_css = '''.notif-wrapper{position:relative;}
.notif-btn{width:38px;height:38px;background:var(--surface);border:1px solid var(--border);border-radius:10px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px;transition:.2s;position:relative;}
.notif-btn:hover{background:rgba(255,255,255,0.1);}
.notif-badge{position:absolute;top:-4px;right:-4px;background:#ef4444;color:#fff;font-size:10px;font-weight:700;width:16px;height:16px;display:flex;align-items:center;justify-content:center;border-radius:50%;border:2px solid var(--bg);}
.notif-panel{position:absolute;top:120%;right:0;width:300px;background:rgba(10,15,30,0.95);border:1px solid var(--border);border-radius:16px;box-shadow:0 20px 40px rgba(0,0,0,0.5);backdrop-filter:blur(20px);opacity:0;visibility:hidden;transform:translateY(-10px);transition:.3s;z-index:200;}
.notif-panel.show{opacity:1;visibility:visible;transform:translateY(0);}
.notif-header{padding:14px 18px;border-bottom:1px solid var(--border);font-size:14px;font-weight:700;color:#fff;}
.notif-body{max-height:300px;overflow-y:auto;}
.notif-item{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid rgba(255,255,255,0.05);transition:.2s;cursor:pointer;}
.notif-item:hover{background:rgba(255,255,255,0.05);}
.notif-icon{width:36px;height:36px;background:var(--surface);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;}
.notif-text{font-size:13px;color:var(--muted);line-height:1.4;}
.notif-text strong{color:#fff;font-weight:600;}'''

html = html.replace(old_css, new_css)

# 2. Update HTML
old_html = '''  <div class="nav-right">
    <div class="notif-btn">🔔</div>'''

new_html = '''  <div class="nav-right">
    <div class="notif-wrapper">
      <div class="notif-btn" id="notifBtn">🔔<span class="notif-badge">2</span></div>
      <div class="notif-panel" id="notifPanel">
        <div class="notif-header">Notifications (2)</div>
        <div class="notif-body">
          <div class="notif-item">
            <div class="notif-icon">🌴</div>
            <div class="notif-text"><strong>Bali Trip</strong><br>Your trip is upcoming in 30 days!</div>
          </div>
          <div class="notif-item">
            <div class="notif-icon">💰</div>
            <div class="notif-text"><strong>Budget Alert</strong><br>You've used 80% of your Bali budget.</div>
          </div>
        </div>
      </div>
    </div>'''

html = html.replace(old_html, new_html)

# 3. Add JS
js_addition = '''
    // Notification Toggle
    const notifBtn = document.getElementById("notifBtn");
    const notifPanel = document.getElementById("notifPanel");
    notifBtn.addEventListener("click", function(e) {
        e.stopPropagation();
        notifPanel.classList.toggle("show");
    });
    document.addEventListener("click", function(e) {
        if (!notifPanel.contains(e.target) && e.target !== notifBtn) {
            notifPanel.classList.remove("show");
        }
    });

    function applyFilters() {'''

html = html.replace('    function applyFilters() {', js_addition)

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Added notification panel to home.html')
