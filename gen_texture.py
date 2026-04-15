import base64
from io import BytesIO
import sys
import subprocess

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFilter

def create_head():
    img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw an oval head, realistic dark green color
    draw.ellipse((2, 2, 18, 18), fill=(34, 139, 34))  # ForestGreen
    draw.ellipse((4, 4, 16, 16), fill=(46, 139, 87))  # SeaGreen
    
    # Draw eyes
    draw.ellipse((5, 5, 8, 8), fill=(255, 255, 0)) # yellow eye
    draw.ellipse((12, 5, 15, 8), fill=(255, 255, 0)) # yellow eye
    # pupils
    draw.ellipse((6, 6, 7, 7), fill=(0, 0, 0))
    draw.ellipse((13, 6, 14, 7), fill=(0, 0, 0))
    
    # tongue
    draw.line((10, 18, 10, 20), fill=(255, 0, 0), width=1)
    return img

def create_body():
    img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw a round body segment
    draw.ellipse((2, 2, 18, 18), fill=(34, 139, 34))
    # Add a slight pattern for scales
    draw.ellipse((6, 6, 14, 14), fill=(0, 100, 0)) # DarkGreen
    return img

def create_apple():
    img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Apple
    draw.ellipse((3, 3, 17, 17), fill=(220, 20, 60)) # Crimson red
    draw.ellipse((5, 5, 10, 10), fill=(255, 69, 0)) # Highlight
    # Stem
    draw.line((10, 3, 11, 0), fill=(139, 69, 19), width=2)
    # Leaf
    draw.ellipse((11, 1, 14, 4), fill=(50, 205, 50))
    return img

def image_to_b64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

with open("/home/milerski.l.28@zszatopkovych.cz/Dokumenty/lukipuki/textures.txt", "w") as f:
    f.write("APPLE_B64 = '" + image_to_b64(create_apple()) + "'\n")
    f.write("HEAD_B64 = '" + image_to_b64(create_head()) + "'\n")
    f.write("BODY_B64 = '" + image_to_b64(create_body()) + "'\n")
print("Done!")
