from PIL import Image
import io

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
from scraper.utils.gcp import upload_blob_from_memory,download_blob_into_memory,upload_blob,download_blob,create_bucket_class_location

OUT_DIR = os.path.join(ROOT_FILE,'result','image')

def create_bucket_test():
    create_bucket_class_location('test_create_example-1')

def memory_test():
    pic_url = 'https://scontent.fbkk29-1.fna.fbcdn.net/v/t1.6435-1/79985008_1873733289437672_221552074033201152_n.jpg?stp=dst-jpg_p320x320&_nc_cat=101&ccb=1-7&_nc_sid=7206a8&_nc_eui2=AeEBfl--880ryc4PTj7w9oJVwvl0jPGDDiTC-XSM8YMOJMwMEE8XZzVG_kLTZvuc9_u0pe49jww30jf3SZ2nRcCY&_nc_ohc=AAVcHwtXpx8AX91D6gx&_nc_ht=scontent.fbkk29-1.fna&oh=00_AT8rTlnBuf33vM4eWGraceRg4-KPB-jDh-qYipXwgt6pCg&oe=630DEA53'
    
    user_id = '1000040305797032'
    image_content = download_image(file_name=user_id,
                                   img_url=pic_url,
                                   out_dir=OUT_DIR,
                                   local_save=False)
    if not image_content:
        print("No_image")
        return
    
    upload_blob_from_memory(bucket_name='test-image-example-1',
                            contents=image_content,
                            destination_blob_name=user_id)
    
    # return 
    image_recv = download_blob_into_memory(bucket_name='test-image-example-1',
                              blob_name=user_id)
    
    image = Image.open(io.BytesIO(image_recv))
    # image = Image.open(io.BytesIO(image_recv))
    file_path = os.path.join(OUT_DIR,user_id+'.jpg')
    print("Path=",file_path)
    try:
        with open(file_path,"wb") as f:
            image.save(f,format='JPEG', subsampling=0, quality=95)
    except :
        os.makedirs(OUT_DIR)
        with open(file_path,"wb") as f:
            image.save(f,format='JPEG', subsampling=0, quality=95)
        
    print("Image id: {} has been save".format(user_id))

def local_test():
    pic_url = 'https://scontent.fbkk29-1.fna.fbcdn.net/v/t1.6435-1/79985008_1873733289437672_221552074033201152_n.jpg?stp=dst-jpg_p320x320&_nc_cat=101&ccb=1-7&_nc_sid=7206a8&_nc_eui2=AeEBfl--880ryc4PTj7w9oJVwvl0jPGDDiTC-XSM8YMOJMwMEE8XZzVG_kLTZvuc9_u0pe49jww30jf3SZ2nRcCY&_nc_ohc=AAVcHwtXpx8AX91D6gx&_nc_ht=scontent.fbkk29-1.fna&oh=00_AT8rTlnBuf33vM4eWGraceRg4-KPB-jDh-qYipXwgt6pCg&oe=630DEA53'
    
    user_id = '100004030579703'
    image_content = download_image(file_name=user_id,
                                   img_url=pic_url,
                                   out_dir=OUT_DIR,
                                   local_save=True)
    if not image_content:
        print("No_image")
        return
    
    upload_blob(bucket_name='test-image-example-1',
                source_file_name=os.path.join(OUT_DIR,user_id+'.jpg'),
                destination_blob_name=user_id)
    
    try:
        download_blob(bucket_name='test-image-example-1',
                              source_blob_name=user_id,
                              destination_file_name=os.path.join(OUT_DIR,user_id+'.jpg'))
    except :
        os.makedirs(OUT_DIR)
        download_blob(bucket_name='test-image-example-1',
                              source_blob_name=user_id,
                              destination_file_name=os.path.join(OUT_DIR,user_id+'.jpg'))
        
if __name__ == '__main__':
    memory_test()