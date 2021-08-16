from PIL import Image, ImageDraw, ImageFont

imgHeight = 52400
imgWidth = 90240
letterHeight = 10
letterWidth = 50
imgSize = (imgWidth, imgHeight)
bg_color = (10, 255, 255)
img = Image.new("RGB", imgSize, bg_color)
drawBrush = ImageDraw.Draw(img)
textY0 = (imgHeight - letterHeight + 1) / 2
textY0 = int(textY0)
textX0 = int((imgWidth - letterWidth + 1) / 2)
print('text location:', (textX0, textY0))
print('text size (width,height):', letterWidth, letterHeight)
print('img size(width,height):', imgSize)
font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", size=20)
fg_color = (20, 220, 90)
drawBrush.text((textX0, textY0), "---zMain---", fill=fg_color, font=font)
img.save("C:\\Users\\tianjingle\\Desktop\\原图123.png", quality=60)