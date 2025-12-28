from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("PigpenCipher.otf")

image = Image.new("RGB", (200,200), color="white")
draw = ImageDraw.Draw(image)
draw.text((10,10), "Hello, World!.,!@#$%^&*()", font=font, fill="black")

image.save("output.png")
