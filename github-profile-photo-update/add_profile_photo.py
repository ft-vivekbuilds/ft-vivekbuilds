from pathlib import Path
import base64, re

svg_path = Path("assets/profile-dashboard.svg")
photo_path = Path("assets/profile.png")

if not svg_path.exists():
    raise SystemExit("assets/profile-dashboard.svg not found. Run generate_dashboard.py first.")
if not photo_path.exists():
    raise SystemExit("assets/profile.png not found. Put the downloaded profile.png inside assets/.")

svg = svg_path.read_text(encoding="utf-8")
photo_b64 = base64.b64encode(photo_path.read_bytes()).decode("ascii")
photo_href = f"data:image/png;base64,{photo_b64}"

# Replace the placeholder text if the generated SVG contains it.
pattern = re.compile(
    r'<text\b[^>]*>YOUR PHOTO</text>\s*'
    r'(?:<text\b[^>]*>ADD IMAGE HERE</text>)?',
    re.I
)

replacement = (
    '<defs><clipPath id="profilePhotoClip">'
    '<circle cx="145" cy="175" r="70"/></clipPath></defs>'
    f'<image href="{photo_href}" x="75" y="105" width="140" height="140" '
    'preserveAspectRatio="xMidYMid slice" clip-path="url(#profilePhotoClip)"/>'
)

new_svg, count = pattern.subn(replacement, svg, count=1)

if count == 0:
    raise SystemExit(
        "Could not find the placeholder in the generated SVG. "
        "Open assets/profile-dashboard.svg and send me the section containing 'YOUR PHOTO'."
    )

svg_path.write_text(new_svg, encoding="utf-8")
print("Profile photo added to assets/profile-dashboard.svg")
