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
    PROJECT_NOT_FOUND="no project found"
    INSERT_INTO_VECTORDB_ERROR="insert_into_vectordb_error"
    INSERT_INTO_VECTORDB_SUCCESS="insert_into_vectordb_SUCCESS"
    VECTORDB_COLLECTION_RETRIEVED="VECTORDB_COLLECTION_RETRIEVED"
    VECTOR_DB_SEARCH_SUCCESS="VECTOR_DB_SEARCH_SUCCESS"
    VECTOR_DB_SEARCH_ERROR="VECTOR_DB_SEARCH ERROR"
    RAG_ANSWER_ERROR="RAG_ANSWER_ERROR"
    RAG_ANSWER_SUCCESS="RAG_ANSWER_SUCCESS"

