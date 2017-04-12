import boto3                                                                    
import cv2                                                                      
import time                                                                     
import os                                                                       
import subprocess                                                               
from PIL import Image                                                           
from datetime import datetime                                                   
                                                                                
class CameraClient(object):                                                     
                                                                                
    def __init__(self, location_id):                                            
        self.location_id = location_id                                          
        self.s3 = {"client": boto3.resource('s3'), "bucket": "parking-spots" }  
        self.dynamodb_client = boto3.resource('dynamodb')                       
        self.tables = { "Spots": self.dynamodb_client.Table("Spots") }          
                                                                                
    def snap_photo(self):                                                       
        cap = cv2.VideoCapture(0)                                               
        ret, image = cap.read()                                                 
        cap.release()                                                           
        return self.__get_image_data(Image.fromarray(image))

    def write_to_db(self, img_filename):                                        
        self.tables["Spots"].update_item(                                       
            Key={'location_id': self.location_id },                             
            UpdateExpression="set image_name = :i, updated=:u, dtg=:d, ip_addres= :ip, username = :un",
            ExpressionAttributeValues={                                         
                ':i': img_filename,                                             
                ':u': True,                                                     
                ':d': "T",#subprocess.Popen("date", stdout=subprocess.PIPE, shel
                ':ip': "T",#subprocess.Popen("ifconfig | sed -En 's/127.0.0.1//;
                ':un': "T",#subprocess.Popen("whoami", stdout=subprocess.PIPE, s
            },                                                                  
            ReturnValues="UPDATED_NEW"                                          
        )

    ### Private Methods                                                         
    def __get_sleep_time(self):                                                 
        return self.tables["Spots"].get_item(Key={'location_id': self.location_id})["Item"]["sleep"]
                                                                                
    def __get_image_data(self, img, tmp_filename = "tmp.jpg"):                  
        img.save(tmp_filename)                                                  
        img_binary_data = open(tmp_filename, 'rb')                              
        os.remove(tmp_filename)                                                 
        return img_binary_data                                                  
                                                                                
LOCATION_ID = "wilby_1"                                                         
client = CameraClient(LOCATION_ID)                                              
img_data = client.snap_photo()                                                  
img_filename = client.get_filename()                                            
client.upload_image(img_data, img_filename)                                     
client.write_to_db(img_filename)  