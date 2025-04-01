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

## Advanced Usage/Configuration

### Properties You Can

> [!WARNING]
> Planned feature. Not yet implemented.

#### Specifying Input Files

| **short flag** | **long flag** | **config variable** |
|----------------|---------------|---------------------|
| `-i`         | `--input`      | `input`             |

the screenshots you want to have mocked up

glob pattern/files

`*.{jpg,png,webp}`

`*png screenshot3.jpg`

---

#### Defining the Output Directory

| **short flag** | **long flag** | **config variable** |
|----------------|---------------|---------------------|
| `-o`         | `--output`     | `output`            |

the directory where to output your mockups to

path of directory

directory will be created if it doesn't exist

---

#### Locating Template Files

| **short flag** | **long flag** | **config variable** |
|----------------|---------------|---------------------|
| `-t`         | `--templates`  | `templates`         |

the directory in which your mockup templates are to be found

---

#### Setting Padding Around Mockups

| **short flag** | **long flag** | **config variable** |
|----------------|---------------|---------------------|
| `-p`         | `--padding`    | `padding`           |

the distance from the mockups to the edge of the output image

single number  
four numbers

`10`  
`10 10 30 10`

---

#### Setting Margin for Background

| **short flag** | **long flag** | **config variable** |
|----------------|---------------|---------------------|
| `-m`         | `--margin`     | `margin`            |

the (extra) distance from your mockups to the edge of the output image, if using a background image

single number  
four numbers

`50`  
`30 50 25 50`

---

#### Specifying Image Resolutions

| **short flag** | **long flag**   | **config variable** |
|----------------|-----------------|---------------------|
| `-r`         | `--resolutions` | `resolutions`       |

the image resolution of the generated mockups

space-separated list of pixel resolutions

`1920x1080`

`3000x2000 800x568`

---

#### Combining Inputs into One Mockup

| **short flag** | **long flag**           | **config variable** |
|----------------|-------------------------|---------------------|
| —              | `--only-combined`       | —                   |

---

#### Creating Standalone Mocks

| **short flag** | **long flag**           | **config variable** |
|----------------|-------------------------|---------------------|
| —              | `--only-standalone`     | —                   |

make only mocks where the screenshots are displayed alone

---

#### Generating All Combinations

| **short flag** | **long flag**                   | **config variable** |
|----------------|---------------------------------|---------------------|
| —              | `--all-possible-combinations`   | —                   |

---

#### Using a Flat Output Directory

| **short flag** | **long flag**                 | **config variable** |
|----------------|-------------------------------|---------------------|
| —              | `--flat-output-directory`     | —                   |

do not structure the output into subfolders, flatly list them in the specified directory

---

#### Config File Location

| **short flag** | **long flag** | **config variable** |
|----------------|---------------|---------------------|
| `-c`         | `--config`     | —                   |

path to your config file
