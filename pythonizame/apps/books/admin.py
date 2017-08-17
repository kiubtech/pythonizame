from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from pythonizame.apps.books.models import Book, TagBook, BookCategory


@admin.register(TagBook)
class TagBookAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',), }


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'preview', 'published', 'publication_date', )
    fields = (('title', 'slug'), ('image', 'file'), 'author', 'url', 'description', 'categories', 'tags')
    filter_horizontal = ('categories', 'tags', )
    prepopulated_fields = {'slug': ('title',), }
    actions = ['publish_this']

    def save_model(self, request, obj, form, change):
        try:
            creador = obj.created_by
            if creador:
                has_created_by = True
            else:
                has_created_by = False
        except:
            has_created_by = False
        if not has_created_by:
            obj.created_by = request.user
        obj.save()

    def publish_this(self, request, queryset):
        if request.user.is_superuser or 'Administrador' in request.user.groups.values_list('name', flat=True):
            for obj in queryset:
                if not obj.published:
                    obj.published = True
                    obj.publication_date = timezone.now()
                    obj.save()
                    message = "Hemos publicado el libro exitosamente"
                    messages.success(request, message)
                else:
                    message = "Libro ya ha sido publicada anteriormente"
                    messages.warning(request, message)
        else:
            message = "No cuentas con los permisos suficientes para ejecutar esta acción"
            messages.error(request, message)

    publish_this.label = "Publicar"  # optional
    publish_this.short_description = "Publicar Libro"  # optional



@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',), }

