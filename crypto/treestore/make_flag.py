from PIL import Image, ImageFont, ImageDraw
import string


def render(msg: str):
    char_size = (16, 32)  # (width, height)
    width = char_size[0] * len(msg)
    image = Image.new("RGBA", (width, char_size[1]), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load("./ter-x32b.pil")  # Terminus 32px
    draw.text((0, 0), msg, font=font)
    return image


if __name__ == "__main__":
    # This not the length of the actual flag
    flag = "bctf{The_quick_brown_fox_jumps_over_the_lazy_dog}"
    # assert len(flag) < 32
    assert set(flag).issubset(set(string.ascii_lowercase + string.ascii_uppercase + string.digits + "{_}"))
    image = render(flag)
    image.save("flag.bmp", format="BMP")
