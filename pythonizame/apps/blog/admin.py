from django.contrib import admin
from django.contrib import messages
from django.utils import timezone

# from django_object_actions import DjangoObjectActions

from pythonizame.apps.blog.models import Post, Category, LikePost, TagPost


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    fields = ('name', 'slug',)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',), }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'slug', 'abstract',
                    'timestamp', 'last_modified', 'preview', 'publication_date', 'published')
    list_display_links = ('id', 'title',)
    fields = (('title', 'slug'), 'main_image', 'pin_image', 'author_image', 'author_link',
              'abstract', 'content', 'categories', 'tags')
    prepopulated_fields = {'slug': ('title',), }
    actions = ['make_published', ]
    filter_horizontal = ('categories', 'tags',)
    search_fields = ['title', 'content', 'tags__name']
    list_per_page = 10

    def publish_this(self, request, obj):
        if request.user.is_superuser or 'Administrador' in request.user.groups.values_list('name', flat=True):
            if not obj.published:
                obj.published = True
                obj.publication_date = timezone.now()
                obj.save()
                message = "Hemos publicado la entrada exitosamente"
                messages.success(request, message)
            else:
                message = "Entrada ya ha sido publicada anteriormente"
                messages.warning(request, message)
        else:
            message = "No cuentas con los permisos suficientes para ejecutar esta acción"
            messages.error(request, message)

    publish_this.label = "Publicar"  # optional
    publish_this.short_description = "Publicar el el contenido del post"  # optional

    # objectactions = ('publish_this', )

    def save_model(self, request, obj, form, change):
        try:
            creador = obj.author
            if creador:
                has_created_by = True
            else:
                has_created_by = False
        except:
            has_created_by = False
        if not has_created_by:
            obj.author = request.user
        obj.save()

    def make_published(self, request, queryset):
        if request.user.is_superuser or 'Administrador' in request.user.groups.values_list('name', flat=True):
            for post in queryset:
                if post.published:
                    messages.warning(request, 'Entrada "%s" ya ha sido publicada anteriormente' % post.title)
                else:
                    post.published = True
                    post.publication_date = timezone.now()
                    post.save()
                    messages.success(request, 'Entrada "%s2 publicada correctamente' % post.title)
        else:
            message = "No cuentas con los permisos suficientes para ejecutar esta acción"
            messages.error(request, message)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    make_published.short_description = "Publicar entradas"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    prepopulated_fields = {'slug': ('name',), }


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'post')
