import os
import random
from itertools import chain, combinations
from PIL import Image, ImageDraw

# ------------------------- Constants -------------------------
BASE_PATH = '/home/brokkoli/GITHUB/scripts/017_auto_mock_screenshots/screenshots'
TOP_BAR_HEIGHT = 35                    
TOP_BAR_COLOR = (211, 211, 211)  # Light gray for top bar
BORDER_SIZE = 10
BORDER_COLOR = (30, 30, 30)       # Dark gray border
OUTER_RADIUS = 20               # Rounded border radius
ICON_TOP_MARGIN = 8
ICON_RIGHT_MARGIN = 10
URLBAR_LEFT_MARGIN = 25         # URL bar left margin
URLBAR_RIGHT_MARGIN = 150       # URL bar right margin from image border
TARGET_ELEMENT_HEIGHT = 20      # Height for both icon and urlbar
URLBAR_CAP_WIDTH = 10           # Preserved cap width for urlbar's rounded corners
ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')

# For placing mocks on canvas (standalone versions)
NO_BG_MARGIN = 20              # Fixed margin in no-bg standalone versions

# For combined mockups only:
COMBINED_GAP = 20              # Fixed gap between individual images
BORDER_GAP_RATIO = 0.02        # Margin from canvas edge: 2% of smaller canvas dimension

# For background composites:
BG_MARGIN_PERCENT = 0.15       # In bg standalone, margin = 15% of the smaller canvas dimension

# Target canvas sizes (also used for background optimization)
BG_TARGET_SIZE = (1920, 1080)   # Final background canvas size

# ------------------------- Global Caches -------------------------
icon_cache = None
urlbar_cache = None

# ------------------------- Overlay Resources -------------------------
def get_icon_image():
    """Load and cache the icon image (RGBA) from 'icons.png' in the script folder."""
    global icon_cache
    if icon_cache is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, 'icons.png')
        try:
            icon_cache = Image.open(icon_path).convert("RGBA")
        except Exception as e:
            print(f"Error loading icon image from {icon_path}: {e}")
            icon_cache = None
    return icon_cache

def get_urlbar_image():
    """Load and cache the urlbar image (RGBA) from 'urlbar.png' in the script folder."""
    global urlbar_cache
    if urlbar_cache is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        urlbar_path = os.path.join(script_dir, 'urlbar.png')
        try:
            urlbar_cache = Image.open(urlbar_path).convert("RGBA")
        except Exception as e:
            print(f"Error loading urlbar image from {urlbar_path}: {e}")
            urlbar_cache = None
    return urlbar_cache

# ------------------------- Basic Mock Processing -------------------------
def create_rounded_mask(size, radius):
    """Create a grayscale mask with rounded corners (white = visible)."""
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask

def stretch_urlbar(urlbar, target_width):
    """
    Perform three-slice scaling on the urlbar so that its left and right caps remain unchanged,
    while only the middle is stretched.
    """
    cap = URLBAR_CAP_WIDTH
    orig_width, orig_height = urlbar.size
    if 2 * cap > orig_width:
        cap = orig_width // 2
    left_part = urlbar.crop((0, 0, cap, orig_height))
    right_part = urlbar.crop((orig_width - cap, 0, orig_width, orig_height))
    middle_part = urlbar.crop((cap, 0, orig_width - cap, orig_height))
    target_middle_width = target_width - 2 * cap
    if target_middle_width < 0:
        target_middle_width = 0
    resized_middle = middle_part.resize((target_middle_width, orig_height), resample=Image.Resampling.LANCZOS)
    new_urlbar = Image.new("RGBA", (target_width, orig_height))
    new_urlbar.paste(left_part, (0, 0))
    new_urlbar.paste(resized_middle, (cap, 0))
    new_urlbar.paste(right_part, (cap + target_middle_width, 0))
    return new_urlbar

