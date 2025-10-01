from .BaseControllers import BaseControllers
from fastapi import UploadFile
from models import ResponseSignal
from .ProjectControllers import ProjectControllers
import re
import os
class DataControllers(BaseControllers):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576 # convert MB to bytesa


    def validate_uploaded_file(self,file:UploadFile):
    
     if file.content_type not in self.app_setting.File_allowed_extensions:
        return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
     
     
     if file.size > self.app_setting.File_max_size * self.size_scale:
        return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
     return True,ResponseSignal.FILE_VALIDATE_SUCCESS.value
   
    def generate_unique_filepath(self,orig_file_name:str,project_id:str):
       
         random_key=self.generate_random_string()
         project_path =ProjectControllers().get_project_path(project_id=project_id)
         
         clean_filename= self.get_clean_file_name(orig_file_name
                                   =orig_file_name)
         new_file_path=os.path.join(
            project_path,
           random_key + "_" + clean_filename
         )

         while os.path.exists(new_file_path):
           random_key=self.generate_random_string() 
           new_file_path=os.path.join(
            project_path,
            random_key + "_" + clean_filename
         )
         return new_file_path ,random_key + "_" + clean_filename


    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name