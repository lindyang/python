import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from flask import Flask


def gen_code(size=(80, 30),
            chars=None,
            mode="RGB",
            bg_color=(255, 255, 255),
            fg_color=(255, 0, 0),
            font_size=18,
            font_type="Monaco.ttf",
            length=4,
            draw_points=True,
            point_chance=1):

    if chars is None:
        chars = ''.join(map(str, range(10)))
    width, height = size
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)

    def get_chars():
        return random.sample(chars, length)

    def create_points():
        chance = min(50, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        c_chars = get_chars()
        strs = '%s' % ''.join(c_chars)
        font_type = 'LiberationSerif-Bold.ttf'
        font = ImageFont.truetype(font_type, size=font_size)
        font_width, font_height = font.getsize(strs)
        draw.text(
            ((width - font_width) / 3, (height - font_height) / 4),
            strs,
            font=font,
            fill=fg_color
        )
        return strs

    if draw_points:
        create_points()

    strs = create_strs()

    params = [1 - float(random.randint(1, 2)) / 100,
        0,
        0,
        0,
        1 - float(random.randint(1, 10)) / 100,
        float(random.randint(1, 2)) / 500,
        0.001,
        float(random.randint(1, 2)) / 500,
    ]
    
    img = img.transform(size, Image.PERSPECTIVE, params)
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, strs


app = Flask(__name__)


@app.route('/')
def get_code():
    img, strs = gen_code()
    buf = BytesIO()
    img.save(buf, 'JPEG', quality=70)
    buf_str = buf.getvalue()
    response = app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
