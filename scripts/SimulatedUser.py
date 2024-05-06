from utils.UserProfile import UserProfile
from utils.search import build_query
from utils.sqlitedb import save_user_profile
import random
import requests

POSSIBLE_SEARCH_TYPES = ["intersection", "phrase"]

class SimulatedUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.profile = UserProfile(user_id)
        self.categories = {
            "POLITICS": 35602,
            "WELLNESS": 17945,
            "ENTERTAINMENT": 17362,
            "TRAVEL": 9900,
            "STYLE & BEAUTY": 9814,
            "PARENTING": 8791,
            "HEALTHY LIVING": 6694,
            "QUEER VOICES": 6347,
            "FOOD & DRINK": 6340,
            "BUSINESS": 5992,
            "COMEDY": 5400,
            "SPORTS": 5077,
            "BLACK VOICES": 4583,
            "HOME & LIVING": 4320,
            "PARENTS": 3955
        }

    # Function to generate a random query related to a category
    def generate_random_query(self, category):
        # Define a dictionary of categories and their corresponding terms
        category_terms = {
            "POLITICS": ["elections", "government policies", "political scandals", "voting rights", "campaign finance", "political corruption", "party politics", "political ideologies", "lobbying", "political activism", "civil rights", "foreign policy", "democrats", "republicans", "GOP", "congress", "senate", "house of representatives", "presidential candidates"],
            "WELLNESS": ["healthy living tips", "mental health advice", "fitness trends", "nutrition tips", "stress management techniques", "self-care practices", "mindfulness exercises", "yoga poses", "meditation techniques", "sleep hygiene tips", "dietary supplements", "holistic wellness", "yoga", "pilates", "jogging", "running", "mindfulness", "meditation", "nutrition", "diet"],
            "ENTERTAINMENT": ["celebrity gossip", "movie reviews", "TV show recommendations", "music news", "entertainment industry updates", "celebrity interviews", "film festivals", "award shows", "pop culture trends", "celebrity fashion", "box office reports", "celebrity scandals", "box office", "interview", "gossip", "celebrity", "film", "TV", "music"],
            "TRAVEL": ["travel destinations", "travel tips", "budget travel hacks", "solo travel advice", "family vacation ideas", "adventure travel experiences", "cultural immersion", "beach destinations", "city breaks", "road trip suggestions", "ecotourism destinations", "travel photography spots", "sustainable travel", "backpacking", "trip", "Los Angeles", "New York", "Paris", "London"],
            "STYLE & BEAUTY": ["fashion trends", "beauty tips", "makeup tutorials", "haircare advice", "skincare routines", "fashion industry news", "celebrity fashion", "styling hacks", "cosmetic product reviews", "DIY beauty treatments", "fashion photography", "makeup artist tips", "fashion", "acne", "style", "trend"],
            "PARENTING": ["parenting advice", "childcare tips", "positive parenting techniques", "family bonding activities", "teen parenting challenges", "newborn care tips", "parenting books", "parenting blogs", "raising teenagers", "single parenting", "parenting hacks", "helicopter parenting", "mother", "father", "child", "family", "diapers", "baby"],
            "HEALTHY LIVING": ["healthy recipes", "exercise routines", "wellness retreats", "clean eating tips", "organic living", "vegan lifestyle advice", "plant-based diets", "natural remedies", "mindful eating", "clean beauty products", "eco-friendly living", "sustainable living tips", "organic food", "vegan", "yoga", "exercise", "diet", "nutrition"],
            "QUEER VOICES": ["LGBTQ+ rights", "queer representation in media", "gay pride events", "transgender issues", "queer literature", "coming out stories", "gender identity", "queer activism", "queer culture", "homophobia", "queer history", "intersectionality", "LGBTQ", "queer", "protest", "pride", "rights", "news"],
            "FOOD & DRINK": ["recipes", "restaurant reviews", "food trends", "cooking techniques", "culinary travel experiences", "food photography", "food festivals", "wine tasting", "mixology recipes", "dessert recipes", "healthy eating habits", "food blogging", "recipe", "restaurant", "food", "drink", "cooking"],
            "BUSINESS": ["business news", "entrepreneurship advice", "startup success stories", "business strategies", "industry trends", "market analysis", "financial planning", "leadership skills", "workplace productivity tips", "investment opportunities", "business networking events", "global economy updates", "business", "entrepreneur", "startup", "investment", "finance"],
            "COMEDY": ["stand-up comedy", "comedy movies", "comedy specials", "improv comedy", "satirical news", "comedy podcasts", "funny memes", "humor writing", "comedy festivals", "sketch comedy", "comedy clubs", "parody videos", "comedian", "jokes", "funny", "humor", "Comedy Central", "SNL", "stand-up", "Chapelle", "Seinfeld", "C.K."],
            "SPORTS": ["sports news", "game highlights", "athlete interviews", "sports analysis", "team rankings", "sports betting tips", "fantasy sports leagues", "sports documentaries", "sports equipment reviews", "sports science", "sports medicine", "Olympic Games coverage", "football", "basketball", "soccer", "baseball", "tennis", "golf", "NBA", "NFL", "news", "media", "sports media"],
            "BLACK VOICES": ["racial justice", "Black history", "Black culture", "African American literature", "civil rights movement", "anti-racism activism", "Black-owned businesses", "Black art", "representation in media", "racial equality", "Afrofuturism", "Black identity", "Black Lives Matter", "racism", "Black", "African American", "history", "culture", "news"],
            "HOME & LIVING": ["home decor ideas", "interior design tips", "home organization hacks", "DIY home improvement", "gardening advice", "sustainable living tips", "houseplant care", "minimalist living", "smart home technology", "homesteading", "home renovation projects", "feng shui principles", "home", "decor", "design", "DIY", "garden", "sustainable"],
            "PARENTS": ["parenting advice", "childcare tips", "family bonding activities", "teen parenting challenges", "newborn care tips", "positive discipline techniques", "raising teenagers", "parenting blogs", "parenting humor", "single parenting", "parenting hacks", "parenting support groups", "mother", "father", "child", "family", "parenting"]
        }

        # Get the list of terms for the specified category
        terms = category_terms.get(category, ["random query"])

        # Randomly choose a term from the list
        return random.choice(terms)

    def simulate_search(self, client, index_name, num_queries):
        for _ in range(num_queries):
            category = random.choices(list(self.categories.keys()), weights=self.categories.values())[0]
            query = self.generate_random_query(category)
            self.make_query(client, index_name, query)

    def simulate_search_targeted(self, client, index_name, num_queries, preferences):
        for _ in range(num_queries):
            category = random.choices(preferences)[0]
            query = self.generate_random_query(category)
            self.make_query(client, index_name, query)
    
    # We also need to actually make the query and randomly click on some articles, in order to simulate user behavior
    def make_query(self, client, index_name, query):
        modified_query = build_query(random.choice(POSSIBLE_SEARCH_TYPES), query)
        # modified_query = self.profile.personalize_search(modified_query)
        self.profile.add_search_query(query)
        try:
            response = client.search(index=index_name, body=modified_query)
            entries = response['hits']['hits']
        except requests.RequestException as e:
            print(e)
        
        # Simulate clicking on some articles
        if entries:
            num_clicks = random.randint(1, min(5, len(entries)))
            for _ in range(num_clicks):
                entry = random.choice(entries)
                clicked_category = entry['_source']['category']
                clicked_headline = entry['_source']['headline']
                clicked_description = entry['_source']['short_description']
                self.profile.add_click_history(clicked_category, clicked_headline, clicked_description)

    def print_profile(self):
        print(f"User Profile for User ID: {self.user_id}")
        print(self.profile)
