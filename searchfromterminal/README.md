## Dependencies

Install the necessary Python libraries using pip:

```bash
pip install elasticsearch tabulate
```

## Configuration

- **Elasticsearch Client**: Configure the client in the `create_elasticsearch_client()` function with appropriate credentials and SSL settings.
- **JSON Dataset**: Provide the file path to your JSON dataset containing news articles in the `main()` function of `ElasticSearch.py`. I choose this database because it is more organized and therefore easy to manipulate: [News Category Dataset on Kaggle](https://www.kaggle.com/datasets/rmisra/news-category-dataset).


## Database Management

To create or recreate the SQLite database, run the `sqlitedb.py` script:

```bash
python sqlitedb.py
```
Choose option '1' to create the database for the first time, or option '2' to delete and to recreate it. 


## Running the Application

Execute the script from the command line:

```bash
python ElasticSearch.py
```
