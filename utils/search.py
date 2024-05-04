def build_query(query_type, term):
    # Build a query based on search type and term
    query = {
        "query": {
            "bool": {
                "must": [],
                "should": [] # TODO: check if this ends up being used
            }
        }
    }

    # TODO: change single to ranked (?)
    if query_type == "single":
        query['query']['bool']['must'].append({"match": {"content": term}})
    elif query_type == "intersection":
        terms = term.split(" ")
        for t in terms:
            query['query']['bool']['must'].append({"match": {"content": t}})
    elif query_type == "phrase":
        query['query'] = {"match_phrase": {"content": term}}

    return query

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

# TODO: add search_ranked?
