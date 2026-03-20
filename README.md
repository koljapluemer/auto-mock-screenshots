# Mock Screenshots

*now solving this problem in [this repo](https://github.com/koljapluemer/screenshot-mock-wrapper)*

Arrange images on a canvas to create mockup compositions. Single images are centered; multiple images are laid out horizontally.

## Installation

```bash
uv tool install .
```

Or for development:

```bash
uv sync
```

## Usage

```
mock-screenshots [OPTIONS] INPUT [INPUT ...]
```

| Flag | Default | Description |
|------|---------|-------------|
| `INPUT` (positional) | — | Image files or glob patterns |
| `-o` / `--output` | `mockup.png` | Output file path |
| `-b` / `--background` | none | Background image file |
| `-r` / `--resolution` | `1920x1080` | Canvas resolution `WIDTHxHEIGHT` |
| `-p` / `--padding` | `20` | Pixels from content to canvas edge |
| `-g` / `--gap` | `20` | Pixels between images |

## Examples

Single image, default settings:

```bash
mock-screenshots screenshot.png
```

Multiple images with a background:

```bash
mock-screenshots screenshots/*.png -b wallpaper.jpg -o mockup.png
```

Custom resolution and spacing:

```bash
mock-screenshots a.png b.png -r 2560x1440 -p 40 -g 30 -o wide.png
```

## Supported Formats

PNG, JPEG, BMP, GIF, WebP
