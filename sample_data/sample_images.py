"""
Sample Inspection Test Image Generator and Registry.
Provides synthetic high-fidelity test images for quick 1-click demonstration.
"""

from PIL import Image, ImageDraw, ImageFont
import io

def generate_sample_ppe_image(scenario: str = "compliant") -> Image.Image:
    """Generates a high-resolution synthetic construction site diagram/photo for testing."""
    img = Image.new("RGB", (900, 600), color=(235, 238, 245))
    draw = ImageDraw.Draw(img)
    
    # Draw construction background (sky, concrete floor, scaffolding grid)
    draw.rectangle([(0, 0), (900, 250)], fill=(186, 215, 233)) # Sky
    draw.rectangle([(0, 250), (900, 600)], fill=(108, 117, 125)) # Concrete deck
    
    # Scaffolding frames (yellow/silver pipes)
    for x in range(50, 900, 150):
        draw.line([(x, 80), (x, 500)], fill=(234, 179, 8), width=6)
        draw.line([(x-75, 220), (x+75, 220)], fill=(234, 179, 8), width=4)
        draw.line([(x-75, 360), (x+75, 360)], fill=(234, 179, 8), width=4)
        draw.line([(x-75, 220), (x+75, 360)], fill=(202, 138, 4), width=3)
        draw.line([(x+75, 220), (x-75, 360)], fill=(202, 138, 4), width=3)

    # Perimeter edge warning banner
    draw.line([(0, 250), (900, 250)], fill=(239, 68, 68), width=5)
    
    # Draw simulated worker 1 (Center)
    # Head & Helmet
    helmet_color = (250, 204, 21) if scenario == "compliant" else (180, 83, 9)
    draw.ellipse([(410, 280), (490, 350)], fill=(254, 202, 202)) # Head
    draw.arc([(400, 260), (500, 330)], 180, 360, fill=helmet_color, width=12) # Hardhat
    draw.rectangle([(405, 290), (495, 305)], fill=helmet_color) # Helmet brim
    
    # Body & Vest
    vest_color = (132, 204, 22) if scenario == "compliant" else (55, 65, 81)
    draw.rectangle([(400, 350), (500, 480)], fill=vest_color) # Torso / Vest
    if scenario == "compliant":
        # Reflective stripes
        draw.line([(400, 380), (500, 380)], fill=(241, 245, 249), width=8)
        draw.line([(400, 440), (500, 440)], fill=(241, 245, 249), width=8)
        draw.line([(430, 350), (430, 480)], fill=(241, 245, 249), width=6)
        draw.line([(470, 350), (470, 480)], fill=(241, 245, 249), width=6)

    # Legs & Boots
    draw.rectangle([(410, 480), (445, 560)], fill=(30, 41, 59))
    draw.rectangle([(455, 480), (490, 560)], fill=(30, 41, 59))
    boot_color = (120, 53, 15) if scenario == "compliant" else (203, 213, 225)
    draw.rectangle([(405, 555), (445, 580)], fill=boot_color) # Safety boots
    draw.rectangle([(455, 555), (495, 580)], fill=boot_color)

    # Safety Text Label Box
    label = "SCENARIO: COMPLIANT PPE (HELMET + HIGH-VIS + STEEL TOE)" if scenario == "compliant" else "SCENARIO: PPE VIOLATIONS DETECTED (NO HARDHAT / NO HIGH-VIS)"
    box_color = (22, 101, 52) if scenario == "compliant" else (153, 27, 27)
    draw.rectangle([(20, 20), (880, 65)], fill=box_color)
    draw.text((35, 32), f"🏗️ SITE AUDIT TEST FEED | {label}", fill=(255, 255, 255))
    
    return img

def generate_sample_crack_image(crack_type: str = "shear") -> Image.Image:
    """Generates a high-resolution synthetic concrete inspection image with specific crack patterns."""
    img = Image.new("RGB", (900, 600), color=(148, 163, 184)) # Concrete gray
    draw = ImageDraw.Draw(img)
    
    # Concrete texture / beam outline
    draw.rectangle([(50, 80), (850, 520)], fill=(203, 213, 225), outline=(71, 85, 105), width=6)
    
    # Grid lines / formwork tie holes
    for x in range(120, 850, 140):
        for y in range(130, 520, 110):
            draw.ellipse([(x-6, y-6), (x+6, y+6)], fill=(51, 65, 85))

    if crack_type == "shear":
        # 45-degree diagonal shear crack near left support
        points = [
            (180, 510), (220, 460), (260, 410), (310, 360),
            (370, 300), (430, 240), (490, 180), (550, 120), (580, 90)
        ]
        # Main crack fissure
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=(15, 23, 42), width=7)
            # Secondary branch
            if i == 4:
                draw.line([(370, 300), (410, 340), (450, 360)], fill=(30, 41, 59), width=3)
        
        banner = "STRUCTURAL DEFECT: 45° DIAGONAL SHEAR CRACK (CRITICAL URGENCY)"
        box_color = (185, 28, 28)

    elif crack_type == "spalling":
        # Exposed rebar & concrete delamination
        draw.ellipse([(350, 200), (600, 420)], fill=(100, 116, 139), outline=(51, 65, 85), width=4)
        # Rebar rusted bars
        draw.line([(320, 280), (630, 280)], fill=(180, 83, 9), width=16) # Corroded Rebar 1
        draw.line([(320, 340), (630, 340)], fill=(146, 64, 14), width=16) # Corroded Rebar 2
        # Rust staining bleeding outwards
        draw.ellipse([(370, 260), (580, 370)], fill=(217, 119, 6, 128))
        banner = "SURFACE DEFECT: CONCRETE COVER SPALLING WITH RUSTED REBAR"
        box_color = (194, 65, 12)

    else:
        # Hairline shrinkage crack
        points = [(450, 100), (445, 180), (460, 270), (440, 350), (455, 430), (450, 500)]
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=(51, 65, 85), width=2)
        banner = "SURFACE DEFECT: PLASTIC DRYING HAIRLINE CRACK (< 0.20 mm)"
        box_color = (71, 85, 105)

    # Label Banner
    draw.rectangle([(20, 20), (880, 65)], fill=box_color)
    draw.text((35, 32), f"🧱 STRUCTURAL INSPECTION FEED | {banner}", fill=(255, 255, 255))
    
    return img
