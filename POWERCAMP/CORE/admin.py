from typing import Any

from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from teams.models import Member, Team


YELLOW: str = 'ffdd00'
BLUE: str = '0044ff'
ORANGE: str = 'ff7700'
BLACK: str = '444444'
PINK: str = 'ff0077'
PURPLE: str = '7700ff'
GREEN: str = '007700'
RED: str = 'aa0000'
TEAM_COLORS: list[str] = [YELLOW, BLUE, ORANGE, BLACK, PINK, PURPLE, GREEN, RED]


def foo() -> str:
    return """<script>
    function getBodyBgColor() {
      return getComputedStyle(document.documentElement)
      .getPropertyValue('--body-bg').trim();
    }

    function getBodyFgColor() {
      return getComputedStyle(document.documentElement)
      .getPropertyValue('--body-fg').trim();
    }

    var bodyBgColor = getBodyBgColor();
    var bodyFgColor = getBodyFgColor();
    </script>"""


def chart1() -> str:
    """Members per Team distribution"""

    return f"""<script>
        new Chart(document.getElementById('chart1'), {{
            type: 'doughnut',
            data: {{
                labels: {[team.color for team in Team.objects.all().order_by('color')]},
                datasets: [{{
                    data: {
        [
            Member.objects.filter(team=team.id).count()
            for team in Team.objects.all().order_by('color')
        ]
    },
                    backgroundColor: {[f'#{col}' for col in TEAM_COLORS]},
                    borderColor: [bodyBgColor],
                    borderWidth: 3
                }}]
            }},
            options: {{
                cutout: '60%',
                plugins: {{
                    legend: {{
                        position: 'top',
                        labels: {{
                            color: bodyFgColor
                        }}
                    }}
                }}
            }}
        }});
    </script>"""


def chart2() -> str:
    """Members inside vs outside a Team"""

    return f"""<script>
        new Chart(document.getElementById('chart2'), {{
            type: 'bar',
            data: {{
                labels: ['Com Equipe', 'Sem Equipe'],
                datasets: [{{
                    data: [
                        {Member.objects.exclude(team=None).count()},
                        {Member.objects.filter(team=None).count()},
                    ],
                    label: 'Membros e Equipes',
                    backgroundColor: {[f'#{BLUE}44', f'#{RED}44']},
                    borderColor: {[f'#{BLUE}', f'#{RED}']},
                    borderWidth: 3
                }}]
            }},
            options: {{
                maintainAspectRatio: false,
                title: {{
                    display: false,
                }},
                plugins: {{
                    legend: {{
                        labels: {{
                            color: bodyFgColor
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        type: 'logarithmic'
                    }}
                }}
            }}
        }});
    </script>"""


class PowerCampAdminSite(AdminSite):
    site_header = 'Administração Geral | PowerCamp'
    site_title = 'Admin'

    def index(
        self, request: WSGIRequest, extra_context: Any = None
    ) -> TemplateResponse:
        extra_context = extra_context or {}

        extra_context['admin_dashboard'] = {
            'range': range(2),
            'def_chart_colors': foo(),
            'chart1': chart1(),
            'chart2': chart2(),
        }

        return super().index(request, extra_context=extra_context)


adm = PowerCampAdminSite(name='customadmin')
adm.register(Group, GroupAdmin)
adm.register(User, UserAdmin)
