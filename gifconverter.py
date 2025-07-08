import os
from PIL import Image

def convert_gif_to_jpeg(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Only process .gif files
        if filename.lower().endswith('.gif'):
            try:
                with Image.open(file_path) as img:
                    # Get the first frame of the GIF
                    img.seek(0)
                    frame = img.convert('RGB')  # Convert to RGB for JPEG

                    # Create new JPEG filename
                    jpeg_filename = os.path.splitext(filename)[0] + ".jpeg"
                    jpeg_path = os.path.join(folder_path, jpeg_filename)

                    # Save as JPEG
                    frame.save(jpeg_path, 'JPEG')

                    # Remove original GIF
                    os.remove(file_path)

                    print(f"Converted and replaced: {filename} -> {jpeg_filename}")
            except Exception as e:
                print(f"Error converting {filename}: {e}")

# Example usage
folder = "img"
convert_gif_to_jpeg(folder)
