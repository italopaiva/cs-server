INSTALLED_APPS = [
    # Codeschool apps
    'codeschool.questions.numeric',
    # 'codeschool.questions.coding_io',
    'codeschool.questions',
    # 'codeschool.gamification',
    'codeschool.lms.activities',
    # 'codeschool.lms.courses',

    # These are required
    #'codeschool.social.feed',
    #'codeschool.social.friends',
    'codeschool.accounts',
    'codeschool.core',

    # Related apps
    'model_reference',
    'srvice',

    # Wagtail and dependencies
    'codeschool.vendor.wagtailmarkdown',
    'wagtail.contrib.wagtailroutablepage',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.table_block',
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'modelcluster',
    'taggit',

    # Userena
    'userena',
    'easy_thumbnails',
    'guardian',

    # Other 3rd party
    'polymorphic',
    'django_extensions',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]