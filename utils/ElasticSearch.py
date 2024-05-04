from elasticsearch import Elasticsearch, exceptions, helpers
import json
import os
from dotenv import load_dotenv

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
HTTP_CA_PATH = "utils/http_ca.crt"

def create_elasticsearch_client():
    return Elasticsearch(
        hosts="https://localhost:9200/",
        basic_auth=["elastic", ELASTIC_PASSWORD], # Authentication credentials
        verify_certs=False, # SSL certificate verification
        ca_certs=HTTP_CA_PATH, # Path to the certificate file
        # timeout=30, # Connection timeout in seconds
    )

def create_index(client, index_name):
    # Configuration for creating an index in Elasticsearch
    index_body = {
        "settings": {
            "number_of_shards": 1, # Sets the number of primary shards
            "number_of_replicas": 0  # Sets the number of replica shards
        },
        "mappings": {
            "properties": {
                "category": {"type": "keyword"},  # Index category as keyword for exact matches
                "headline": {"type": "text"},  # Index headline as text for full-text search
                "authors": {"type": "text"},  # Similarly, index authors as text
                "link": {"type": "keyword"},   # Index link as keyword for exact retrieval
                "short_description": {"type": "text"},  # Index short descriptions as text
                "date": {"type": "date"}  # Index date as a date type for time-based queries
            }
        }
    }
    # Check if the index already exists
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body=index_body)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists and will be used.")

def index_news_articles(client, index_name, file_path):
    # Index articles from a JSON file into Elasticsearch
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            actions = []
            for i, line in enumerate(file):
                article = json.loads(line)
                actions.append({
                    "_index": index_name,
                    "_id": i,
                    "_source": {
                        "category": article['category'],
                        "headline": article['headline'],
                        "authors": article['authors'],
                        "link": article['link'],
                        "short_description": article['short_description'],
                        "date": article['date']
                    }
                })
                # Bulk index every 500 articles or last batch
                if len(actions) >= 500:
                    helpers.bulk(client, actions)
                    actions = []
            # Index any remaining articles
            if actions:
                helpers.bulk(client, actions)
        print(f"Indexed articles.")
    except Exception as e:
        print(f"Failed to read or index file: {e}")
