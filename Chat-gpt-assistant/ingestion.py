import os 
from dotenv import load_dotenv
from tqdm import tqdm 
from  langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import  RecursiveCharacterTextSplitter , SpacyTextSplitter
from langchain.vectorstores import FAISS

import logging

load_dotenv()
# pinecone.init(api_key = os.environ.get('PINECONE_API_KEY'),environment=os.environ.get('PINECONE_ENVIRONMENT_REGION'))

import logging

def create_logger():
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:- %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger("APT_Realignment")
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)
    logger.propagate = False
    return logger




def ingest_doc(path,embeddings=None,out_path=None,chunk_size=1000,info_overlap=100)->None:
    log = create_logger()
    
    loader = ReadTheDocsLoader(path)
    raw_documents = loader.load()
    log.info("Number of documents available:{}".format(len(raw_documents)))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=info_overlap,length_function=len)
    documents = text_splitter.split_documents(documents=raw_documents)
    log.info("Number of documents acquired after txt split {}".format(len(documents)))
    log.info("Updating metadata .. ")
    for doc in tqdm(documents):
        new_url = doc.metadata['source'].replace(path,'https://python.langchain.com/en/latest/')
        doc.metadata.update({"source":new_url})
    log.info("Metadata updated ")
    
    # Pinecone.from_documents(documents=documents,embedding=embeddings,index_name='langchain-doc-index')
    vectorstore =  FAISS.from_documents(documents=documents,embedding = embeddings) # turn dcos into Vectors and store them in RAM
    
    vectorstore.save_local(out_path)
    log.warn("Vector database stored locally at ",out_path)
    return documents

