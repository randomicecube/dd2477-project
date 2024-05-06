QUERY_TEMPLATE = {
    "query": {
        "bool": {
            "must": [],
            "should": []
        }
    }
}

def build_query(query_type, term):
    match query_type:
        case "intersection":
            return search_intersection(term)
        case "phrase":
            return search_phrase(term)

def search_intersection(terms):
    # Search for an intersection of multiple terms within an index
    query = {
        "query": {
            "bool": {
                "must": [],
                "should": []
            }
        }
    }
    should_clauses = [
        {
            "bool": {
                "should": [
                    {"match": {"headline": term}},
                    {"match": {"short_description": term}}
                ],
                "minimum_should_match": 1
            }
        }
        for term in terms.split()
    ]
    query['query']['bool']['must'] = should_clauses
    return query

def search_phrase(phrase):
    # Search for an exact phrase within an index
    query = {
        "query": {
            "bool": {
                "must": [],
                "should": []
            }
        }
    }
    query['query']['bool']['must'] = [
        {
            "bool": {
                "should": [
                    {"match_phrase": {"headline": phrase}},
                    {"match_phrase": {"short_description": phrase}}
                ],
                "minimum_should_match": 1
            }
        }
    ]
    return query
