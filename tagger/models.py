from django.db import models

from user.models import User


class Sentence(models.Model):
    text = models.TextField(max_length=4096, null=False)
    # TODO refactor
    polarityAvg = models.FloatField(default=0, null=False)

    def __str__(self):
        return str(self.text) + '\t' + str(self.polarityAvg)


class SentenceHistory(models.Model):
    sentenceId = models.ForeignKey(Sentence, null=False, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    polarity = models.IntegerField(null=False)
    ip = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        sentenceText = self.sentenceId.text
        return str(sentenceText) + '\t' + str(self.userId) + '\t' + str(self.polarity) + '\t' + str(self.ip)
