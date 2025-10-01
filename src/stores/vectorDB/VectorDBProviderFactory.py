from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBEnums
from controllers.BaseControllers import BaseControllers
 

class VectorDBProviderFactory:

    def __init__(self,config:dict):
        self.config=config
        self.base_controllers=BaseControllers()



    def create(self,provider:str):
        if provider == VectorDBEnums.QDRANT.value:
          db_path=self.base_controllers.get_database_path(db_name=self.config.VECTOR_DB_PATH)
          return QdrantDBProvider(
            db_path=db_path,
            distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
            )
        
    
        return None



        
     