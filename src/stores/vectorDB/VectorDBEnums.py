from enum import Enum

class VectorDBEnums(Enum):

   QDRANT=  "QDRANT"  
   PGVECTOR="PGVECTOR"

class DistanceMethodEnums(Enum):

   COSINE="COSINE"
   DOT="Dot"
