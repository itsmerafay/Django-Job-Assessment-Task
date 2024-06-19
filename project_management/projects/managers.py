from django.db import models

class ProjectQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)