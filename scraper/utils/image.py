from fileinput import filename
import requests
import io
from PIL import Image
import os

def download_image(out_dir,img_url,file_name,local_save):
    fail_list=[]
    
    try:
        image_content = requests.get(img_url).content      
        if local_save:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)
            file_path = os.path.join(out_dir,file_name+'.jpg')
            print("Path=",file_path)
            try:
                with open(file_path,"wb") as f:
                    image.save(f,format='JPEG', subsampling=0, quality=95)
            except :
                os.makedirs(out_dir)
                with open(file_path,"wb") as f:
                    image.save(f,format='JPEG', subsampling=0, quality=95)
                
            print("Image id: {} has been save".format(file_name))
        # return image_file.getvalue()
        return image_content
        
    except Exception as e:
        fail_list.append(file_name)
        print("Fail:",e)
        
    return fail_list
        