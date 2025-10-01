from fastapi import FastAPI
from routes import base ,data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectorDB.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser


app = FastAPI()

async def start_span():
    settings=get_settings()
    app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_DATABASE_url)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE] 

    LLM_provider_factory=LLMProviderFactory(settings)
    VectorDB_provider_factory=VectorDBProviderFactory(settings)

    #generation Client

    app.generation_client=LLM_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)


    #embedding Client
    app.embedding_clinet=LLM_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_clinet.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,embedding_size=settings.EMBEDDING_MODEL_SIZE)



    #VectorDB client 
    app.vectordb_client=VectorDB_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND
        )
    app.vectordb_client.connect()

    app.template_parser=TemplateParser(
        language=settings.DEFAULT_LANG,
    )
    

    
async def shudown_span():    
    app.mongo_conn.close()   
    app.vectordb_client.disconnect()



app.on_event("startup")(start_span)
app.on_event("shutdown")(shudown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
