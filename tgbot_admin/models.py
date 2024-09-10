from django.db import models
from django.utils import timezone
from asgiref.sync import sync_to_async
from django.db import close_old_connections

# Create your models here.
class TodoList(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)  # Текстовое поле
    created = models.DateField(default=timezone.now)  # Дата создания


    class Meta:
        ordering = ["-created"]  # Сортировка дел по времени их создания

    def __str__(self):
        return self.title
    
@sync_to_async
def get_list():
    return TodoList.objects.all()
# async def get_list():
#     @sync_to_async
#     def _get_user():
#         close_old_connections()
#         return TodoList.objects.all()
#     return await _get_user()
    