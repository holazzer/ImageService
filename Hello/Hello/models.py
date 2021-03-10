from django.db import models


class P(models.Model):
    ip_string = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    b = models.BinaryField()


class ImagePAccessEvent(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    ip_string = models.TextField()
    p = models.ForeignKey(P, on_delete=models.CASCADE)


class ImageRequestEvent(models.Model):
    path = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    ip_string = models.TextField()

    def __str__(self):
        return "<ImageRequestEvent: {},{}>".format(self.ip_string, self.path)


