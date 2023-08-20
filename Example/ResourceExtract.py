import os
import shutil
from PyQt5.QtGui import QImage
from QtResources import qt_resource_data


class ImageExtractor:

    def clean_junk(self, folder_name):
        try:
            path = os.path.join(os.path.dirname(__file__), folder_name)
            if os.path.exists(path) and os.path.isdir(path):
                shutil.rmtree(path)
                print("\n[ ✔ ] Cleaned Junk")
        except Exception as e:
            print(f"[ ✗ ] An error occurred while cleaning junk: {e}")

    def extract_images_from_resources(self):
        try:
            resource_data = qt_resource_data  # No need to decode binary data for PNG / JPG images

            # Create a directory to store the extracted images
            directory = "extracted_images"
            os.makedirs(directory, exist_ok=True)

            jpg_count = 0
            png_count = 0
            svg_count = 0

            offset = 0

            # Iterate over the resource data and extract images
            while offset < len(resource_data):
                # Find the start and end positions of the image
                if resource_data[offset] == 0xFF and resource_data[offset + 1] == 0xD8:
                    # JPG/JPEG image
                    start_marker = b"\xFF\xD8"  # JPG/JPEG file signature
                    end_marker = b"\xFF\xD9"
                    file_type = "jpg"
                elif resource_data[offset] == 0x89:
                    # PNG image
                    start_marker = b"\x89PNG"  # PNG file signature
                    end_marker = b"IEND"
                    file_type = "png"
                elif resource_data[offset] == 0x3C:
                    # SVG image
                    start_marker = b"<svg"  # SVG opening tag
                    end_marker = b"</svg>"
                    file_type = "svg"
                else:
                    # Not a recognized image format, skip to the next byte
                    offset += 1
                    continue

                start_pos = resource_data.find(start_marker, offset)

                if start_pos == -1:
                    break

                end_pos = resource_data.find(end_marker, start_pos)
                if end_pos == -1:
                    break

                # Extract the image data
                image_data = resource_data[start_pos:end_pos + len(end_marker)]

                # Save the image to a file
                if file_type == "jpg":
                    jpg_count += 1
                    filename = f"jpg_{jpg_count}.{file_type}"
                elif file_type == "png":
                    png_count += 1
                    filename = f"png_{png_count}.{file_type}"
                elif file_type == "svg":
                    svg_count += 1
                    filename = f"svg_{svg_count}.{file_type}"

                filepath = os.path.join(directory, filename)
                with open(filepath, 'wb') as f:
                    f.write(image_data)

                print(f"[ → ] {file_type.upper()} image {filename} extracted and saved as '{filepath}'")

                # Update the offset to search for the next image
                offset = end_pos + len(end_marker)

            if all(count == 0 for count in [jpg_count, png_count, svg_count]):
                print("[ ✗ ] No images found in the resource data")

            self.clean_junk("__pycache__")

        except Exception as e:
            print(f"[ ✗ ] An error occurred while extracting images from resources: {e}")


if __name__ == "__main__":
    extractor = ImageExtractor()
    extractor.extract_images_from_resources()
    print("[ ✔ ] Job Completed")
