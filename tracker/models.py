from django.db import models
from django.core.exceptions import ValidationError


class Game(models.Model):
    name = models.CharField(verbose_name="Game Name", max_length=300)
    platform = models.ForeignKey(
        "Platform", on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    release_date = models.DateField(verbose_name="Release Date", blank=True, null=True)
    url = models.CharField(verbose_name="IGDB Link", max_length=400, blank=True, null=True)
    # TODO: Developer and publisher should be reconfigured as collections of foreign keys derived
    # from Companies. The foreign keys will be sourced from the Companies IGDB data dump
    developer = models.CharField(verbose_name="Developer", max_length=300, blank=True, null=True)
    publisher = models.CharField(verbose_name="Publisher", max_length=300, blank=True, null=True)
    igdb_id = models.IntegerField(verbose_name="IGDB ID", default=0)
    igdb_name = models.CharField(verbose_name="IGDB Name", max_length=300)
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
        blank=True,
        null=True
    )
    file_name = models.CharField(verbose_name="Filename", max_length=400, null=True)
    version = models.CharField(verbose_name="Version", max_length=300, default='1.00 (Unverified)')
    release_date = models.DateField(verbose_name="Release Date", blank=True, null=True)
    # TODO: Developer and publisher exists on Game Version for cases where we know a specific Game Version
    # was developed or published by a specific Company. These will mostly be blank, and should also be
    # reconfigured into aggregates like on Game.
    developer = models.CharField(verbose_name="Developer", max_length=300, blank=True, null=True)
    publisher = models.CharField(verbose_name="Publisher", max_length=300, blank=True, null=True)
    is_archived = models.BooleanField(verbose_name="Archived", default=False)
    played_status = models.IntegerField(choices=PlayedStatusChoices.choices, default=PlayedStatusChoices.unplayed)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return f"{self.game} ({self.game.platform}) ({self.version})"
        return self.file_name

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
    igdb_name = models.CharField(verbose_name="IGDB Name", max_length=300)
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

class Company(models.Model):
    name = models.CharField(verbose_name="Company Name", max_length=300)
    founding_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
