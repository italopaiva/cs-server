from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from bricks.contrib.mdl import button, div
from bricks.html5 import ul, li, a, i, select, option, input, table, tbody, thead, th, td, tr
from codeschool.bricks import navbar as _navbar, navsection
from codeschool.models import User
from .bricks import navbar, layout, activities_layout
from .forms import CsvUploadForm, NewUserGradeForm
from .models import UserGrade, SpartaActivity

# Create your views here.
def index(request):
    ctx = {
    'main':layout(),
    'navbar':navbar(),
    }
    return render(request, 'sparta/index.jinja2', ctx)

def activities(request):

    ctx = {
    'content_title':'Atividades',
    'content_body':activities_layout(),
    }
    return render(request, 'sparta/activities.jinja2', ctx)

def rating(request):

    ctx = {
        'content_title':'Avaliação dos Membros',
        'content_body': ul(class_="demo-list-icon mdl-list")[
        table(class_="mdl-data-table mdl-js-data-table mdl-shadow--2dp")[
        div(class_="mdl-tooltip", for_="tt1")['Já Avaliado'],
          thead()[
            tr()[
              th(class_="mdl-data-table__cell--non-numeric")['Aluno'],
              th()['Avaliações'],
              th()['Nota'],
              th()['Avaliar'],
            ]
          ],
          tbody()[
            tr()[
              td(class_="mdl-data-table__cell--non-numeric")['Goku da Silva Mendes'],
              td()['3 Aluno(s)'],
              td()['10'],
             td()[
               i(class_="material-icons", id='tt1')['done'],
               ],
            ],
            tr()[
              td(class_="mdl-data-table__cell--non-numeric")['Ronaldo Andrade Souza'],
              td()['0 Aluno(s)'],
              td()['0'],
              td()[
                i(class_="material-icons")['mode_edit'],
                ]
            ],
            tr()[
              td(class_="mdl-data-table__cell--non-numeric")['Florentina de Jesus'],
              td()['0 Aluno(s)'],
              td()['0'],
              td()[
                i(class_="material-icons")['mode_edit'],
                ]
            ],
          ],
        ],
    ]
    }
    return render(request, 'sparta/rating.jinja2', ctx)

def uploadcsv(request, activity_id):
    activity = SpartaActivity.objects.get(pk=activity_id)
    if request.POST:
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_data = request.FILES['csv_file'].read().decode('utf-8').strip()
            activity.populate_from_csv(file_data)
            return redirect('sparta_user_grades', activity_id=activity.pk)
        ctx = {
            'form': form,
            'activity_id': activity_id,
        }
        return render(request, 'sparta/uploadcsv.jinja2', ctx)
    else:
        form = CsvUploadForm()
        ctx = {
            'form': form,
            'activity_id': activity_id,
        }
    return render(request, 'sparta/uploadcsv.jinja2', ctx)

def get_user_grades(request, activity):
    grades = UserGrade.objects.filter(activity=activity)
    ctx = {'grades': grades, 'activity': activity}
    return render(request, 'sparta/user_grades.jinja2', ctx)

def update_user_grade(request, activity):
    post_data = dict(request.POST.lists())
    students = post_data['students[]']
    grades = post_data['grades[]']
    student_grades_map = dict(zip(students, grades))
    UserGrade.update_activity_grades(activity, student_grades_map)
    return redirect('sparta_user_grades', activity_id=activity.pk)

@login_required
def user_grade_view(request, activity_id):
    activity = SpartaActivity.objects.get(pk=activity_id)
    if not request.user == activity.teacher:
        # User grades are only visible to the teacher of the activity
        redirect('sparta_index')
    if request.POST:
        return update_user_grade(request, activity)
    else:
        return get_user_grades(request, activity)


class NewUserGradeView(View):
    """
    View to handle new user grade requests.
    """
    form = NewUserGradeForm

    @method_decorator(login_required)
    def get(self, request, activity_id):
        activity = SpartaActivity.objects.get(pk=activity_id)
        form = self.filter_registered_users(activity)
        ctx = {
            'activity': activity,
            'form': form
        }
        return render(request, 'sparta/new_user_grade.jinja2', ctx)

    @method_decorator(login_required)
    def post(self, request, activity_id):
        activity = SpartaActivity.objects.get(pk=activity_id)
        user_grade = UserGrade(activity=activity)
        form = self.form(data=request.POST, instance=user_grade)
        if form.is_valid():
            form.save()
            return redirect('sparta_user_grades', activity_id=activity.pk)
        else:
            ctx = {
                'activity': activity,
                'form': self.filter_registered_users(activity, form=form)
            }
            return render(request, 'sparta/new_user_grade.jinja2', ctx)

    def filter_registered_users(self, activity, form=None):
        """Remove from form users that are already registered in the activity."""
        if not form:
            form = self.form()
        registered_users = [user_grade.user.username for user_grade in activity.user_grades.all()]
        form.fields['user'].queryset = User.objects\
            .exclude(username__in=registered_users)\
            .exclude(pk=activity.teacher.pk)
        return form