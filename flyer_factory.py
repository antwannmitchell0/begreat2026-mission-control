#!/usr/bin/env python3
"""
BeGreat2026 Flyer Factory
Generates branded motivational flyers automatically.
Run: python3 flyer_factory.py
"""

from PIL import Image, ImageDraw, ImageFont
import os, random, json, textwrap, math
from datetime import datetime

OUTPUT_DIR = os.path.expanduser("~/Desktop/BeGreat_Flyers")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── BRAND COLORS ───────────────────────────────────────────
COLORS = {
    "black":      "#0A0A0A",
    "gold":       "#D4AF37",
    "gold_light": "#F0C93A",
    "white":      "#FFFFFF",
    "gray":       "#1E1E1E",
    "red_accent": "#C0392B",
}

# ─── CONTENT LIBRARY ────────────────────────────────────────
QUOTES = [
    ("The only person you are destined to become is the person you decide to be.", "Ralph Waldo Emerson"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Your story is not over. The best chapter is still being written.", "Antwann Mitchell Sr."),
    ("I dropped out in 7th grade, went to prison for 10 years, and still got my degree.\nIf I can, so can you.", "Antwann Mitchell Sr."),
    ("Believe. Endure. Grind. Resilience. Educate. Adapt. Transform.\nThat's what it means to B.E.G.R.E.A.T.", "Antwann Mitchell Sr."),
    ("You didn't come this far to only come this far.", "Unknown"),
    ("The prison walls couldn't hold my mind. Nothing can hold yours.", "Antwann Mitchell Sr."),
    ("Success is not given. It is built — brick by brick, day by day.", "Antwann Mitchell Sr."),
    ("Your past is proof you survived. Your future is proof you can thrive.", "Antwann Mitchell Sr."),
    ("Greatness is not a destination. It is a decision you make every morning.", "Antwann Mitchell Sr."),
    ("Stop waiting for the perfect moment. Take the moment and make it perfect.", "Unknown"),
    ("The comeback is always greater than the setback.", "Unknown"),
    ("You are not your worst day. You are every time you chose to get back up.", "Antwann Mitchell Sr."),
    ("Hard times are not the end. They are the beginning of your testimony.", "Antwann Mitchell Sr."),
]

STATS = [
    ("92%", "of people never achieve their goals\nbecause they give up too soon."),
    ("80%", "of millionaires went through\na major failure before their breakthrough."),
    ("Only 8%", "of people achieve their New Year's goals.\nBe the 8%."),
    ("43%", "of formerly incarcerated people\nare re-arrested within a year.\nYou don't have to be a statistic."),
    ("70%", "of success is just showing up\nconsistently when others quit."),
    ("1 in 4", "adults say fear of failure\nis the #1 reason they never start."),
    ("67%", "of people who write down their goals\nachieve them vs. those who don't."),
    ("It takes", "an average of 66 days\nto build a new habit.\nStay consistent."),
    ("Less than 1%", "of people pursue higher education\nafter incarceration.\nBe the 1%."),
    ("People with a mentor", "are 5x more likely\nto reach their goals.\nWho is mentoring you?"),
]

ACRONYM_LINES = [
    ("B", "BELIEVE in yourself when nobody else will."),
    ("E", "ENDURE the pain that others refuse to face."),
    ("G", "GRIND when motivation runs out."),
    ("R", "RESILIENCE turns setbacks into setups."),
    ("E", "EDUCATE yourself — knowledge is power."),
    ("A", "ADAPT or stay stuck. The choice is yours."),
    ("T", "TRANSFORM your life one decision at a time."),
]

# ─── FONT HELPERS ────────────────────────────────────────────
def get_font(size, bold=False):
    font_paths = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_text_centered(draw, text, y, font, color, canvas_w, shadow=True):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (canvas_w - text_w) // 2
    if shadow:
        draw.text((x+3, y+3), text, font=font, fill=(0,0,0,180))
    draw.text((x, y), text, font=font, fill=color)
    return bbox[3] - bbox[1]  # return height

def draw_text_wrapped(draw, text, x, y, max_w, font, color, canvas_w, center=True, line_spacing=1.3):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0,0), test, font=font)
        if bbox[2] - bbox[0] <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    
    total_h = 0
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        lh = bbox[3] - bbox[1]
        if center:
            lw = bbox[2] - bbox[0]
            lx = (canvas_w - lw) // 2
        else:
            lx = x
        draw.text((lx+2, y+total_h+2), line, font=font, fill=(0,0,0,160))
        draw.text((lx, y+total_h), line, font=font, fill=color)
        total_h += int(lh * line_spacing)
    return total_h

