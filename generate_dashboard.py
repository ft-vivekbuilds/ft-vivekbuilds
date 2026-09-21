from pathlib import Path
import html

ROOT = Path(__file__).parent
DATA = ROOT / "data/profile.yml"
OUT = ROOT / "assets/profile-dashboard.svg"

def parse():
    d, section = {}, None
    for raw in DATA.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if s.endswith(":") and not s.startswith("-"):
            section = s[:-1]
            d[section] = []
        elif s.startswith("- ") and section:
            d[section].append(s[2:].strip().strip('"'))
        elif ":" in s:
            k, v = s.split(":", 1)
            d[k.strip()] = v.strip().strip('"')
            section = None
    return d

d = parse()
E = lambda x: html.escape(str(x), quote=True)

def text(x, y, value, cls="text", anchor="start"):
    return '<text x="{}" y="{}" class="{}" text-anchor="{}">{}</text>'.format(
        x, y, cls, anchor, E(value)
    )

svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1050" viewBox="0 0 1200 1050">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#101923"/><stop offset="1" stop-color="#111827"/>
</linearGradient>
<style>
.panel{fill:#101923;stroke:#29415e;stroke-width:1.5}
.title{font:700 19px monospace;fill:#63b3ff;letter-spacing:1px}
.text{font:16px monospace;fill:#d8e2f0}
.value{font:16px monospace;fill:#f1f5f9}
.muted{font:14px monospace;fill:#8fa2b8}
</style>
</defs>
<rect width="1200" height="1050" rx="18" fill="url(#bg)"/>

<rect x="20" y="20" width="1160" height="62" rx="10" class="panel"/>
<circle cx="48" cy="51" r="7" fill="#ff5f57"/><circle cx="70" cy="51" r="7" fill="#febc2e"/><circle cx="92" cy="51" r="7" fill="#28c840"/>
svg += text(45,138,"PROFILE","title")
svg += '<line x1="45" y1="154" x2="375" y2="154" stroke="#26394e"/>'

photo_path = BASE / "assets" / "profile.png"
photo_data = base64.b64encode(photo_path.read_bytes()).decode("ascii")

svg += '<defs><clipPath id="profilePhoto"><circle cx="210" cy="290" r="105"/></clipPath></defs>'
svg += '<circle cx="210" cy="290" r="105" fill="#273241" stroke="#4778a8" stroke-width="2"/>'
svg += '<image href="data:image/png;base64,{}" x="105" y="185" width="210" height="210" preserveAspectRatio="xMidYMid slice" clip-path="url(#profilePhoto)"/>'.format(photo_data)
svg += text(120,57,"~/profile.md")
svg += text(1150,57,"BUILD • LEARN • IMPROVE • REPEAT","muted","end")

svg += text(45,138,"PROFILE","title")
svg += '<line x1="45" y1="154" x2="375" y2="154" stroke="#26394e"/>'
svg += '<circle cx="210" cy="290" r="105" fill="#273241" stroke="#4778a8" stroke-width="2"/>'
svg += text(210,285,"YOUR PHOTO","muted","middle")
svg += text(210,312,"ADD IMAGE HERE","muted","middle")svg += '''<rect x="20" y="102" width="380" height="380" rx="10" class="panel"/>

svg += text(45,138,"PROFILE","title")
svg += '<line x1="45" y1="154" x2="375" y2="154" stroke="#26394e"/>'
svg += '<circle cx="210" cy="290" r="105" fill="#273241" stroke="#4778a8" stroke-width="2"/>'
svg += text(210,285,"YOUR PHOTO","muted","middle")
svg += text(210,312,"ADD IMAGE HERE","muted","middle")

svg += '''<rect x="420" y="102" width="760" height="380" rx="10" class="panel"/>
'''
svg += text(445,138,"SYSTEM.INFO","title")
svg += '<text x="1150" y="138" text-anchor="end" style="font:14px monospace;fill:#31d17c">● ONLINE</text>'
svg += '<line x1="445" y1="154" x2="1155" y2="154" stroke="#26394e"/>'
svg += '<text x="445" y="205" style="font:700 42px monospace;fill:#f1f5f9">{}</text>'.format(E(d.get("name","YOUR NAME")))
svg += text(445,238,d.get("subtitle","Your subtitle"))
svg += '<text x="445" y="270" style="font:700 18px monospace;fill:#45a3ff">{}</text>'.format(E(d.get("role","Your role")))
svg += text(445,302,d.get("tagline","Your tagline"),"muted")
svg += '<line x1="445" y1="320" x2="1155" y2="320" stroke="#26394e"/>'
for y, label, key in [(348,"Location","location"),(375,"Education","education"),(402,"Interests","interests"),(429,"Tech Stack","tech_stack"),(456,"Tools","tools"),(483,"Email","email")]:
    svg += text(445,y,label) + text(650,y,d.get(key,""),"value")


svg += '''<rect x="410" y="502" width="370" height="300" rx="10" class="panel"/>
'''
svg += text(435,538,"LANGUAGES","title")
svg += '<line x1="435" y1="552" x2="755" y2="552" stroke="#26394e"/>'
y = 590
for item in d.get("languages",[])[:6]:
    parts = item.split("|")
    name = parts[0].strip()
    pct = parts[1].strip() if len(parts)>1 else ""
    try: val = float(pct.replace("%",""))
    except: val = 0
    svg += text(435,y,name)
    svg += '<rect x="545" y="{}" width="220" height="12" rx="6" fill="#1b2a3b"/>'.format(y-14)
    svg += '<rect x="545" y="{}" width="{}" height="12" rx="6" fill="#45a3ff"/>'.format(y-14,min(220,val*2.2))
    svg += text(770,y,pct,"muted","end")
    y += 40

svg += '''<rect x="800" y="502" width="380" height="300" rx="10" class="panel"/>
'''
svg += text(825,538,"CURRENTLY LEARNING","title")
svg += '<line x1="825" y1="552" x2="1155" y2="552" stroke="#26394e"/>'
y = 592
for i,item in enumerate(d.get("learning",[])[:6]):
    svg += '<text x="830" y="{}" style="font:20px monospace;fill:#45a3ff">{}</text>'.format(y, "✓" if i<3 else "○")
    svg += text(860,y,item)
    y += 40

svg += '''<rect x="20" y="822" width="1160" height="160" rx="10" class="panel"/>
'''
svg += text(45,858,"PROJECTS","title")
svg += '<line x1="45" y1="872" x2="1155" y2="872" stroke="#26394e"/>'
positions = [(55,910),(55,945),(400,910),(400,945),(745,910)]
for item,pos in zip(d.get("projects",[])[:5],positions):
    svg += text(pos[0],pos[1],"› "+item)

svg += text(45,1020,"Email: "+d.get("email",""),"muted")
svg += text(600,1020,"LinkedIn: "+d.get("linkedin",""),"muted","middle")
svg += text(1155,1020,"GitHub: "+d.get("github",""),"muted","end")
svg += "</svg>"

OUT.write_text(svg, encoding="utf-8")
print("Generated:", OUT)
svg += text(45,138,"PROFILE","title")
svg += '<line x1="45" y1="154" x2="375" y2="154" stroke="#26394e"/>'

photo_path = BASE / "assets" / "profile.png"
photo_data = base64.b64encode(photo_path.read_bytes()).decode("ascii")

svg += '<defs><clipPath id="profilePhoto"><circle cx="210" cy="290" r="105"/></clipPath></defs>'
svg += '<circle cx="210" cy="290" r="105" fill="#273241" stroke="#4778a8" stroke-width="2"/>'
svg += '<image href="data:image/png;base64,{}" x="105" y="185" width="210" height="210" preserveAspectRatio="xMidYMid slice" clip-path="url(#profilePhoto)"/>'.format(photo_data)	

