import math
import random

# Posts
class Post():
    def __init__(self, tags: list[str]):
        self.tags = tags
    
class SponsoredPost(Post):
    """Advertisements"""
    def __init__(self, tags: list[str], sponsor: "ContentCreator"):
        super().__init__(tags)
        self.sponsor = sponsor

class User():
    def __init__(self, interests: list[str]):
        self.interests = interests
        self.posts = []
        
    def browse(self, interest: str):
        if interest not in self.interests:
            # Implementation for browsing content related to the interest
            self.interests += [interest]

class ContentCreator(User):
    def __init__(self, niches: list[str]):
        super(ContentCreator, self).__init__(niches)

    def get_advertisement(self):
        return random.choice(self.posts)


# Main Platform
class Platform:
    def __init__(self,
        users:    list[User],
        sponsors: list[ContentCreator],
        posts:    list[Post]
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
        """Return a sponsored post."""
        sponsors = self.sponsors
        return random.choice(sponsors).get_advertisement()

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
