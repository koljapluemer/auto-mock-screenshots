import glob
import sys
from pathlib import Path
from PIL import Image

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'}


def load_images(inputs: list[str]) -> list[Image.Image]:
    """Resolve file paths and glob patterns, open images with PIL.

    Shell-expanded globs arrive as individual file args.
    Quoted globs are expanded here via glob.glob().
    """
    paths: list[Path] = []
    for entry in inputs:
        if any(c in entry for c in ('*', '?', '[')):
            matches = sorted(glob.glob(entry, recursive=True))
            if not matches:
                print(f"Warning: pattern '{entry}' matched no files", file=sys.stderr)
            paths.extend(Path(m) for m in matches)
        else:
            paths.append(Path(entry))

    images: list[Image.Image] = []
    for p in paths:
        if not p.exists():
            print(f"Error: file not found: {p}", file=sys.stderr)
            sys.exit(1)
        if p.suffix.lower() not in ALLOWED_EXTENSIONS:
            print(f"Error: unsupported format: {p}", file=sys.stderr)
            sys.exit(1)
        images.append(Image.open(p).convert("RGBA"))

    if not images:
        print("Error: no valid input images", file=sys.stderr)
        sys.exit(1)

    return images


def parse_resolution(resolution_str: str) -> tuple[int, int]:
    """Parse a 'WIDTHxHEIGHT' string into a (width, height) tuple."""
    try:
        w, h = resolution_str.lower().split('x')
        return int(w), int(h)
    except (ValueError, AttributeError):
        print(f"Error: invalid resolution '{resolution_str}', expected WIDTHxHEIGHT", file=sys.stderr)
        sys.exit(1)


def process_background_for_canvas(bg_path: str, canvas_size: tuple[int, int]) -> Image.Image:
    """Load background image and scale+center-crop it to exactly canvas_size."""
    target_w, target_h = canvas_size
    bg_image = Image.open(bg_path)
    bg_w, bg_h = bg_image.size
    scale = max(target_w / bg_w, target_h / bg_h)
    new_w = int(bg_w * scale)
    new_h = int(bg_h * scale)
    bg_resized = bg_image.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    bg_cropped = bg_resized.crop((left, top, left + target_w, top + target_h))
    return bg_cropped.convert("RGBA")


def place_image_on_canvas(image: Image.Image, canvas_size: tuple[int, int], margin: int) -> Image.Image:
    """Scale image to fit within canvas minus margins, centered on a transparent canvas."""
    canvas_w, canvas_h = canvas_size
    avail_w = canvas_w - 2 * margin
    avail_h = canvas_h - 2 * margin
    img_w, img_h = image.size
    scale = min(avail_w / img_w, avail_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    resized = image.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    pos_x = (canvas_w - new_w) // 2
    pos_y = (canvas_h - new_h) // 2
    canvas.paste(resized, (pos_x, pos_y), resized)
    return canvas


def combine_images_horizontally(
    images: list[Image.Image],
    canvas_size: tuple[int, int],
    gap: int = 20,
    padding: int = 20,
) -> Image.Image:
    """Combine images horizontally on a canvas, uniformly scaled to the same height.

    Images are centered as a group with `padding` px from canvas edges
    and `gap` px between each image.
    """
    canvas_w, canvas_h = canvas_size
    n = len(images)
    available_width = canvas_w - 2 * padding - gap * (n - 1)
    available_height = canvas_h - 2 * padding

    widths = [img.width * available_height / img.height for img in images]
    total_width = sum(widths)
    if total_width > available_width:
        scale = available_width / total_width
        final_height = int(available_height * scale)
        final_widths = [int(w * scale) for w in widths]
    else:
        final_height = int(available_height)
        final_widths = [int(w) for w in widths]

    group_width = sum(final_widths) + gap * (n - 1)
    start_x = (canvas_w - group_width) // 2
    start_y = (canvas_h - final_height) // 2

    composite = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    current_x = start_x
    for idx, img in enumerate(images):
        resized = img.resize((final_widths[idx], final_height), resample=Image.Resampling.LANCZOS)
        composite.paste(resized, (current_x, start_y), resized)
        current_x += final_widths[idx] + gap
    return composite


def arrange_images(
    images: list[Image.Image],
    canvas_size: tuple[int, int],
    gap: int,
    padding: int,
) -> Image.Image:
    """Dispatch: 1 image -> place centered, N images -> combine horizontally."""
    if len(images) == 1:
        return place_image_on_canvas(images[0], canvas_size, padding)
    return combine_images_horizontally(images, canvas_size, gap=gap, padding=padding)


def generate_mockup(
    images: list[Image.Image],
    canvas_size: tuple[int, int],
    output: str,
    background: str | None = None,
    gap: int = 20,
    padding: int = 20,
) -> None:
    """Arrange images on canvas, optionally composite onto background, save to output."""
    arranged = arrange_images(images, canvas_size, gap=gap, padding=padding)

    if background:
        bg = process_background_for_canvas(background, canvas_size)
        bg.paste(arranged, (0, 0), arranged)
        result = bg
    else:
        result = arranged

    # Save as RGB for JPEG, RGBA for everything else
    if output.lower().endswith(('.jpg', '.jpeg')):
        result = result.convert('RGB')

    result.save(output)
    print(f"Saved: {output}")
