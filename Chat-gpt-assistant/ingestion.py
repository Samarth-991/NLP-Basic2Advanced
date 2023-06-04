import os 
from dotenv import load_dotenv
from tqdm import tqdm 
from  langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import  RecursiveCharacterTextSplitter , SpacyTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


import logging as log

load_dotenv()
# pinecone.init(api_key = os.environ.get('PINECONE_API_KEY'),environment=os.environ.get('PINECONE_ENVIRONMENT_REGION'))

def ingest_doc(path,embeddings=None,out_path=None,chunk_size=1000,info_overlap=100)->None:
    loader = ReadTheDocsLoader(path)
    raw_documents = loader.load()
    log.info("Number of documents available:{}".format(len(raw_documents)))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=info_overlap,length_function=len)
    documents = text_splitter.split_documents(documents=raw_documents)
    log.info("Number of documents acquired after txt split {}".format(len(documents)))
    log.info("Updating metadata .. ")
    for doc in tqdm(documents):
        new_url = doc.metadata['source'].replace(os.path.dirname(raw_documents[0].metadata['source']),'https://')
        doc.metadata.update({"source":new_url})

    # Pinecone.from_documents(documents=documents,embedding=embeddings,index_name='langchain-doc-index')
    vectorstore =  FAISS.from_documents(documents=documents,embedding = embeddings) # turn dcos into Vectors and store them in RAM
    log.warn("Saving the vector database locally")
    vectorstore.save_local(out_path)
    return documents

