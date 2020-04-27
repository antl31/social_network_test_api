from django.contrib import admin
from .models import Post, User,PostLike


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, AuthorAdmin)
admin.site.register(User, AuthorAdmin)
admin.site.register(PostLike, AuthorAdmin)