# ─── FLYER TEMPLATES ─────────────────────────────────────────

def make_quote_flyer(quote, author, filename):
    W, H = 1080, 1080
    img = Image.new("RGBA", (W, H), hex_to_rgb(COLORS["black"]))
    draw = ImageDraw.Draw(img)

    # Gold diagonal accent bars
    for i in range(0, W+H, 40):
        draw.line([(i, 0), (i-H, H)], fill=(*hex_to_rgb(COLORS["gold"]), 15), width=20)

    # Top gold bar
    draw.rectangle([0, 0, W, 8], fill=hex_to_rgb(COLORS["gold"]))
    # Bottom gold bar
    draw.rectangle([0, H-8, W, H], fill=hex_to_rgb(COLORS["gold"]))

    # Gold corner accents
    draw.rectangle([0, 0, 80, 8], fill=hex_to_rgb(COLORS["gold_light"]))
    draw.rectangle([0, 0, 8, 80], fill=hex_to_rgb(COLORS["gold_light"]))
    draw.rectangle([W-80, H-8, W, H], fill=hex_to_rgb(COLORS["gold_light"]))
    draw.rectangle([W-8, H-80, W, H], fill=hex_to_rgb(COLORS["gold_light"]))

    # Big quotation mark
    q_font = get_font(220)
    draw.text((40, -30), "\u201C", font=q_font, fill=(*hex_to_rgb(COLORS["gold"]), 60))

    # Brand name top
    brand_font = get_font(36)
    draw_text_centered(draw, "B.E.G.R.E.A.T. 2026", 30, brand_font, hex_to_rgb(COLORS["gold"]), W, shadow=False)

    # Quote text
    quote_font = get_font(58 if len(quote) < 80 else 46 if len(quote) < 130 else 38)
    quote_y = 180
    quote_h = draw_text_wrapped(draw, f"\u201C{quote}\u201D", 60, quote_y, W-120, quote_font, 
                                 hex_to_rgb(COLORS["white"]), W, center=True, line_spacing=1.4)

    # Author
    auth_font = get_font(34)
    auth_y = quote_y + quote_h + 50
    draw_text_centered(draw, f"— {author}", auth_y, auth_font, hex_to_rgb(COLORS["gold"]), W)

    # Divider line
    line_y = auth_y + 70
    draw.rectangle([W//2 - 150, line_y, W//2 + 150, line_y + 3], fill=hex_to_rgb(COLORS["gold"]))

    # Bottom branding
    tag_font = get_font(28)
    draw_text_centered(draw, "@begreat2026", H - 60, tag_font, hex_to_rgb(COLORS["gold_light"]), W, shadow=False)
    draw_text_centered(draw, "#BeGreat2026 #Motivation #Mindset #Inspire", H - 28, get_font(20), 
                        (*hex_to_rgb(COLORS["white"]), 160), W, shadow=False)

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, filename), quality=95)
    print(f"  ✅ {filename}")


