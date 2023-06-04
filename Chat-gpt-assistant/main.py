import logging
import argparse
from ingestion import ingest_doc
from backend import core
from backend.hugging_face_embeddings import LocalHuggingFaceEmbeddings as Embeddings 

def main(args):

    embedd_model = args.model
    embeddings = Embeddings(embedd_model)
    raw_documents = ingest_doc(path=args.path,embeddings=embeddings,out_path =args.vector_path,chunk_size=args.chunk_size,info_overlap=args.overlap)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LLM documentation query based application')
    parser.add_argument('-q','--query',type=str,default=None , required=True,help='Query to be asked')
    parser.add_argument('-p','--path',type=str,default=None,required=True,help='documentation path')
    parser.add_argument('-v','--vector_path',type=str,default='vector_database',help='Path to store vectors',required=False)
    parser.add_argument('-c','--chunk_size',type=int,default=500,help="chunk size",required=False)
    parser.add_argument('--overlap',type=int,default=50,help='information overlap')
    parser.add_argument('---verbose',type=bool,default=False,help='debug default False')
    parser.add_argument('--model',type=str,default='multi-qa-mpnet-base-dot-v1',help='embedding model')
    args = parser.parse_args()
    main(args)
