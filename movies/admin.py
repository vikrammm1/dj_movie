from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import Category, Actor, Genre, Movie, MovieShots, RettingStar, Rating, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Опис', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name', )


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height = "110"')

    get_image.short_description = 'Кадри з фільму'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year', )
    search_fields = ('title', 'category__name', )
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    readonly_fields = ('get_image', )
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'), )
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'worlds_premiere', 'country'),)
        }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fess_in_usa', 'fess_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height = "110"')

    def unpublish(self, request, queryset):
        '''Зняти з публікації'''
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запис був вилучено'
        else:
            message_bit = f'{row_update} записів було вилучено'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        '''Публікація'''
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запис був опубліковано'
        else:
            message_bit = f'{row_update} записів було оновлено'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опублікувати'
    publish.allowed_permissions = ('change', )

    unpublish.short_description = 'Зняти з публікації'
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height = "60"')

    get_image.short_description = 'Зображення'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height = "60"')

    get_image.short_description = 'Кадри з фільму'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'movie', 'ip')


admin.site.register(RettingStar)


admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
