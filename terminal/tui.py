from utils.ElasticSearch import create_elasticsearch_client, create_index, index_news_articles
from utils.search import build_query
from utils.sqlitedb import save_user_profile, load_user_profile
from tabulate import tabulate

DATA_FILE = "data/News_Category_Dataset_v3.json"

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

    keep_displaying = True
    while keep_displaying:
        try:
            choice = int(input("\nEnter the number of the article to view details or -1 to exit: "))
            if choice == -1:
                keep_displaying = not keep_displaying
                continue
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

    if input("Do you want to index news articles? (yes/no): ") == "yes":
        index_news_articles(client, index_name, DATA_FILE)

    # Create a user profile
    user_id = input("Enter your user ID: ")
    user_profile = load_user_profile(user_id)
    print(user_profile)

    keep_searching = True
    while keep_searching:
        query_type = input("Enter search type (intersection/phrase): ")
        if query_type not in ['intersection', 'phrase']:
            print("Invalid search type! Please input one of 'intersection', or 'phrase'.")
            continue

        term = input("Enter term(s) to search: ")
        query = build_query(query_type, term)

        # Log the search query
        user_profile.add_search_query(term)

        # Personalize the query based on user profile
        query = user_profile.personalize_search(query)

        print("[INFO]: Sent query to Elasticsearch: ", query)

        # Perform the search
        response = client.search(index=index_name, body=query, size=20)
        print_search_results(response)
        view_full_article(response)
        # Log clicked results if any
        if input("Log clicked result? (yes/no): ") == "yes":
            clicked_category = input("Enter the category of clicked result: ")
            user_profile.add_click_history(clicked_category)

        save_user_profile(user_profile)

        if input("Continue searching? (yes/no): ") != 'yes':
            keep_searching = not keep_searching

if __name__ == "__main__":
    main()