from CORE.admin import adm
from django.contrib.admin import ModelAdmin

from teams.models import Member, Team


class TeamAdmin(ModelAdmin):  # type: ignore
    actions_selection_counter = True
    empty_value_display = 'A Definir'
    list_filter = ('color',)
    list_display = ('color', 'name', 'mascot')
    ordering = ('color',)
    show_full_result_count = True


class MemberAdmin(ModelAdmin):  # type: ignore
    actions_selection_counter = True
    empty_value_display = 'A Definir'
    list_filter = ('team', 'is_team_leader', 'is_mascot')
    list_display = ('name', 'is_team_leader', 'is_mascot', 'team')
    ordering = ('name',)
    search_fields = ('name',)
    show_full_result_count = True


adm.register(Team, TeamAdmin)
adm.register(Member, MemberAdmin)
