from UserProfile import UserProfile
from sqlitedb import save_user_profile
import random

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
            "POLITICS": ["elections", "government policies", "political scandals", "voting rights", "campaign finance", "political corruption", "party politics", "political ideologies", "lobbying", "political activism", "civil rights", "foreign policy"],
            "WELLNESS": ["healthy living tips", "mental health advice", "fitness trends", "nutrition tips", "stress management techniques", "self-care practices", "mindfulness exercises", "yoga poses", "meditation techniques", "sleep hygiene tips", "dietary supplements", "holistic wellness"],
            "ENTERTAINMENT": ["celebrity gossip", "movie reviews", "TV show recommendations", "music news", "entertainment industry updates", "celebrity interviews", "film festivals", "award shows", "pop culture trends", "celebrity fashion", "box office reports", "celebrity scandals"],
            "TRAVEL": ["travel destinations", "travel tips", "budget travel hacks", "solo travel advice", "family vacation ideas", "adventure travel experiences", "cultural immersion", "beach destinations", "city breaks", "road trip suggestions", "ecotourism destinations", "travel photography spots"],
            "STYLE & BEAUTY": ["fashion trends", "beauty tips", "makeup tutorials", "haircare advice", "skincare routines", "fashion industry news", "celebrity fashion", "styling hacks", "cosmetic product reviews", "DIY beauty treatments", "fashion photography", "makeup artist tips"],
            "PARENTING": ["parenting advice", "childcare tips", "positive parenting techniques", "family bonding activities", "teen parenting challenges", "newborn care tips", "parenting books", "parenting blogs", "raising teenagers", "single parenting", "parenting hacks", "helicopter parenting"],
            "HEALTHY LIVING": ["healthy recipes", "exercise routines", "wellness retreats", "clean eating tips", "organic living", "vegan lifestyle advice", "plant-based diets", "natural remedies", "mindful eating", "clean beauty products", "eco-friendly living", "sustainable living tips"],
            "QUEER VOICES": ["LGBTQ+ rights", "queer representation in media", "gay pride events", "transgender issues", "queer literature", "coming out stories", "gender identity", "queer activism", "queer culture", "homophobia", "queer history", "intersectionality"],
            "FOOD & DRINK": ["recipes", "restaurant reviews", "food trends", "cooking techniques", "culinary travel experiences", "food photography", "food festivals", "wine tasting", "mixology recipes", "dessert recipes", "healthy eating habits", "food blogging"],
            "BUSINESS": ["business news", "entrepreneurship advice", "startup success stories", "business strategies", "industry trends", "market analysis", "financial planning", "leadership skills", "workplace productivity tips", "investment opportunities", "business networking events", "global economy updates"],
            "COMEDY": ["stand-up comedy", "comedy movies", "comedy specials", "improv comedy", "satirical news", "comedy podcasts", "funny memes", "humor writing", "comedy festivals", "sketch comedy", "comedy clubs", "parody videos"],
            "SPORTS": ["sports news", "game highlights", "athlete interviews", "sports analysis", "team rankings", "sports betting tips", "fantasy sports leagues", "sports documentaries", "sports equipment reviews", "sports science", "sports medicine", "Olympic Games coverage"],
            "BLACK VOICES": ["racial justice", "Black history", "Black culture", "African American literature", "civil rights movement", "anti-racism activism", "Black-owned businesses", "Black art", "representation in media", "racial equality", "Afrofuturism", "Black identity"],
            "HOME & LIVING": ["home decor ideas", "interior design tips", "home organization hacks", "DIY home improvement", "gardening advice", "sustainable living tips", "houseplant care", "minimalist living", "smart home technology", "homesteading", "home renovation projects", "feng shui principles"],
            "PARENTS": ["parenting advice", "childcare tips", "family bonding activities", "teen parenting challenges", "newborn care tips", "positive discipline techniques", "raising teenagers", "parenting blogs", "parenting humor", "single parenting", "parenting hacks", "parenting support groups"]
        }

        # Get the list of terms for the specified category
        terms = category_terms.get(category, ["random query"])

        # Randomly choose a term from the list
        return random.choice(terms)

    def simulate_search(self, num_queries):
        for _ in range(num_queries):
            category = random.choices(list(self.categories.keys()), weights=self.categories.values())[0]
            query = self.generate_random_query(category)
            self.profile.add_search_query(query)
            self.profile.add_click_history(category)

    def simulate_search_targeted(self, num_queries, preferences):
        for _ in range(num_queries):
            # category = random.choices(preferences, weights=[self.categories[cat] for cat in preferences])[0]
            category = random.choices(preferences)[0]
            query = self.generate_random_query(category)
            self.profile.add_search_query(query)
            self.profile.add_click_history(category)

    def print_profile(self):
        print(f"User Profile for User ID: {self.user_id}")
        print(self.profile)

# # Define the number of users and queries per user
# num_users = 3
# num_queries_per_user = 20

# # Simulate users' search behavior
# simulated_users = []
# for i in range(num_users):
#     user = SimulatedUser(user_id=i+1)
#     user.simulate_search(num_queries_per_user)
#     simulated_users.append(user)

# # Print profiles
# for user in simulated_users:
#     user.print_profile()

# Define targeted user preferences
user1_preferences = ["SPORTS", "HEALTHY LIVING", "ENTERTAINMENT", "TRAVEL"]
user2_preferences = ["POLITICS", "BLACK VOICES", "QUEER VOICES"]

# Create targeted users
user1 = SimulatedUser(user_id="sportive")
user2 = SimulatedUser(user_id="activist")

# Simulate search behavior for targeted users
num_queries_per_user = 75
user1.simulate_search_targeted(num_queries_per_user, user1_preferences)
user2.simulate_search_targeted(num_queries_per_user, user2_preferences)

# Print profiles for targeted users
user1.print_profile()
save_user_profile(user1.profile)
user2.print_profile()
save_user_profile(user2.profile)
