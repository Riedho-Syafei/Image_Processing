def process_pgm(input_path, output_path, offset=100):
    try:
        with open(input_path, 'rb') as f:
            # Read the header
            header = f.readline().decode().strip() # Should be 'P5'
            if header != 'P5':
                print("Error: Input must be a P5 (binary) PGM file.")
                return

            # Skip comments and read dimensions
            line = f.readline().decode()
            while line.startswith('#'):
                line = f.readline().decode()
            
            width, height = map(int, line.split())
            max_val = int(f.readline().decode())

            # Read the raw pixel data
            pixels = list(f.read())

        # Process pixels: Add 100 and clip at 255
        # Logic: New Pixel = min(255, current_pixel + 100)
        processed_pixels = [min(255, p + offset) for p in pixels]

        # Write to new file
        with open(output_path, 'wb') as f:
            # Write PGM Header
            header_str = f"P5\n{width} {height}\n255\n"
            f.write(header_str.encode())
            # Write binary pixel data
            f.write(bytearray(processed_pixels))

        print(f"Success! Brightened image saved to {output_path}")

    except FileNotFoundError:
        print("Error: File not found.")

# Usage
process_pgm('input.pgm', 'output.pgm')