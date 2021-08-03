from app.repository.base import RepositoryBase
from app.models.tweet import Tweet


class RepositoryTweet(RepositoryBase[Tweet]):
    pass


tweet = RepositoryTweet(Tweet)
