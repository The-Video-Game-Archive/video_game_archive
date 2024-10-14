from django.db import models
from django.core.exceptions import ValidationError


class Game(models.Model):
    name = models.CharField(verbose_name="Game Name", max_length=300)
    platform = models.ForeignKey(
        "Platform", on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    release_date = models.DateField(verbose_name="Release Date", blank=True, null=True)
    url = models.CharField(verbose_name="IGDB Link", max_length=400, blank=True, null=True)
    igdb_id = models.IntegerField(verbose_name="IGDB ID", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    test_boolean = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'platform', 'igdb_id')
        ordering = ["name"]
        verbose_name = "Game"
        verbose_name_plural = "Games"


class GameVersion(models.Model):
    class PlayedStatusChoices(models.IntegerChoices):
        unplayed = '0', 'Unplayed'
        played = '1', 'Played'
        completed = '2', 'Completed'
    
    game = models.ForeignKey(
        "Game",
        on_delete=models.PROTECT,
    )
    version = models.CharField(verbose_name="Version", max_length=300)
    release_date = models.DateField(verbose_name="Release Date", blank=True, null=True)
    is_archived = models.BooleanField(verbose_name="Archived", default=False)
    played_status = models.IntegerField(choices=PlayedStatusChoices.choices, default=PlayedStatusChoices.unplayed)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.game} ({self.game.platform}) ({self.version})"

    class Meta:
        ordering = ["game"]
        verbose_name = "Game Version"
        verbose_name_plural = "Game Versions"


class Platform(models.Model):
    name = models.CharField(verbose_name="Platform Name", max_length=300)
    release_date = models.DateField(verbose_name="Release Date", blank=True, null=True)
    url = models.CharField(verbose_name="IGDB Link", max_length=400, blank=True, null=True)
    generation = models.IntegerField(verbose_name = "Generation", blank=True, null=True)
    igdb_id = models.IntegerField(verbose_name="IGDB ID", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Platform"
        verbose_name_plural = "Platforms"


class PlatformVersion(models.Model):
    platform = models.ForeignKey("Platform", on_delete=models.PROTECT)
    version = models.CharField(verbose_name="Version", max_length=300)
    is_archived = models.BooleanField(verbose_name="Archived", default=False)
    release_date = models.DateField(verbose_name="Release Date", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.platform.name} ({self.version})"

    class Meta:
        ordering = ["platform"]
        verbose_name = "Platform Version"
        verbose_name_plural = "Platform Versions"

class GameEngine(models.Model):
    name = models.CharField(verbose_name="Game Engine Name", max_length=300)
    url = models.CharField(verbose_name="IGDB Link", max_length=400, blank=True, null=True)
    igdb_id = models.IntegerField(verbose_name="IGDB ID", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Game Engine"
        verbose_name_plural = "Game Engines"
