from django.shortcuts import render
from bricks.contrib.mdl import button, div
from bricks.html5 import ul, li, a, i, select, option, input, table, tbody, thead, th, td, tr
from codeschool.bricks import navbar as _navbar, navsection
from .bricks import navbar, layout, activities_layout
from .forms import CsvUploadForm
from .models import SpartaActivity

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

            var = activity.populate_from_csv(file_data, commit=False)
            import pdb; pdb.set_trace()
            return HttpResponseRedirect('/success/url/')
        ctx = {
            'content_title':'Upload de CSV de notas!',
            'content_body': ul(class_="demo-list-icon mdl-list"),
            'form': form,
            'activity_id': activity_id
        }
        return render(request, 'sparta/uploadcsv.jinja2', ctx)
    else:
        form = CsvUploadForm()
        ctx = {
            'content_title':'Upload de CSV de notas',
            'content_body': ul(class_="demo-list-icon mdl-list"),
            'form': form,
            'activity_id': activity_id
        }
    return render(request, 'sparta/uploadcsv.jinja2', ctx)
