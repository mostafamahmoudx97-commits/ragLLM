from .providers import QdrantDBProvider ,PGVectorProvider
from .VectorDBEnums import VectorDBEnums
from controllers.BaseControllers import BaseControllers
from sqlalchemy.orm import sessionmaker
 

class VectorDBProviderFactory:

    def __init__(self,config:dict,db_client: sessionmaker=None):
        self.config = config
        self.base_controller = BaseControllers()
        self.db_client = db_client


    def create(self,provider:str):
        if provider == VectorDBEnums.QDRANT.value:
          db_path=self.base_controllers.get_database_path(db_name=self.config.VECTOR_DB_PATH)
          return QdrantDBProvider(
            db_client=db_path,
            distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
            default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
            index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )
        

        if provider == VectorDBEnums.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )
        
    
        return None



        
     