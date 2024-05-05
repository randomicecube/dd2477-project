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

# TODO: see if it makes sense to boost headline more than the content
# TODO: check if it makes sense for any of them to be a should, instead of a must

def search_intersection(terms):
    # Search for an intersection of multiple terms within an index
    query = QUERY_TEMPLATE
    must_clauses = [{"multi_match": {"query": term, "fields": ["headline", "short_description"]}} for term in terms.split()]
    query['query']['bool']['must'] = must_clauses
    return query

def search_phrase(phrase):
    # Search for an exact phrase within an index
    query = QUERY_TEMPLATE
    query['query']['bool']['must'].append({"match_phrase": {"headline": phrase}})
    query['query']['bool']['must'].append({"match_phrase": {"short_description": phrase}})
    return query
