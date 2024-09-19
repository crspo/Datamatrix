from pylibdmtx.pylibdmtx import encode
import os
from PIL import Image
CURRENT_DIR = os.path.dirname(__file__)

def read_serials_from_file(file):
    """Read serial numbers from a file and return them as a list.

    Args:
        file (str): The path to the file containing the serial numbers.

    Returns:
        list: A list of strings representing the serial numbers.
    """
    with open(file, 'r') as file:
        serials = [line.strip() for line in file.readlines()]
    return serials

def generate_datamatrix(serials, output_path):
    """
    Generate a data matrix from a list of serial numbers.
    Parameters:
        input_file (str): The path to the file containing the serial numbers.
        output_path (str): The path to save the generated data matrices.
    """
    data = '\r\n'.join(serials)
    
    encoded = encode(data.encode('utf-8'))    
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    new_width = 200
    aspect_ratio = img.height / img.width
    new_height = int(new_width * aspect_ratio)
    
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    
    resized_img.save(output_path)
    
    
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