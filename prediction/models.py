from django.db import models


class PredictionHistory(models.Model):

    job_title = models.CharField(max_length=200)

    company_profile = models.TextField(blank=True)

    job_description = models.TextField(blank=True)

    requirements = models.TextField(blank=True)

    benefits = models.TextField(blank=True)

    result = models.CharField(max_length=50)

    confidence = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title
