from enum import Enum

class ResponseSignal(Enum):


    FILE_VALIDATE_SUCCESS="FILE UPLOADED SUCCESSFULLY"
    FILE_TYPE_NOT_SUPPORTED="File type  is not allowed."
    FILE_SIZE_EXCEEDED="File size is larger than expected" 
    FILE_UPLOAD_SUCCESS="file upload success"
    FILE_UPLOAD_FAILED="file upload failed"
    PROCESSING_FAILED="processing failed"
    PROCESSING_Success="processing success"
    NO_FILES_ERRORS="No Files Found"
    FILE_ID_ERROR="no file found with this id"