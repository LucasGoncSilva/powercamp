from django.contrib import admin

from teams.models import Member, Team


class TeamAdmin(admin.ModelAdmin):  # type: ignore
    actions_selection_counter = True
    empty_value_display = 'A Definir'
    list_filter = ('color',)
    list_display = ('color', 'name', 'mascot')
    ordering = ('color',)
    show_full_result_count = True


class MemberAdmin(admin.ModelAdmin):  # type: ignore
    actions_selection_counter = True
    empty_value_display = 'A Definir'
    list_filter = ('team', 'is_team_leader', 'is_mascot')
    list_display = ('name', 'is_team_leader', 'is_mascot', 'team')
    ordering = ('name',)
    search_fields = ('name',)
    show_full_result_count = True


admin.site.register(Team, TeamAdmin)
admin.site.register(Member, MemberAdmin)
