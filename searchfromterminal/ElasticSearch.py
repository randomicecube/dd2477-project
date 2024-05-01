import json
from tabulate import tabulate
from elasticsearch import Elasticsearch, exceptions, helpers
from UserProfile import UserProfile
from sqlitedb import save_user_profile, load_user_profile

def create_elasticsearch_client():
    # Establish a connection to Elasticsearch with specified settings
    return Elasticsearch(
        hosts="https://localhost:9200/",
        basic_auth=["elastic", "X4DppLED2J+osbPYRcHu"], # Authentication credentials
        verify_certs=True, # SSL certificate verification
        ca_certs="http_ca.crt" # Path to the certificate file
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


def search_single_term(client, index, term):
    # Search for a single term within an index
    query = {
        "query": {
            "match": {
                "content": term
            }
        }
    }
    return client.search(index=index, body=query)

def search_intersection(client, index, terms):
    # Search for an intersection of multiple terms within an index
    must_clauses = [{"match": {"content": term}} for term in terms]
    query = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }
    return client.search(index=index, body=query)

def search_phrase(client, index, phrase):
    # Search for an exact phrase within an index
    query = {
        "query": {
            "match_phrase": {
                "content": phrase
            }
        }
    }
    return client.search(index=index, body=query)

def print_search_results(response):
    # Display search results in a tabulated format
    results = []
    for index, hit in enumerate(response['hits']['hits']):
        headline = hit["_source"]["headline"]
        short_description = hit["_source"]["short_description"]
        # Add the index at the beginning of each row
        results.append([index, headline, short_description[:50] + "..."])
    print(tabulate(results, headers=["#", "Headline", "Short Description"], tablefmt="grid"))

def view_full_article(response):
    # Allow the user to view full article details from search results
    articles = [hit["_source"] for hit in response['hits']['hits']]
    
    if not articles:
        print("No articles to display.")
        return

    while True:
        try:
            choice = int(input("\nEnter the number of the article to view details or -1 to exit: "))
            if choice == -1:
                break
            article = articles[choice]
            print("\nFull Article Details:")
            print("Headline:", article['headline'])
            print("Authors:", article['authors'])
            print("Link:", article['link'])
            print("Category:", article['category'])
            print("Date:", article['date'])
            print("Description:", article['short_description'])
        except (IndexError, ValueError):
            print("Invalid input, please try again.")


def main():
    # Main function to handle the workflow
    client = create_elasticsearch_client()
    index_name = "news_articles"
    
    # Create index if not exists
    create_index(client, index_name)

    # File path to the JSON dataset
    file_path = "/Users/ossamaziri/Desktop/project/News_Category_Dataset_v3.json"
    if input("Do you want to index news articles? (yes/no): ") == "yes":
        index_news_articles(client, index_name, file_path)

    # Create a user profile
    user_id = input("Enter your user ID: ")
    user_profile = load_user_profile(user_id)
    print(user_profile)

    while True:
        search_type = input("Enter search type (single/intersection/phrase): ")
        if search_type not in ['single', 'intersection', 'phrase']:
            print("Invalid search type!")
            continue

        term = input("Enter term(s) to search: ")
        query = {
            "query": {
                "bool": {
                    "must": [],
                    "should": []
                }
            }
        }

        # Log the search query
        user_profile.add_search_query(term)

        if search_type == "single":
            query['query']['bool']['must'].append({"match": {"headline": term}})
        elif search_type == "intersection":
            terms = term.split(",")
            for t in terms:
                query['query']['bool']['must'].append({"match": {"headline": t.strip()}})
        elif search_type == "phrase":
            query['query'] = {"match_phrase": {"headline": term}}

        # Personalize the query based on user profile
        query = user_profile.personalize_search(query)

        # Perform the search
        response = client.search(index=index_name, body=query)
        print_search_results(response)
        view_full_article(response)
        # Log clicked results if any
        if input("Log clicked result? (yes/no): ") == "yes":
            clicked_category = input("Enter the category of clicked result: ")
            user_profile.add_click_history(clicked_category)

        save_user_profile(user_profile)

        if input("Continue searching? (yes/no): ") != 'yes':
            break

if __name__ == "__main__":
    main()