from enum import Enum

class LLMEnum(Enum):

    OPENAI="OPENAI"
    COHERE="COHERE"

class OPENAIEnums(Enum):
    SYSTEM="system"
    ASSISTANT="assistant"
    USER="user"    

class COHEREENUMS(Enum):
    SYSTEM="system"
    ASSISTANT="assistant"
    USER="chatbot"
    DOCUMENT="search_document"
    QUERY="search_query"

 
class DOCUMENTTYPEENUM(Enum):
    DOCUMENT="document"
    QUERY="query"