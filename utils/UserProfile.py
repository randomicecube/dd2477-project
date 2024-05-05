class UserProfile:
    # Initialization method for the UserProfile class
    def __init__(self, user_id):
        self.user_id = user_id  # Unique identifier for the user
        self.search_history = []  # List to store past search queries made by the user
        self.click_history = []  # List to store the categories of items clicked by the user
        self.category_preferences = {}  # Dictionary to store preferences for categories based on user interactions
        self.term_preferences = {}  # Dictionary to store frequency of search terms used by the user

    # Method to add a search query to the user's search history and update term preferences
    def add_search_query(self, query):
        # Append the query to the search history list
        self.search_history.append(query)
        # Split the query into individual terms
        terms = query.split()
        # Update the term preferences dictionary with the count of each term
        for term in terms:
            if term in self.term_preferences:
                self.term_preferences[term] += 1  # Increment count of the term if it already exists
            else:
                self.term_preferences[term] = 1  # Set count of the term to 1 if it's a new term

    # Method to add a category to the click history and update category preferences
    def add_click_history(self, category):
        # Append the category to the click history list
        self.click_history.append(category)
        # Update the category preferences dictionary with the count of each category
        if category in self.category_preferences:
            self.category_preferences[category] += 1  # Increment count of the category if it already exists
        else:
            self.category_preferences[category] = 1  # Set count of the category to 1 if it's a new category

    # Method to personalize a search query based on the user's preferences
    def personalize_search(self, query):
        # Boost categories in the search query based on the user's category preferences
        if self.category_preferences:
            # Get top 3 categories based on preference count
            top_categories = sorted(self.category_preferences, key=self.category_preferences.get, reverse=True)[:3]
            # Create boost clauses for these categories
            # TODO: check if 2 is a good boost value
            category_should_clauses = [{"match": {"category": {"query": cat, "boost": 2}}} for cat in top_categories]
            # Add these clauses to the search query
            query['query']['bool']['should'] += category_should_clauses
        
        # Boost terms in the search query based on the user's term preferences
        if self.term_preferences:
            # Get top 5 terms based on frequency of use
            # TODO: check if this is a good strategy for boosting terms
            top_terms = sorted(self.term_preferences, key=self.term_preferences.get, reverse=True)[:5]
            # Create boost clauses for these terms
            # TODO: check if 1.5 is a good boost value
            term_should_clauses = [{"match": {"headline": {"query": term, "boost": 1.5}}} for term in top_terms]
            # Add these clauses to the search query
            query['query']['bool']['should'] += term_should_clauses

        # Return the modified query
        return query

    # String representation method for the UserProfile class
    def __str__(self):
        # Return a formatted string that lists all the user's data
        return f'User ID: {self.user_id}\nSearch History: {self.search_history}\nClick History: {self.click_history}\nCategory Preferences: {self.category_preferences}\nTerm Preferences: {self.term_preferences}'
