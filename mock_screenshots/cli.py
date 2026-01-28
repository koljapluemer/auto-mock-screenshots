import argparse

from .core import generate_mockup, load_images, parse_resolution


def main():
    parser = argparse.ArgumentParser(
        prog="mock-screenshots",
        description="Arrange images on a canvas to create mockup compositions.",
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Image files or glob patterns",
    )
    parser.add_argument(
        "-o", "--output",
        default="mockup.png",
        help="Output file path (default: mockup.png)",
    )
    parser.add_argument(
        "-b", "--background",
        default=None,
        help="Background image file",
    )
    parser.add_argument(
        "-r", "--resolution",
        default="1920x1080",
        help="Canvas resolution WIDTHxHEIGHT (default: 1920x1080)",
    )
    parser.add_argument(
        "-p", "--padding",
        type=int,
        default=20,
        help="Pixels from content to canvas edge (default: 20)",
    )
    parser.add_argument(
        "-g", "--gap",
        type=int,
        default=20,
        help="Pixels between images (default: 20)",
    )
    args = parser.parse_args()

    canvas_size = parse_resolution(args.resolution)
    images = load_images(args.inputs)
    generate_mockup(
        images,
        canvas_size,
        output=args.output,
        background=args.background,
        gap=args.gap,
        padding=args.padding,
    )


if __name__ == "__main__":
    main()
