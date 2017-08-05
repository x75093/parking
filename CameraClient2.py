import boto3                                                                    
import cv2                                                                      
import time                                                                     
import os                                                                       
import subprocess                                                               
from PIL import Image                                                           
from datetime import datetime 
#test
                                                                                
class CameraClient(object):                                                     
                                                                                
    def __init__(self, location_id):                                            
        self.location_id = location_id                                          
        self.s3 = {"client": boto3.resource('s3'), "bucket": "parking-spots2" }  
        self.dynamodb_client = boto3.resource('dynamodb')                       
        self.tables = { "Harvard_Allston": self.dynamodb_client.Table("Harvard_Allston") }          
                                                                                
    def snap_photo(self):                                                       
        cap = cv2.VideoCapture(2)                                               
        ret, image = cap.read()                                                 
        cap.release()                                                           
        return self.__get_image_data(Image.fromarray(image))


    def get_filename(self):
        return self.location_id + "_" + str(datetime.strftime( datetime.now() , '%Y-%m-%d %H:%M:%S' )) + ".jpg"

    def upload_image(self, img_data, img_filename):
        self.s3["client"].Bucket(self.s3["bucket"]).put_object(Key = img_filename, Body = img_data)
        time.sleep(self.__get_sleep_time())

    def write_to_db(self, img_filename):                                        
        self.tables["Harvard_Allston"].update_item(                                       
            Key={'location_id': self.location_id },                             
            UpdateExpression="set image_name = :i, updated=:u, dtg=:d, ip_address= :ip",
            ExpressionAttributeValues={                                         
                ':i': img_filename,                                             
                ':u': True,                                                     
                ':d': False,
                ':ip': subprocess.Popen("ip route get 1 | awk '{print $NF;exit}'", stdout=subprocess.PIPE, shell=True).communicate()[0],
            },                                                                  
            ReturnValues="UPDATED_NEW"                                          
        )

    ### Private Methods                                                         
    def __get_sleep_time(self):                                                 
        return self.tables["Harvard_Allston"].get_item(Key={'location_id': self.location_id})["Item"]["sleep"]
                                                                                
    def __get_image_data(self, img, tmp_filename = "tmp.jpg"):                  
        img.save(tmp_filename)                                                  
        img_binary_data = open(tmp_filename, 'rb')                              
        os.remove(tmp_filename)                                                 
        return img_binary_data                                                  
                                                                                
LOCATION_ID = "Harvard_Allston_01c"                                                         
client = CameraClient(LOCATION_ID)                                              
img_data = client.snap_photo()                                                  
img_filename = client.get_filename()                                            
client.upload_image(img_data, img_filename)                                     
client.write_to_db(img_filename)  
