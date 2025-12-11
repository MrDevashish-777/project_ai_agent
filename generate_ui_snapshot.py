"""generate_ui_snapshot.py
Creates a static HTML snapshot of a typical conversation (user/bot) using sample outputs we captured.
This provides a reproducible visual preview of what the frontend shows.
"""
import json
import os

OUT_HTML = 'ui_demo_output.html'

sample = {
    "conversation": [
        {"role": "user", "message": "Hi"},
        {"role": "bot", "message": "Hello! Welcome to Nagpur hotel helper. What's your budget per night (INR) or what kind of hotel are you looking for?"},
        {"role": "user", "message": "Budget 2500"},
        {"role": "bot", "message": "I found 17 hotels within ₹2500/night. Here are top matches (id, name, price, rating). Reply with the hotel id to book or ask for more details.",
         "suggestions": [
             {"id":"h11","name":"Hotel Dwarkamai","price_per_night":2500,"rating":4.2},
             {"id":"h20","name":"Hotel Lotus Inn","price_per_night":2200,"rating":4.1},
             {"id":"h16","name":"Hotel Vrandavan","price_per_night":2300,"rating":4.0}
         ]
        },
        {"role": "user", "message": "Book h2 name:Alice phone:+919999999999 2025-12-12 nights 2"},
        {"role": "bot", "message": "Booking confirmed. Booking ID: 450d0366-aaa3-4b9a-8cc3-287120311a97. Total: ₹11600"}
    ]
}

TEMPLATE = '''<!doctype html>
<meta charset="utf-8">
<title>UI Demo Snapshot</title>
<style>body{{font-family:Arial,Helvetica,sans-serif;background:#f4f4f4;padding:24px}}#wrap{{width:420px;margin:0 auto;background:#fff;border-radius:8px;padding:14px;box-shadow:0 6px 18px rgba(0,0,0,0.08)}}.msg{{margin:10px 0;padding:12px;border-radius:10px;max-width:86%}}.user{{background:#3498db;color:#fff;margin-left:auto}}.bot{{background:#ecf0f1;color:#222;margin-right:auto}}.suggestions{{display:flex;flex-direction:column;gap:8px;margin-top:8px}}.suggestion{{display:flex;justify-content:space-between;padding:8px;border-radius:8px;border:1px solid #ddd;background:#fff}}</style>
<div id="wrap">
    <h3>UI Demo Snapshot</h3>
    <div id="chat">
    ###MESSAGES###
    </div>
</div>'''

def render_messages(conv):
    parts = []
    for m in conv:
        if m['role']=='user':
            parts.append(f"<div class='msg user'>{m['message']}</div>")
        else:
            s = f"<div class='msg bot'>{m['message']}</div>"
            if 'suggestions' in m and m['suggestions']:
                s += '<div class="suggestions">'
                for h in m['suggestions']:
                    s += ("<div class='suggestion'><div><b>{name}</b><div style=\"font-size:12px; color:#666\">id: {id} · ₹{price} · ⭐{rating}</div></div>"
                          "<div style='display:flex; gap:6px'><button>Select</button><button>Book</button></div></div>").format(name=h['name'], id=h['id'], price=h['price_per_night'], rating=h['rating'])
                s += '</div>'
            parts.append(s)
    return '\n'.join(parts)

def main():
    html = TEMPLATE.replace('###MESSAGES###', render_messages(sample['conversation']))
    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Saved snapshot:', OUT_HTML)

if __name__=='__main__':
    main()
