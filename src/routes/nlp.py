from fastapi import APIRouter, FastAPI, status, Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings ,Settings
import logging
from routes.schemes.nlp import PushRequest,SearchRequest
from models.ProjectModels import ProjectModel
from models.ChunkModel import ChunkModel
from controllers.NLPControllers import NLPControllers
from models import ResponseSignal


logger=logging.getLogger('uvicorn.error')

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
)


@nlp_router.post("/index/push/{project_id}")

async def index_project(request:Request, project_id:str, push_request:PushRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client,
    )


    project=await project_model.get_project_or_create_one(
        project_id=project_id
    )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.PROJECT_NOT_FOUND.value
            }
        )
    
    nlp_controllers = NLPControllers(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_clinet,
        template_parser=request.app.template_parser
    )


    has_records=True
    page_no=1
    inserted_items_count=0
    idx = 0

    while has_records:
        page_chunk = await chunk_model.get_poject_chunks(project_id=project.id,page_no=page_no) 
        if len(page_chunk):
            page_no+=1

        if not page_chunk or len(page_chunk)==0:
            has_records=False
            break 

        chunk_ids = list(range(idx,idx + len(page_chunk))) 
        idx+= len(page_chunk)

        is_inserted = nlp_controllers.index_into_vector_db(
            project=project,
            chunks=page_chunk,
            do_reset=push_request.do_reset,
            chunk_ids=chunk_ids
        )

        if not is_inserted :
            return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.INSERT_INTO_VECTORDB_ERROR.value
            }
        )
        inserted_items_count += len(page_chunk)
        print(is_inserted)

    return JSONResponse(
            content={
                "signal":ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
                "inserted_items_count":inserted_items_count
            }
        )     











    # chunk=chunk_model.get_poject_chunks(project_id=project.project_id)

@nlp_router.get("/index/info/{project_id}")

async def get_project_index_info(project_id:str,request:Request):
     
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    
    project=await project_model.get_project_or_create_one(
        project_id=project_id
    )
    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.PROJECT_NOT_FOUND.value
            }
        )
    nlp_controllers = NLPControllers(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_clinet,
        template_parser=request.app.template_parser
    )
    

    collection_info = nlp_controllers.get_vector_db_collection_info(project=project)

    print(collection_info)
    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTORDB_COLLECTION_RETRIEVED.value,
            "collection_info": collection_info
        }
    

    )

@nlp_router.post("/index/search/{project_id}")
async def search_index(project_id:str,request:Request,search_request:SearchRequest):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project=await project_model.get_project_or_create_one(
        project_id=project_id
    )
    nlp_controllers = NLPControllers(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_clinet,
        template_parser=request.app.template_parser
    )

    results=nlp_controllers.search_vector_db_collection(project=project,text=search_request.text,limit=search_request.limit)
    print(search_request.text)
    print(results)
    if not results:
        return JSONResponse(
        content={ 
            "signal": ResponseSignal.VECTOR_DB_SEARCH_ERROR.value,
        }
        )


    return JSONResponse(
        content={ 
            "signal": ResponseSignal.VECTOR_DB_SEARCH_SUCCESS.value,
            "result":[ result. dict() for result in results]
        }
        )

@nlp_router.post("/index/answer/{project_id}")
async def answer_rag(request: Request, project_id: str, search_request: SearchRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPControllers(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_clinet,
        template_parser=request.app.template_parser,
    )

    answer, full_prompt, chat_history = nlp_controller.answer_user_with_llm(
        project=project,
        query=search_request.text,
        limit=search_request.limit,
    )

    if not answer:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.RAG_ANSWER_ERROR.value
                } 
        )
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.RAG_ANSWER_SUCCESS.value,
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_history": chat_history
        }
    )
    

    
    




