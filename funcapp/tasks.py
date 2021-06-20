import datetime

from celery.decorators import task
from celery.signals import task_success
from celery.utils.log import get_task_logger

from django.core.files.base import ContentFile
from django.utils import timezone

from . import plot

logger = get_task_logger(__name__)


@task(name='save_plot_task')
def save_plot_task(id):
    from .models import Funktion
    logger.warning(f"Look if object with id {id} exists")
    if not Funktion.objects.filter(pk=id).exists():
        logger.warning("Object not found")
        return
    obj = Funktion.objects.get(pk=id)
    logger.info(f"Object found - {obj.pk}")
    arrx = plot.getX(obj.interval, obj.step)
    arry = plot.getY(arrx[0], obj.func)
    if arry[1]:
        f = plot.plott(arrx[1], arry[0])
        content_file = ContentFile(f.getvalue())
        logger.info(f"Save plot image - {content_file} - {f}")
        obj.plot.save(f'plot_{id}.png', content_file, save=False)
        logger.info(f"file plot_{id}.png saved")
    else:
        logger.info(f"Save error message{arry[0]}")
        obj.errorfield = arry[0]
    obj.last_date = datetime.datetime.now(tz=timezone.utc)
    obj.save()
    return True


@task_success.connect(sender=save_plot_task)
def task_success_notifier(sender=None, **kwargs):
    print("From task_success_notifier ==> Task run successfully!")
