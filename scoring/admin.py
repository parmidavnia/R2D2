from django.contrib import admin
from scoring.models import *

# Register your models here.
admin.site.register(ScoringDataset)
admin.site.register(ScoringSentence)
admin.site.register(ScoringSentenceHistory)