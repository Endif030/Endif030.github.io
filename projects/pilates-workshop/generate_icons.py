from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename, text="普拉"):
    img = Image.new('RGB', (size, size), color='#FBBF24')
    draw = ImageDraw.Draw(img)

    font = None
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    
    font_size = int(size * 0.35)
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
    
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) / 2
    y = (size - text_height) / 2

    draw.text((x, y), text, font=font, fill='#1F2937')

    img.save(filename, 'PNG')
    print(f"✓ 已生成 {filename}")

if __name__ == "__main__":
    create_icon(192, 'icon-192.png', '普拉')
    create_icon(512, 'icon-512.png', '普拉')
    print("✓ PWA 图标生成完成")
