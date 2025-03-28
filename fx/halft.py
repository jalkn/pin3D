from PIL import Image, ImageDraw

def halftone_pil(input_path, output_path, scale=10, angle=45):
    # Load image and convert to grayscale
    image = Image.open(input_path).convert('L')
    width, height = image.size
    
    # Create a new image for the halftone result
    halftone = Image.new('L', (width * scale, height * scale))
    draw = ImageDraw.Draw(halftone)
    
    # Calculate dot size based on pixel brightness
    for x in range(0, width, 8):
        for y in range(0, height, 8):
            brightness = 255 - image.getpixel((x, y))
            radius = int(brightness / 255 * scale)
            draw.ellipse((x * scale - radius, y * scale - radius,
                         x * scale + radius, y * scale + radius), fill=255)
    
    # Rotate and crop if needed
    if angle != 0:
        halftone = halftone.rotate(angle, expand=1)
    
    halftone.save(output_path)
    return halftone

# Usage
halftone_pil('img/2.jpg', 'img/3.jpg', scale=5, angle=45)