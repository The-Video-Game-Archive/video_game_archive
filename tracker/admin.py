from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from datetime import datetime

from .models import Game, GameVersion, Platform, PlatformVersion

class GameResource(resources.ModelResource):

    class Meta:
        model = Game
        fields = ('id', 'name', 'platform', 'description', 'release_date', 'url', 'igdb_id', 'created_at')

    def convert_date(self, row_date):
        return datetime.strptime(row_date, '%Y-%m-%d %H:%M:%S') if row_date else None
    
    def get_platform_objects(self, row_platforms):
        platform_ids = row_platforms[1:-1].split(',') if row_platforms else []
        platform_objects = []

        if platform_ids:
            for platform_id in platform_ids:
                platform_id = platform_id.strip()
                try:
                    platform = Platform.objects.get(pk=int(platform_id))
                    platform_objects.append(platform)
                except (Platform.DoesNotExist):
                    print(f"Platform with ID {platform_id} does not exist.")

        return platform_objects
    
    def before_import_row(self, row, **kwargs):
        game_instance = {
            'name': row['name'],
            'description': row['summary'],
            'release_date': self.convert_date(row['first_release_date']),
            'url': row['url'],
            'igdb_id': row['id']
        }
        platforms = self.get_platform_objects(row['platforms'])

        if not platforms:
            Game.objects.get_or_create(**game_instance)
        else:
            for platform in platforms:
                game_instance['platform'] = platform
                Game.objects.get_or_create(**game_instance)        

    def save_instance(self, instance, is_create, row, **kwargs):
        pass

class PlatformResource(resources.ModelResource):

    class Meta:
        model = Platform
        fields = ('id', 'name', 'url', 'generation')


class GameAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'platform', 'release_date', 'test_boolean', 'igdb_id', 'created_at')
    
    resource_classes = [GameResource]

class GameVersionAdmin(ImportExportModelAdmin):
    list_display = ('game_name', 'version', 'release_date', 'is_archived', 'played_status')

    def game_name(self, obj):
        return obj.game.name
    
    # resource_classes = [GameVersionResource]

class PlatformAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'release_date', 'url', 'generation')

    resource_classes = [PlatformResource]


admin.site.register(Game, GameAdmin)
admin.site.register(GameVersion, GameVersionAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(PlatformVersion)
