from celery.task import task
import quest.google_drive.api2 as google_api
from .models import GoogleDriveDoc

@task(ignore_result=True, max_retries=1, default_retry_delay=10)
def update_google_drive_photos():
    print "Start updating Players images"

    count = 0
    service = google_api.getDriveService(google_api.USER)
    days = google_api.getAllDays(service, google_api.ROOT_FOLDER)
    imgs = google_api.getAllImgs(service, days)
    persisted_imgs = GoogleDriveDoc.objects.filter(type='img-p').values_list('id', flat=True)
    new_imgs = [i for i in imgs if i['id'] not in persisted_imgs]

    for ni in new_imgs:
        doc = GoogleDriveDoc(id=ni['id'], name=ni['name'], type='img-p')
        doc.save()
        share_google_drive_photos(ni['id'])
        count += 1
    print "New images stored =", count

@task(ignore_result=True, max_retries=1, default_retry_delay=10)
def share_google_drive_photos(id):
    service = google_api.getDriveService(google_api.USER)
    permission = {
        'type': 'anyone',
        'role': 'reader',
        'allowFileDiscovery': True
    }
    service.permissions().create(fileId=id, body=permission).execute()

@task(ignore_result=True, max_retries=1, default_retry_delay=10)
def share_all_google_drive_photos():
    print "Start sharing Players images"

    count = 0
    service = google_api.getDriveService(google_api.USER)
    permission = {
        'type': 'anyone',
        'role': 'reader',
        'allowFileDiscovery': True
    }
    for img in GoogleDriveDoc.objects.all():
        service.permissions().create(fileId=img.id, body=permission).execute()
        count += 1

    print "End sharing Players images =", count