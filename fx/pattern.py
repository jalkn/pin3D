from PIL import Image, ImageDraw
import math

def advanced_halftone(input_path, output_path, pattern='circle', scale=8, angle=45):
    img = Image.open(input_path).convert('L')
    width, height = img.size
    output = Image.new('L', (width * scale, height * scale))
    draw = ImageDraw.Draw(output)
    
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            brightness = 255 - img.getpixel((x, y))
            size = (brightness / 255) * scale
            
            if pattern == 'circle':
                draw.ellipse([(x*scale - size, y*scale - size),
                            (x*scale + size, y*scale + size)], fill=255)
            elif pattern == 'square':
                draw.rectangle([(x*scale - size, y*scale - size),
                              (x*scale + size, y*scale + size)], fill=255)
            elif pattern == 'line':
                draw.line([(x*scale - size, y*scale),
                         (x*scale + size, y*scale)], fill=255, width=int(size/2))
    
    if angle != 0:
        output = output.rotate(angle, expand=1)
    
    output.save(output_path)
    return output

# Usage examples:
advanced_halftone('img/2.jpg', 'img/4.jpg', pattern='circle')
# advanced_halftone('input.jpg', 'square_halftone.jpg', pattern='square')
# advanced_halftone('input.jpg', 'line_halftone.jpg', pattern='line')