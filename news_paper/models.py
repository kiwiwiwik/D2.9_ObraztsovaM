from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

#
# суммарный рейтинг каждой статьи автора умножается на 3;
# суммарный рейтинг всех комментариев автора;
# суммарный рейтинг всех комментариев к статьям автора.


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_posts = self.post_set.aggregate(ratingPost=Sum('rating'))
        rating_post = 0
        rating_post += rating_posts.get('ratingPost')

        rating_comments = self.authorUser.comment_set.aggregate(ratingComment=Sum('rating'))
        rating_comment = 0
        rating_comment += rating_comments.get('ratingComment')

        rating_post_com = 0
        for author_post in self.post_set.all():
            rating_post_coms = author_post.comment_set.aggregate(ratingPostCom=Sum('rating'))
            rating_post_com += rating_post_coms.get('ratingPostCom')

        self.rating = rating_post * 3 + rating_comment + rating_post_com
        self.save()


class Category(models.Model):
    economics = 'EC'
    politics = 'PO'
    culture = 'CU'
    style = 'ST'
    social = 'SO'
    sport = 'SP'

    CATEGORIES = [
        (economics, 'Экономика'),
        (politics, 'Политика'),
        (culture, 'Культура'),
        (style, 'Стиль'),
        (social, 'Общество'),
        (sport, 'Спорт')
    ]

    category = models.CharField(max_length = 2,
                            choices = CATEGORIES,
                            default = social)


class Post(models.Model):
    news = 'NE'
    article = 'AR'

    TYPES = [(news, 'Новость'), (article, 'Статья')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length = 2,
                            choices = TYPES,
                            default = news)
    time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commented_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