def paste_urlbar(temp_image, width):
    """
    Resize the urlbar so its height becomes TARGET_ELEMENT_HEIGHT, then stretch its middle section
    so that it spans from URLBAR_LEFT_MARGIN to (width - URLBAR_RIGHT_MARGIN), and paste it.
    """
    urlbar = get_urlbar_image()
    if not urlbar:
        return
    scaled_width = int(urlbar.width * (TARGET_ELEMENT_HEIGHT / urlbar.height))
    scaled_urlbar = urlbar.resize((scaled_width, TARGET_ELEMENT_HEIGHT), resample=Image.Resampling.LANCZOS)
    target_width = width - URLBAR_LEFT_MARGIN - URLBAR_RIGHT_MARGIN
    stretched_urlbar = stretch_urlbar(scaled_urlbar, target_width)
    temp_image.paste(stretched_urlbar, (URLBAR_LEFT_MARGIN, ICON_TOP_MARGIN), stretched_urlbar)

def paste_icon(temp_image, width):
    """
    Resize the icon so its height becomes TARGET_ELEMENT_HEIGHT and paste it at the top right,
    respecting ICON_RIGHT_MARGIN.
    """
    icon = get_icon_image()
    if not icon:
        return
    aspect = icon.width / icon.height
    target_width = int(aspect * TARGET_ELEMENT_HEIGHT)
    resized_icon = icon.resize((target_width, TARGET_ELEMENT_HEIGHT), resample=Image.Resampling.LANCZOS)
    x = width - ICON_RIGHT_MARGIN - resized_icon.width
    y = ICON_TOP_MARGIN
    temp_image.paste(resized_icon, (x, y), resized_icon)

def paste_top_elements(temp_image, width):
    """For landscape images, overlay the urlbar and icon onto the top bar."""
    paste_urlbar(temp_image, width)
    paste_icon(temp_image, width)

def process_image_content(original_image):
    """
    If the screenshot is landscape (width > height), add a light gray top bar and overlay the top elements.
    Otherwise, return a copy.
    """
    width, height = original_image.size
    if width > height:
        new_height = height + TOP_BAR_HEIGHT
        temp_image = Image.new('RGB', (width, new_height), TOP_BAR_COLOR)
        temp_image.paste(original_image, (0, TOP_BAR_HEIGHT))
        paste_top_elements(temp_image, width)
        return temp_image
    else:
        return original_image.copy()