def make_stat_flyer(big_text, detail_text, filename):
    W, H = 1080, 1080
    img = Image.new("RGBA", (W, H), hex_to_rgb(COLORS["black"]))
    draw = ImageDraw.Draw(img)

    # Background circle
    draw.ellipse([W//2-420, H//2-420, W//2+420, H//2+420], 
                  fill=(*hex_to_rgb(COLORS["gray"]), 255))
    draw.ellipse([W//2-400, H//2-400, W//2+400, H//2+400], 
                  fill=(*hex_to_rgb(COLORS["black"]), 255))
    draw.arc([W//2-420, H//2-420, W//2+420, H//2+420], 
              0, 270, fill=hex_to_rgb(COLORS["gold"]), width=8)

    # Gold bars
    draw.rectangle([0, 0, W, 10], fill=hex_to_rgb(COLORS["gold"]))
    draw.rectangle([0, H-10, W, H], fill=hex_to_rgb(COLORS["gold"]))

    # Brand
    brand_font = get_font(34)
    draw_text_centered(draw, "B.E.G.R.E.A.T. 2026", 25, brand_font, hex_to_rgb(COLORS["gold"]), W, shadow=False)

    # DID YOU KNOW
    know_font = get_font(30)
    draw_text_centered(draw, "DID YOU KNOW?", H//2 - 250, know_font, hex_to_rgb(COLORS["gold"]), W)

    # Big stat number/text
    stat_font = get_font(120 if len(big_text) <= 5 else 80)
    draw_text_centered(draw, big_text, H//2 - 170, stat_font, hex_to_rgb(COLORS["gold_light"]), W)

    # Detail text
    detail_font = get_font(42)
    draw_text_wrapped(draw, detail_text, 60, H//2 + 20, W-140, detail_font,
                       hex_to_rgb(COLORS["white"]), W, center=True, line_spacing=1.5)

    # Bottom
    cta_font = get_font(32)
    draw_text_centered(draw, "YOUR STORY IS NOT OVER. B.E.G.R.E.A.T.", H - 90, cta_font, 
                        hex_to_rgb(COLORS["gold"]), W)
    draw_text_centered(draw, "@begreat2026  |  #BeGreat2026", H - 45, get_font(24),
                        (*hex_to_rgb(COLORS["white"]), 180), W, shadow=False)

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, filename), quality=95)
    print(f"  ✅ {filename}")


def make_acronym_flyer(filename):
    W, H = 1080, 1920  # Portrait/Story format
    img = Image.new("RGBA", (W, H), hex_to_rgb(COLORS["black"]))
    draw = ImageDraw.Draw(img)

    # Subtle background texture
    for i in range(0, H, 60):
        draw.line([0, i, W, i], fill=(*hex_to_rgb(COLORS["gray"]), 30), width=1)

    # Gold bars
    draw.rectangle([0, 0, W, 10], fill=hex_to_rgb(COLORS["gold"]))
    draw.rectangle([0, H-10, W, H], fill=hex_to_rgb(COLORS["gold"]))
    draw.rectangle([0, 0, 10, H], fill=hex_to_rgb(COLORS["gold"]))
    draw.rectangle([W-10, 0, W, H], fill=hex_to_rgb(COLORS["gold"]))

    # Title
    title_font = get_font(80)
    draw_text_centered(draw, "B.E.G.R.E.A.T.", 60, title_font, hex_to_rgb(COLORS["gold"]), W)
    sub_font = get_font(36)
    draw_text_centered(draw, "The 7 Principles of Greatness", 160, sub_font, hex_to_rgb(COLORS["white"]), W)

    # Divider
    draw.rectangle([W//2-200, 220, W//2+200, 226], fill=hex_to_rgb(COLORS["gold"]))

    # Each letter
    letter_font = get_font(90)
    word_font = get_font(44)
    desc_font = get_font(30)
    
    start_y = 260
    spacing = (H - start_y - 120) // len(ACRONYM_LINES)
    
    for i, (letter, description) in enumerate(ACRONYM_LINES):
        y = start_y + i * spacing
        # Letter background circle
        cx, cy = 90, y + spacing//2 - 10
        draw.ellipse([cx-45, cy-45, cx+45, cy+45], fill=hex_to_rgb(COLORS["gold"]))
        draw.text((cx - 25, cy - 42), letter, font=letter_font, fill=hex_to_rgb(COLORS["black"]))
        # Description
        word = description.split()[0]
        rest = description[len(word):]
        draw.text((150, y + spacing//2 - 52), word, font=word_font, fill=hex_to_rgb(COLORS["gold_light"]))
        draw.text((150, y + spacing//2 - 5), rest.strip(), font=desc_font, fill=hex_to_rgb(COLORS["white"]))

    # Bottom
    draw_text_centered(draw, "@begreat2026  |  #BeGreat2026", H - 55, get_font(28),
                        hex_to_rgb(COLORS["gold"]), W, shadow=False)

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, filename), quality=95)
    print(f"  ✅ {filename}")


# ─── MAIN: GENERATE BATCH ────────────────────────────────────
def generate_batch(count=10):
    print(f"\n🎨 BeGreat2026 Flyer Factory — Generating {count} flyers...\n")
    print(f"📁 Output: {OUTPUT_DIR}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    generated = []

    # Always include the acronym flyer
    fname = f"begreat_acronym_{timestamp}.jpg"
    make_acronym_flyer(fname)
    generated.append(fname)

    # Mix of quotes and stats
    random.shuffle(QUOTES)
    random.shuffle(STATS)
    
    q_count = count // 2
    s_count = count - q_count - 1  # -1 for acronym
    
    for i, (quote, author) in enumerate(QUOTES[:q_count]):
        fname = f"begreat_quote_{i+1}_{timestamp}.jpg"
        make_quote_flyer(quote, author, fname)
        generated.append(fname)
    
    for i, (big, detail) in enumerate(STATS[:s_count]):
        fname = f"begreat_stat_{i+1}_{timestamp}.jpg"
        make_stat_flyer(big, detail, fname)
        generated.append(fname)

    print(f"\n✅ {len(generated)} flyers generated!")
    print(f"📁 Find them on your Desktop in: BeGreat_Flyers/")
    print(f"\nReady to post on Instagram, Facebook, TikTok, and YouTube! ⚡")
    return generated

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    generate_batch(count)
