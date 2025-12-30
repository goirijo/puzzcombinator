import textwrap
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("PigpenCipher.otf")

image = Image.new("RGB", (800,800), color="white")
draw = ImageDraw.Draw(image)

margin=offset=40
text="This is a very long text, that goes on for line upon line upon line. I really just want to see if it wraps."

for line in textwrap.wrap(text, width=80):
    draw.text((margin, offset), line, font=font, fill="black")
    offset += font.getbbox(line)[3]

image.save("output.png")

