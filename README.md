# Mock Screenshots

A tool to automatically generate mockups from screenshots. This tool adds browser-like elements (top bar, URL bar, icons) to screenshots and can create various combinations of them with or without backgrounds.

Usable on my system with a bash alias now:

```bash
alias mock-screenshots='~/.local/venv/mock-screenshots/bin/mock-screenshots'
```

...after installing like follows:

```sh
python3 -m venv ~/.local/venv/mock-screenshots
source ~/.local/venv/mock-screenshots/bin/activate
cd /home/brokkoli/GITHUB/auto-mock-screenshots
pip install -e .
```
(and adding the alias to my `.bashrc`)

## General Installation

```bash
pip install mock-screenshots
```

## Usage

The tool can be used from the command line:

```bash
mock-screenshots [--input-dir INPUT_DIR] [--output-dir OUTPUT_DIR]
```

### Arguments

- `--input-dir`, `-i`: Directory containing the screenshots (default: current directory)
- `--output-dir`, `-o`: Directory where the generated mockups will be saved (default: current directory)

### Input Directory Structure

The tool expects the following structure in the input directory:

```
input_dir/
├── screenshot1.png
├── screenshot2.png
├── bg.png
└── resolutions.txt
```

- Place all screenshots directly in the input directory
- Optionally, you can add a `bg.png` file to use as a background
- Optionally, you can add a `resolutions.txt` file with custom resolutions (one per line, format: `WIDTHxHEIGHT`)

### Output Structure

The tool will create the following structure in the output directory:

```
output_dir/
└── mocks/
    ├── basic/
    │   ├── screenshot1.png
    │   └── screenshot2.png
    └── 1920x1080/
        ├── no-bg/
        │   ├── standalone/
        │   └── combined/
        └── bg/
            ├── standalone/
            └── combined/
```

## Configuration

> [!WARNING]
> Planned feature. Not yet implemented.


| **short flag** | **long flag** | **config variable** | **description** | **accepted values** | **example** |  | **default** | **notes** |
|----------------|---------------|---------------------|-----------------|---------------------|-------------|--|-------------|-----------|
| `-i` | `--input` | `input` | the screenshots you want to have mocked up | `glob pattern/files` | `*png screenshot3.jpg` | will mockup all png files as well as `screenshot3.jpg` in the current working directory | `*.{jpg,png,webp}` |  |
| `-o` | `--output` | `output` | the directory where to output your mockups to | `path of directory` |  |  |  | directory will be created if it doesn't exist |
| `-t` | `--templates` | `templates` | the directory in which your mockup templates are to be found |  |  |  |  |  |
| `-p` | `--padding` | `padding` | the distance from the mockups to the edge of the output image | `single number` | `10` |  |  |  |
|  |  |  |  | `four numbers` | `10 10 30 10` |  |  |  |
| `-m` | `--margin` | `margin` | the (extra) distance from your mockups to the edge of the output image, if using a background image | `single number` | `50` |  |  |  |
|  |  |  |  | `four numbers` | `30 50 25 50` |  |  |  |
| `-r` | `--resolutions` | `resolutions` | the image resolution of the generated mockups | `space-separated list of pixel resolutions` | `3000x2000 800x568` |  | `1920x1080` |  |
|  | `--only-combined` |  |  |  |  |  |  |  |
|  | `--only-standalone` |  | make only mocks where the screenshots are displayed alone |  |  |  |  |  |
|  | `--all-possible-combinations` |  |  |  |  |  |  |  |
|  | `--flat-output-directory` |  | do not structure the output into subfolders, flatly list them in the specified directory |  |  |  |  |  |
| `-c` | `--config` |  | path to your config file | `filepath` |  |  |  |  |