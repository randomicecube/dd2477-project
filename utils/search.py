def build_query(query_type, term):
    # Build a query based on search type and term
    if query_type == "intersection":
        # Construct query for intersection search
        query = construct_intersection_query(term)
    elif query_type == "phrase":
        # Construct query for phrase search
        query = construct_phrase_query(term)
    return query


def construct_intersection_query(terms):
    # Constructing the list of must clauses for intersection search
    must_clauses = [{"multi_match": {"query": term, "fields": ["headline", "short_description"]}} for term in terms.split()]

    # Constructing the query object
    query = {
        "query": {
            "bool": {
                "must": must_clauses,
                "should": []  # Empty list for should clause
            }
        }
    }
    return query


def construct_phrase_query(terms):
    # Construct query for phrase search
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"headline": terms}},
                    {"match_phrase": {"short_description": terms}}
                ],
                "should": []  # Empty list for should clause
            }
        }
    }
    return query

# TODO: add search_ranked?
