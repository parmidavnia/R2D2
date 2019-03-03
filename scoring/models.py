from django.db import models

from user.models import User


class ScoringDataset(models.Model):
    name = models.CharField(null=False, max_length=128)

    def __str__(self):
        return str(self.name)


class ScoringSentence(models.Model):
    dataset = models.ForeignKey(ScoringDataset, null=False, on_delete=models.CASCADE)
    number = models.IntegerField(null=False)  # ID field in the dataset
    text = models.TextField(max_length=4096, null=False)
    mr = models.TextField(max_length=4096, null=False)
    informativeness_avg = models.FloatField(default=0, null=False)
    naturalness_avg = models.FloatField(default=0, null=False)
    quality_avg = models.FloatField(default=0, null=False)

    def __str__(self):
        return str(self.text) + '\t' + str(self.mr) + '\t' + str(self.informativeness_avg) + '\t' +\
               str(self.naturalness_avg) + '\t' + str(self.quality_avg)


class ScoringSentenceHistory(models.Model):
    sentenceId = models.ForeignKey(ScoringSentence, null=False, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    informativeness = models.IntegerField(null=False)
    naturalness = models.IntegerField(null=False)
    quality = models.IntegerField(null=False)
    ip = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sentenceId.text) + '\t' + str(self.userId) + '\t' + str(self.informativeness) + '\t' + \
               str(self.naturalness) + '\t' + str(self.quality) + '\t' + str(self.ip)

