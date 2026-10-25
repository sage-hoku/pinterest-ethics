import current, new

class Patch:
    def __init__(self):
        self.converted = {}
        
    def convert_post(
        self, 
        post: current.Post, 
        content_creator: new.ContentCreator | None = None
    )      -> new.Post | None:
        """
        tries to find a content creator for sponsored posts, 
           otherwise converts directly or deletes.
        """
        if isinstance(post, current.SponsoredPost):
            # delete old external advertisements.
            if content_creator is None:
                return None
            # otherwise, link to content creator.
            else:
                return new.SponsoredPost(list(post.tags), content_creator)
        return new.Post(list(post.tags))
    
    def convert_user(
        self, 
        user: current.User
    )      -> new.User:
        new_user = new.User(list(user.interests))
        new_user.posts = [p for p in (
                          self.convert_post(p) for p in user.posts) if p] 
        return new_user
    
    def convert_creator(
        self,
        creator: current.ContentCreator
    )         -> new.ContentCreator:
        new_creator = new.ContentCreator(list(creator.interests))
        new_creator.posts = [self.convert_post(p, new_creator) for p in creator.posts]
        return new_creator
    
    def convert_stakeholder(
        self,
        s: current.Stakeholder 
    )             -> new.User | None:
        if isinstance(s, current.ContentCreator): # check first, since it inherits from both User and Sponsor
            return self.convert_creator(s)
        if isinstance(s, current.User):
            return self.convert_user(s)
        if isinstance(s, (current.Sponsor, current.Investor)):
            return None  # delete
        raise TypeError(f"Unknown stakeholder: {type(s).__name__}")

    def convert_platform(
        self,
        platform: current.Platform
    )          -> new.Platform:
        users = [u for u in (self.convert_stakeholder(u) for u in platform.users)]
        sponsors = [self.convert_creator(s) for s in platform.sponsors
                    if isinstance(s, current.ContentCreator)]
        posts = [p for p in (self.convert_post(p) for p in platform.posts) if p]
        return new.Platform(users, sponsors, posts)