def add_dark_border(image):
    """
    Add a dark gray border (of thickness BORDER_SIZE) with rounded corners (OUTER_RADIUS)
    around the image.
    """
    inner_width, inner_height = image.size
    final_width = inner_width + 2 * BORDER_SIZE
    final_height = inner_height + 2 * BORDER_SIZE
    final_image = Image.new('RGBA', (final_width, final_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(final_image)
    draw.rounded_rectangle((0, 0, final_width, final_height), radius=OUTER_RADIUS, fill=BORDER_COLOR)
    inner_mask = create_rounded_mask((inner_width, inner_height), OUTER_RADIUS - BORDER_SIZE)
    final_image.paste(image.convert("RGBA"), (BORDER_SIZE, BORDER_SIZE), inner_mask)
    outer_mask = create_rounded_mask((final_width, final_height), OUTER_RADIUS)
    final_image.putalpha(outer_mask)
    return final_image

def create_enhanced_screenshot(image_path):
    """
    Create the basic enhanced mock from a screenshot by applying the top bar and dark border.
    """
    original_image = Image.open(image_path)
    processed_image = process_image_content(original_image)
    final_image = add_dark_border(processed_image)
    return final_image

# ------------------------- Background Processing -------------------------
def process_background_for_canvas(bg_path, canvas_size):
    """
    Load the background image and scale+center-crop it to exactly the given canvas_size.
    """
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

# ------------------------- Canvas Placement -------------------------
def place_image_on_canvas(image, canvas_size, margin):
    """
    Scale the given image as large as possible so that it fits within the area defined by
    canvas_size minus 2*margin, then center it on a transparent canvas of size canvas_size.
    """
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

def combine_images_horizontally(images, canvas_size, combined_gap=COMBINED_GAP, border_gap_ratio=BORDER_GAP_RATIO):
    """
    Combine a list of images (all basic mocks) horizontally on a canvas of canvas_size.
    All images are scaled to have the same height.
    The gap between images is fixed to combined_gap.
    The entire group is centered on the canvas, leaving a margin equal to
    border_gap_ratio * min(canvas_width, canvas_height) at the edges.
    Returns the composite image.
    """
    canvas_w, canvas_h = canvas_size
    border_gap = int(min(canvas_w, canvas_h) * border_gap_ratio)
    n = len(images)
    available_width = canvas_w - 2 * border_gap - combined_gap * (n - 1)
    available_height = canvas_h - 2 * border_gap

    # For uniform height, set each image's height to available_height.
    widths = [img.width * available_height / img.height for img in images]
    total_width = sum(widths)
    if total_width > available_width:
        scale = available_width / total_width
        final_height = int(available_height * scale)
        final_widths = [int(w * scale) for w in widths]
    else:
        final_height = int(available_height)
        final_widths = [int(w) for w in widths]
    group_width = sum(final_widths) + combined_gap * (n - 1)
    start_x = (canvas_w - group_width) // 2
    start_y = (canvas_h - final_height) // 2

    composite = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    current_x = start_x
    for idx, img in enumerate(images):
        resized = img.resize((final_widths[idx], final_height), resample=Image.Resampling.LANCZOS)
        composite.paste(resized, (current_x, start_y), resized)
        current_x += final_widths[idx] + combined_gap
    return composite

# ------------------------- Directory & Resolution Processing -------------------------
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def read_resolutions_file(subfolder_path):
    """
    Read resolutions.txt (if it exists) in the given subfolder.
    Returns a list of (width, height) tuples.
    """
    res_file = os.path.join(subfolder_path, "resolutions.txt")
    resolutions = []
    if os.path.isfile(res_file):
        with open(res_file, "r") as f:
            for line in f:
                line = line.strip()
                if 'x' in line:
                    parts = line.lower().split('x')
                    try:
                        w = int(parts[0].strip())
                        h = int(parts[1].strip())
                        resolutions.append((w, h))
                    except:
                        pass
    return resolutions

def all_nonempty_subsets(iterable):
    """Return all non-empty subsets of the input iterable."""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def process_subfolder(subfolder_path):
    """
    Process one subfolder:
      1. Create mocks/basic/ and generate basic enhanced mocks for each screenshot.
      2. Check if a background file exists.
      3. For each target resolution (1920x1080 plus those in resolutions.txt),
         create the folder structure:
             mocks/<resolution>/no-bg/standalone, mocks/<resolution>/no-bg/combined,
             and if a bg file exists, mocks/<resolution>/bg/standalone, mocks/<resolution>/bg/combined.
         Also, optimize and save the background for that resolution.
      4. For each basic mock, place it on a canvas of that resolution:
             - In no-bg/standalone, use a fixed margin of 20px.
             - In bg/standalone, use margin = 15% of the smaller resolution dimension.
      5. For combined mockups, generate one composite image for every non-empty subset of basic mocks
         that contains at least two images. For each combination, randomize the order and combine them
         horizontally, with a fixed gap (20px) between images and a margin of 2% (of the smaller dimension)
         to the canvas edge. Save these in no-bg/combined and, if a background exists, in bg/combined.
    """
    print(f"Processing subfolder: {subfolder_path}")
    # Create mocks/ folder.
    mocks_dir = os.path.join(subfolder_path, "mocks")
    ensure_dir(mocks_dir)

    # Create basic mocks folder.
    basic_dir = os.path.join(mocks_dir, "basic")
    ensure_dir(basic_dir)

    # Find screenshots (ignore files starting with "bg", "mocks", etc.)
    screenshot_files = [f for f in os.listdir(subfolder_path)
                        if f.lower().endswith(ALLOWED_EXTENSIONS)
                        and not f.lower().startswith("bg")
                        and not f.lower().startswith("mocks")
                        and os.path.isfile(os.path.join(subfolder_path, f))]

    basic_mocks = []
    for fname in screenshot_files:
        img_path = os.path.join(subfolder_path, fname)
        try:
            enhanced = create_enhanced_screenshot(img_path)
            out_path = os.path.join(basic_dir, fname)
            # Convert to RGB if saving as JPEG
            if fname.lower().endswith(('.jpg', '.jpeg')):
                enhanced = enhanced.convert('RGB')
            enhanced.save(out_path)
            basic_mocks.append(out_path)
            print(f"Basic mock saved: {out_path}")
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

    # Check for background file.
    bg_path = None
    for f in os.listdir(subfolder_path):
        if f.lower().startswith("bg") and f.lower().endswith(ALLOWED_EXTENSIONS):
            bg_path = os.path.join(subfolder_path, f)
            break

    # Determine target resolutions: always include 1920x1080, plus those in resolutions.txt.
    target_resolutions = [(1920, 1080)]
    target_resolutions.extend(read_resolutions_file(subfolder_path))
    # Remove duplicates.
    target_resolutions = list({res: res for res in target_resolutions}.values())

    for res in target_resolutions:
        res_str = f"{res[0]}x{res[1]}"
        res_dir = os.path.join(mocks_dir, res_str)
        ensure_dir(res_dir)
        # Optimize background if available.
        optimized_bg = None
        if bg_path:
            optimized_bg = process_background_for_canvas(bg_path, res)
            bg_opt_path = os.path.join(res_dir, "optimized_bg.png")
            optimized_bg.save(bg_opt_path)
            print(f"Optimized bg saved: {bg_opt_path}")
        # Create subdirectories.
        no_bg_standalone = os.path.join(res_dir, "no-bg", "standalone")
        no_bg_combined = os.path.join(res_dir, "no-bg", "combined")
        ensure_dir(no_bg_standalone)
        ensure_dir(no_bg_combined)
        if optimized_bg:
            bg_standalone = os.path.join(res_dir, "bg", "standalone")
            bg_combined = os.path.join(res_dir, "bg", "combined")
            ensure_dir(bg_standalone)
            ensure_dir(bg_combined)
        # For each basic mock, place it on a canvas.
        for bm in basic_mocks:
            mock_img = Image.open(bm).convert("RGBA")
            placed_no_bg = place_image_on_canvas(mock_img, res, NO_BG_MARGIN)
            out_path = os.path.join(no_bg_standalone, os.path.basename(bm))
            # Convert to RGB if saving as JPEG
            if out_path.lower().endswith(('.jpg', '.jpeg')):
                placed_no_bg = placed_no_bg.convert('RGB')
            placed_no_bg.save(out_path)
            print(f"No-bg standalone saved: {out_path}")
            if optimized_bg:
                margin_bg = int(min(res) * BG_MARGIN_PERCENT)
                placed_bg = place_image_on_canvas(mock_img, res, margin_bg)
                composite = optimized_bg.copy()
                composite.paste(placed_bg, (0, 0), placed_bg)
                out_path_bg = os.path.join(bg_standalone, os.path.basename(bm))
                # Convert to RGB if saving as JPEG
                if out_path_bg.lower().endswith(('.jpg', '.jpeg')):
                    composite = composite.convert('RGB')
                composite.save(out_path_bg)
                print(f"Bg standalone saved: {out_path_bg}")

        # Combined mockups: generate one composite for every non-empty subset of basic mocks with at least two images.
        if basic_mocks:
            imgs_all = [Image.open(path).convert("RGBA") for path in basic_mocks]
            combo_index = 1
            # Only generate combinations with at least 2 images.
            for combo in chain.from_iterable(combinations(imgs_all, r) for r in range(2, len(imgs_all)+1)):
                combo_list = list(combo)
                random.shuffle(combo_list)
                combined_no_bg = combine_images_horizontally(combo_list, res, combined_gap=COMBINED_GAP, border_gap_ratio=BORDER_GAP_RATIO)
                out_name = f"combined_{combo_index}.png"
                out_combined_no_bg = os.path.join(no_bg_combined, out_name)
                combined_no_bg.save(out_combined_no_bg)
                print(f"Combined no-bg saved: {out_combined_no_bg}")
                if optimized_bg:
                    combined_bg = combine_images_horizontally(combo_list, res, combined_gap=COMBINED_GAP, border_gap_ratio=BORDER_GAP_RATIO)
                    composite_bg = optimized_bg.copy()
                    composite_bg.paste(combined_bg, (0, 0), combined_bg)
                    out_combined_bg = os.path.join(bg_combined, out_name)
                    composite_bg.save(out_combined_bg)
                    print(f"Combined bg saved: {out_combined_bg}")
                combo_index += 1

def process_all_subfolders():
    """Loop through direct subfolders of BASE_PATH and process each."""
    for subfolder in os.listdir(BASE_PATH):
        subfolder_path = os.path.join(BASE_PATH, subfolder)
        if os.path.isdir(subfolder_path):
            process_subfolder(subfolder_path)

# ------------------------- Main -------------------------
if __name__ == '__main__':
    process_all_subfolders()
