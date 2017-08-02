from django.core.management.base import BaseCommand, CommandError
from quest.models import *
import os
import server.settings
import quest.google_api.api
import random

class Command(BaseCommand):
    help = 'Update views count for quests'

    SCOPE = ['https://www.googleapis.com/auth/analytics.readonly']
    SERVICE_ACCOUNT_EMAIL = 'service@ageless-granite-156009.iam.gserviceaccount.com'
    KEY_FILE_LOCATION = os.path.join(server.settings.BASE_DIR, 'quest', 'google_api', 'Analytics-691f0dc58d05.p12')

    def updateDB(self, results):
        if results and isinstance(results, dict) and 'rows' in results:
            rows = results['rows']
            Quest.objects.all().update(view_count=0)
            for path, v in {r[0]: {'views': r[1], 'uviews': r[2]} for r in rows}.items():
                url = filter(None, path.rsplit('/'))[-1]
                # print url, v['views'], v['uviews']
                try:
                    q = Quest.objects.get(seo_url=url)
                    q.view_count = int(v['views'])
                    q.save()
                except:
                    pass

        visitors, created = Settings.objects.get_or_create(name='visitors_count')
        min, min_created = Settings.objects.get_or_create(name='visitors_min_count')
        max, max_created = Settings.objects.get_or_create(name='visitors_max_count')
        dx, dx_created = Settings.objects.get_or_create(name='visitors_dx_count')

        if min_created:
            min.value = 7
            min.save()
        if max_created:
            max.value = 38
            max.save()
        if dx_created:
            dx.value = 3
            dx.save()

        val = 0

        if created:
            val = random.randint(int(min.value), int(max.value))
        else:
            val = random.randint(int(visitors.value) - int(dx.value), int(visitors.value) + int(dx.value))

        if val > int(max.value):
            val = max.value
        elif val < int(min.value):
            val = min.value

        visitors.value = val

        visitors.save()




    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # Authenticate and construct service.
        service = quest.google_api.api.get_service('analytics', 'v3', Command.SCOPE,
                                                 Command.KEY_FILE_LOCATION,
                                                 Command.SERVICE_ACCOUNT_EMAIL)
        profile = quest.google_api.api.get_first_profile_id(service)
        results = quest.google_api.api.get_pageviews(service, profile)
        self.updateDB(results)