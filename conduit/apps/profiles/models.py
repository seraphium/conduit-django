from django.db import models
from conduit.apps.core.models import TimestampModel


class Profile(TimestampModel):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

    follows = models.ManyToManyField('self',
                                     related_name='followed_by',
                                     symmetrical=False)

    favorites = models.ManyToManyField('articles.Article',
                                       related_name='favorited_by')

    def follow(self, profile):
        self.follows.add(profile)

    def unfollow(self, profile):
        self.follows.remove(profile)

    def is_following(self, profile):
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        return self.followed_by.filter(pk=profile.pk).exists()

    def favorite(self, article):
        self.favorites.add(article)

    def unfavorite(self, article):
        self.favorites.remove(article)

    def has_favorited(self, article):
        return self.favorites.filter(pk=article.pk).exists()

