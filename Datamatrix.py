from pylibdmtx.pylibdmtx import encode
import os
import re
from PIL import Image, ImageDraw, ImageFont
CURRENT_DIR = os.path.dirname(__file__)

def read_serials_from_file(file):
    """Read serial numbers from a file and return them as a list.

    Args:
        file (str): The path to the file containing the serial numbers.

    Returns:
        list: A list of strings representing the serial numbers.
    """
    with open(file, 'r') as file:
        serials = [re.sub(r"\s+", "", line.strip()) for line in file.readlines()]
    return serials

def generate_datamatrix(serials, output_path):
    """
    Generate a data matrix from a list of serial numbers.
    Parameters:
        input_file (str): The path to the file containing the serial numbers.
        output_path (str): The path to save the generated data matrices.
    """
    def create_qr_image(serials):
        data = '\r\n'.join(serials) 
        encoded = encode(data.encode('utf-8'))    
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        new_width = 200
        aspect_ratio = img.height / img.width
        new_height = int(new_width * aspect_ratio)
    
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        return resized_img
    
    # Split serials into two groups
    if 100 <= len(serials) < 200:
        first_group = serials[:100]
        second_group = serials[100:]
    
        #generate QR code from both groups
        img1 = create_qr_image(first_group)
        img2 = create_qr_image(second_group)
    
        # Combine the two images into one
        combined_width = img1.width + img2.width + 40
        combined_height = max(img1.height, img2.height) + 40
        combined_img = Image.new('RGB', (combined_width, combined_height), "white")

        #creating drawing context for captions
        draw = ImageDraw.Draw(combined_img)
        font = ImageFont.load_default()
        draw.text((20, 5), 'QR for first 100 serials', fill="black", font=font)
        draw.text((img1.width + 40, 5), 'QR for remaining serials', fill="black", font=font)
        # Paste the images into the new image
        combined_img.paste(img1, (10, 20))
        combined_img.paste(img2, (img1.width + 20, 20))
        

        
        combined_img.save(output_path)
    
    else:
        img = create_qr_image(serials)
        img.save(output_path)
    
    
def main(input_file, output_path):
    """
    Generate a data matrix from a list of serial numbers.
    Parameters:
        input_file (str): The path to the file containing the serial numbers.
        output_path (str): The path to save the generated data matrices.
    """
    serials = read_serials_from_file(input_file)
    generate_datamatrix(serials, output_path)
    print("Generated DataMatrix for all serials")

if __name__ == "__main__":
    input_file = os.path.join(CURRENT_DIR, "Data//serials.txt") 
    output_path = os.path.join(CURRENT_DIR,"Data//Qrcode_for_all_serials.png")

    main(input_file, output_path)