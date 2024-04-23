from elasticsearch import Elasticsearch
import os
import argparse

def init_client(hosts: str, 
                basic_auth: tuple[str, str]=None, 
                api_key: str=None, 
                verify_certs: bool=False, 
                ca_certs: str=None):
    """
    Initialize an Elasticsearch client. Either basic_auth or api_key must be provided.
    :param hosts: url of the Elasticsearch server
    :param basic_auth: tuple of username and password
    :param api_key: API key
    :param verify_certs: whether to verify certificates
    :param ca_certs: path to the CA certificate

    :return: Elasticsearch client
    """
    return Elasticsearch(
        hosts=hosts,
        basic_auth=basic_auth,
        api_key=api_key,
        verify_certs=verify_certs,
        ca_certs=ca_certs,
    )

def exists_index(client: Elasticsearch,
                 index: str):
    """
    Check if an index exists.
    :param client: Elasticsearch client
    :param index: name of the index

    :return: True if the index exists, False otherwise
    """
    return client.indices.exists(index=index)

def index_documents(client: Elasticsearch, 
                    dname: str, 
                    index: str):
    """
    Index documents in a directory.
    :param client: Elasticsearch client
    :param dname: path to the directory
    :param index: name of the index
    """
    if client.indices.exists(index=index):
        return
    
    for fname in os.listdir(dname):
        with open(os.path.join(dname, fname), "r") as f:
            content = f.read()
            client.index(
                index=index,
                id=fname,
                document={
                    "content": content,
                },
            )

def search(client: Elasticsearch, 
           index: str, 
           query: str, 
           size: int=10):
    """
    Normal search (not personalized).
    :param client: Elasticsearch client
    :param index: name of the index
    :param query: search query
    :param size: number of results to return

    :return: a dictionary with the following format:
    ```
    {
        "took": int,  # Time taken for the query (in milliseconds)
        "timed_out": bool,  # Whether the query timed out
        "_shards": {  # Shard information
            "total": int,  # Total number of shards
            "successful": int,  # Number of successful shards
            "skipped": int,  # Number of skipped shards
            "failed": int,  # Number of failed shards
        },
        "hits": {  # Search results
            "total": {  # Total number of results
            "value": int,
            "relation": str
            },
            "max_score": float,  # Highest _score
            "hits": [  # List of results
            {
                "_index": str,  # Index where the document is located
                "_type": str,  # Type of the document
                "_id": str,  # ID of the document
                "_score": float,  # _score of the document
                "_source": {  # Source data of the document
                # ...
                }
            },
            # ...
            ]
        }
    }
    ```
    """

    queryDSL = {
        "match": {
            "content": {
                "query": query
            }
        }
    }
    return client.search(index=index, query=queryDSL, size=size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Elasticsearch host", default="https://localhost:9200")
    parser.add_argument("-u", "--username", help="Elasticsearch username", default="elastic")
    parser.add_argument("-p", "--password", help="Elasticsearch password", required=True)
    parser.add_argument("-d", "--dname", help="Path to the directory of documents", default="../davisWiki")
    parser.add_argument("-i", "--index", help="Index name", default="davis-wiki")
    parser.add_argument("-q", "--query", help="Search query", default="zombie attack")
    parser.add_argument("-s", "--size", help="Number of results to return", type=int, default=10)
    args = parser.parse_args()

    client = init_client(
        hosts=args.host,
        basic_auth=(args.username, args.password),
        verify_certs=True,
        ca_certs="../http_ca.crt",
    )

    if not exists_index(client, index=args.index):
        print("Indexing documents")
        index_documents(client, dname=args.dname, index=args.index)
        
    out = search(client, index=args.index, query=args.query, size=args.size)

    for hit in out["hits"]["hits"]:
        print(f"Document ID: {hit['_id']}, Score: {hit['_score']}")