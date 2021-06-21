import logging

from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import redirect
from django.utils.html import format_html

from .models import Funktion
from .tasks import save_plot_task


logger = logging.getLogger(__name__)


class FunktionAdmin(admin.ModelAdmin):
    change_form_template = "admin/change_form1.html"
    change_list_template = "admin/my_admin_list.html"
    list_display = ('func', 'graph', 'interval', 'step', 'time_seconds')
    readonly_fields = ('graph',)
    fields = ('func', 'interval', 'step')

    def graph(self, obj):
        url = obj.plot.url if obj.plot else None
        if url:
            return format_html(f'<a href={url}>'
                               f'<img src="{url}"width="240" height="240" />'
                               '</a>')
        else:
            return obj.errorfield

    def time_seconds(self, obj):
        return obj.last_date.strftime("%d-%m-%Y %H:%M:%S.%f")
    time_seconds.short_description = 'время обработки'

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        id = obj.save()
        transaction.commit
        logger.warning(f'-----function created with id {id}-----')
        pid = save_plot_task.apply_async(args=(id,), countdown=0.5)
        request.session['task_id'] = str(pid)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    actions = ["renew"]

    def renew(self, request, obj):
        return redirect('/admin/funcapp/funktion/')
    renew.short_description = 'Обновить'


admin.site.register(Funktion, FunktionAdmin)
admin.site.unregister(Group)
