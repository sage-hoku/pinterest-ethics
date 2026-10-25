import math
import random

# Posts
class Post():
    def __init__(self, tags: list[str]):
        self.tags = tags
    
class SponsoredPost(Post):
    """Advertisements"""
    def __init__(self, tags: list[str], sponsor: "Sponsor"):
        super().__init__(tags)
        self.sponsor = sponsor

# People
class Stakeholder:
    def __init__(self, stake: float): # percentage of ownership):
        self.stake = stake
        
class Investor(Stakeholder):
    def __init__(self, stake: float):
        super(Investor, self).__init__(stake)
        
class Sponsor(Stakeholder):
    def __init__(self, stake: float):
        super(Sponsor, self).__init__(stake)
        self.posts = []
        
    def get_advertisement(self) -> Post:
        return random.choice(self.posts)
    
class User(Stakeholder):
    def __init__(self, interests: list[str]):
        super(User, self).__init__(0.0)
        self.interests = interests
        self.posts = []
        
    def browse(self, interest: str):
        if interest not in self.interests:
            # Implementation for browsing content related to the interest
            self.interests += [interest]

class ContentCreator(User, Sponsor):
    def __init__(self, niches: list[str], stake: float):
        super(ContentCreator, self).__init__(niches)
        super(Sponsor, self).__init__(stake)
   

# Main Platform
class Platform:
    def __init__(self,
        users:    list[User],
        sponsors: list[Sponsor],
        posts:    list[Post],
    ):
        self.posts = posts
        self.sponsors = sponsors
        self.users = users
        self.SPONSORED_CONTENT_RATIO = 0.2 # 20% of content is ads

    def show_post(self, interest: str, posts: list[Post] | None = None) -> Post:
        """Show a post matching a specific interest"""
        if posts is None:
            posts = self.posts
        filtered_posts = [p for p in posts if interest in p.tags]
        return random.choice(filtered_posts)
    
    def show_sponsored_post(self) -> Post:
        """Return a sponsor chosen with probability equal to its stake."""
        sponsors = self.sponsors
        weights = [sponsor.stake for sponsor in self.sponsors]
        return random.choices(sponsors, weights=weights, k=1)[0].get_advertisement()

    def shuffle_content(self, posts: list[Post]):
        random.shuffle(posts)
        return
    
    def generate_user_recommendations(self, n: int, user: User): # n recommendations based on User user.
        user_recs = []
        num_ads = math.ceil(n * self.SPONSORED_CONTENT_RATIO)
        for i in range(num_ads):
            user_recs.append(self.show_sponsored_post())

        for i in range(n - num_ads):
            user_recs.append(
                self.show_post(
                    random.choice(user.interests)
                    ))
        self.shuffle_content(user_recs)
        return user_recs
