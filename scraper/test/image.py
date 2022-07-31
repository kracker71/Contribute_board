import sys
import os
from pathlib import Path


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0].parents[0].parents[0]  # backend root directory
ROOT_FILE = FILE.parents[0].parents[0]
# print(FILE)
# print(ROOT)

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / 'backend') not in sys.path:
    sys.path.append(str(ROOT / 'backend'))  # add backend ROOT to PATH

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from scraper.utils.image import download_image

def image_download_test(out_dir,img_url,file_name):
    download_image(out_dir,img_url,file_name)
    
if __name__ == '__main__':
    url = r'https://www.shutterstock.com/th/search/imagre'
    url_2 = 'https://scontent.fbkk29-1.fna.fbcdn.net/v/t1.6435-1/79985008_1873733289437672_221552074033201152_n.jpg?stp=dst-jpg_p320x320&_nc_cat=101&ccb=1-7&_nc_sid=7206a8&_nc_ohc=_PvMK9GUAk8AX8CO9hZ&_nc_ht=scontent.fbkk29-1.fna&oh=00_AT_B6774hp6W5ZiLZLN8InYlFtARuoGrPnyhiz--5T9iig&oe=6309F5D3'
    url_3 = 'https://scontent.fbkk22-2.fna.fbcdn.net/v/t39.30808-1/220250863_1147898959013177_2904226116532179432_n.jpg?stp=dst-jpg_p100x100&_nc_cat=106&ccb=1-7&_nc_sid=7206a8&_nc_ohc=o0x8tVCXYPQAX9781ON&_nc_ht=scontent.fbkk22-2.fna&oh=00_AT8CmUGJagNXSxRJdbZyTBI0xf2Av46zN_44Hzu9U80BiA&oe=62E083FE'
    
    download_image(os.path.join(ROOT_FILE,'result','image'),url_3,'2')