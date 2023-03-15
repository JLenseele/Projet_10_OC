from django.contrib import admin
from issuetracking.models import Project, Contributor, Issue, Comments


class ProjectAdmin(admin.ModelAdmin):

    list_display = ('title', 'type', 'status', 'author')


class ContributorAdmin(admin.ModelAdmin):

    list_display = ('project', 'user', 'permission', 'role')


class IssueAdmin(admin.ModelAdmin):

    list_display = ('title', 'status', 'project_id', 'author', 'assign')
    '''
    @admin.display(description='Category')
    def category(self, obj):
        return obj.product.category'''


class CommentsAdmin(admin.ModelAdmin):

    list_display = ('desc', 'author', 'issue')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comments, CommentsAdmin)
