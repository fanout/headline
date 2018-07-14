from django.db import models

class Headline(models.Model):
    type = models.CharField(max_length=64)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def to_data(self):
        out = {}
        out['id'] = str(self.id)
        out['type'] = self.type
        if self.title:
            out['title'] = self.title
        out['date'] = self.date.isoformat()
        out['text'] = self.text
        return out

    def __str__(self):
        return '%s: %s' % (self.type, self.text[:100])
