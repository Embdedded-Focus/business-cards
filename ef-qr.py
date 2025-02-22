import argparse
import logging
import sys
from decimal import Decimal
from math import cos, sin
from pathlib import Path

import qrcode
import qrcode.constants
import qrcode.image.svg
from qrcode.image.pil import PilImage
from qrcode.image.styles.moduledrawers.svg import SvgPathQRModuleDrawer

HTL_COLOR_CONTRAST = "rgb(1, 3, 38)"
HTL_COLOR_CONTRAST_RGB = (1, 3, 38)


class SvgPathImageHTL(qrcode.image.svg.SvgPathImage):
    background = HTL_COLOR_CONTRAST


class SvgPathHexDrawer(SvgPathQRModuleDrawer):
    def __init__(self, size_ratio: Decimal = Decimal(1), start_angle: float = 0) -> None:
        super().__init__(size_ratio=size_ratio)
        self.start_angle = start_angle

    def subpath(self, box: tuple[tuple[int, int], tuple[int, int]]) -> str:
        coords = self.coords(box)
        x0 = self.img.units(coords.x0, text=False)
        y0 = self.img.units(coords.y0, text=False)
        x1 = self.img.units(coords.x1, text=False)
        y1 = self.img.units(coords.y1, text=False)

        width = x1 - x0
        height = y1 - y0

        center_x, center_y = x0 + width / 2, y0 + height / 2

        side_length = min(width, height) / 2

        path = ""
        for i in range(6):
            angle_grad = 60 * i + 30 + self.start_angle
            angle_rad = angle_grad * (3.14159 / 180)
            x = round(center_x + side_length * Decimal(cos(angle_rad)), 2)
            y = round(center_y + side_length * Decimal(sin(angle_rad)), 2)
            instruction = "M" if i == 0 else "L"
            path += f"{instruction}{x},{y} "

        path += "Z"

        return path


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", type=Path, help="path to the generaged QR-Code")
    parser.add_argument("-i", "--input", type=Path, required=True, help="path to the data to embed")

    namespace = parser.parse_args(args)
    return namespace


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    arguments = parse_args(sys.argv[1:])

    qr = qrcode.QRCode(
        image_factory=qrcode.image.svg.SvgPathImage,
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(arguments.input.read_text())
    qr.make(fit=True)

    img = qr.make_image(
        # image_factory=CustomQRImage,
        module_drawer=SvgPathHexDrawer(size_ratio=Decimal(1), start_angle=30),
        # color_mask=ImageColorMask(
        #     color_mask_path="/home/rpoisel/git/embedded-focus/embedded-focus-site/assets/images/favicon.png"
        # ),
        # embeded_image_path="../embedded-focus-site/assets/images/favicon.png",
    )

    # img.path.attrib["fill"] = HTL_COLOR_CONTRAST  # type: ignore

    img.save(arguments.output or arguments.input.with_name("qr_code_" + arguments.input.name).with_suffix(".svg"))


if __name__ == "__main__":
    main()
