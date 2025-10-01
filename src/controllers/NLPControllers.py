from .BaseControllers import BaseControllers
from models.db_schemes import Project, DataChunk
from typing import List
import json
from stores.llm.LLMEnums import DOCUMENTTYPEENUM

class NLPControllers(BaseControllers):
    def __init__(self, vectordb_client, generation_client, 
                 embedding_client,template_parser):

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser
        

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()

    def reset_vector_db_collection(self, project: Project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self, project: Project, chunks: List[DataChunk], chunk_ids : List[int],
                                   do_reset: bool = False):
          

      #get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)


      #manage items in the colletion to extract what the func need

        texts = [c.chunk_text for c in chunks]
        metadata= [c.chunk_metadata for c in chunks]
    
        vectors =[
            self.embedding_client.embed_text(text=text,document_type=DOCUMENTTYPEENUM.DOCUMENT.value)
            for text in texts
        ]
    
  
      #create the collection if it does not exist
        _=self.vectordb_client.create_collection(collection_name=collection_name, 
         embedding_size=self.embedding_client.embedding_size,  
         do_reset=do_reset)


      #insert into the vector database

        vec=self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts, 
            vectors=vectors,
            metadata=metadata, 
            record_ids=chunk_ids
                         )
        print(vec)
        return True
        
    

    def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):

        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: get text embedding vector   
        vector = self.embedding_client.embed_text(text=text, 
        document_type=DOCUMENTTYPEENUM.QUERY.value)
        # print(vector)

        if not vector or len(vector) == 0:
            return False
         
        # step3: do semantic search

        results = self.vectordb_client.search_by_vector(
         collection_name = collection_name,
         vector = vector,
         limit=limit
         )
        
        # print(collection_name)
        # print(limit)
        # print(vector)
        # print(results)
        
        if not results:
            return False
        return results
    

    def answer_user_with_llm(self,project:Project,query:str,limit:int=10):
     
     
     answer, full_prompt, chat_history = None, None, None

     reterived_document=self.search_vector_db_collection(
         project=project,
         text=query,
          limit=limit
         )
     if not reterived_document or len(reterived_document) == 0:
            return answer, full_prompt, chat_history
     
     #step 2: construct LLM prompt

     system_prompt = self.template_parser.get("rag", "system_prompt")

     documents_prompts = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                    "doc_num": idx + 1,
                    "chunk_text": doc.text,
            })
            for idx, doc in enumerate(reterived_document)
        ])
     
     footer_prompt = self.template_parser.get("rag", "footer_prompt",{
         "query":query
     })

        # step3: Construct Generation Client Prompts
     chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

     full_prompt = "\n\n".join([ documents_prompts,  footer_prompt])

        # step4: Retrieve the Answer
     answer = self.generation_client.gernerate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )

     return answer, full_prompt, chat_history





