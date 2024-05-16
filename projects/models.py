from django.db import models
import uuid

from users.models import Profile


class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True,
        blank=True,
        default="/projects/project-default.png",
        upload_to="images/projects/",
    )
    votes = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True, related_name="projects")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        This method returns the title of the project
        """
        return self.title

    class Meta:
        ordering = ["-votes", "-vote_ratio", "title"]

    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(vote_type="up").count()
        total_votes = reviews.count()
        ratio = (up_votes / total_votes) * 100

        self.votes = total_votes
        self.vote_ratio = ratio
        self.save()

    @property
    def review(self):
        queryset = self.review_set.all().values_list("owner__id", flat=True)
        return queryset


class Review(models.Model):
    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote"),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    vote_type = models.CharField(max_length=50, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["owner", "project"]]

    def __str__(self):
        """
        This method returns the vote type of the review
        """
        return self.vote_type


class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
