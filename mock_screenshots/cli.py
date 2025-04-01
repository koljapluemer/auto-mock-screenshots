import argparse
import os
from .core import process_directory

def main():
    parser = argparse.ArgumentParser(description='Generate mockups from screenshots')
    parser.add_argument('--input-dir', '-i', default='.',
                      help='Input directory containing screenshots (default: current directory)')
    parser.add_argument('--output-dir', '-o', default='.',
                      help='Output directory for generated mockups (default: current directory)')
    args = parser.parse_args()

    # Convert relative paths to absolute
    input_dir = os.path.abspath(args.input_dir)
    output_dir = os.path.abspath(args.output_dir)

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Change to input directory to process files
    original_dir = os.getcwd()
    os.chdir(input_dir)
    
    try:
        process_directory('.', output_dir)
    finally:
        # Always change back to original directory
        os.chdir(original_dir)

if __name__ == '__main__':
    main() 