from datetime import datetime

from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    url = models.CharField(max_length=255, null=True)
    logo = models.CharField(max_length=255, null=True)

    def options(self):
        return sorted(self.option_set.filter(hidden=False), key=lambda r: r.name.lower())

class Meal(models.Model):
    closing_at = models.DateTimeField(null=False)
    place = models.ForeignKey(Place, null=False)

    @classmethod
    def current(cls):
        try:
            return cls.objects.get(closing_at__gt=datetime.now())
        except Meal.DoesNotExist:
            return None

    @classmethod
    def most_recent(cls):
        try:
            return cls.objects.all().order_by("-closing_at")[0]
        except IndexError:
            return None

    def is_open(self):
        return self.closing_at > datetime.now()

    def grouped_choices(self):
        items = {}
        for choice in self.choice_set.all().order_by("who"):
            if items.get(choice.option.name) is None:
                items[choice.option.name] = { 'choices': [ choice ] }
            else:
                items[choice.option.name]['choices'].append(choice)
        for k, v in items.items():
            v['count'] = len([ c for c in v['choices'] if not c.deleted ])
        return sorted(items.iteritems(), key=lambda r: (r[1]["count"] == 0, r[0].lower()))

class Option(models.Model):
    place = models.ForeignKey(Place, null=False)
    name = models.CharField(max_length=255, null=False)
    hidden = models.BooleanField()
    class Meta:
        unique_together = ("place", "name")

class Choice(models.Model):
    who = models.CharField(max_length=255, null=False)
    meal = models.ForeignKey(Meal, null=False)
    option = models.ForeignKey(Option, null=False)
    customisation = models.CharField(max_length=255, null=True)
    deleted = models.BooleanField()
