# Django

### 시작하기

```bash
# 프로젝트 폴더로 이동
cd myDjango

# 가상환경 설치
python3 -m venv myvenv
# 가상환경 실행
source myvenv/bin/activate

# Django 설치
pip3 install django
# Django 설치 확인
python3 -m django --version
```

### 프로젝트 만들기

```bash
# 프로젝트 만들기
django-admin startproject mysite

# 개발 서버 실행
cd mysite
python3 manage.py runserver
```

```bash
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

### 설문조사 앱 만들기

```bash
pyhton3 manage.py startapp polls
```

```bash
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

### 첫 번째 뷰 작성하기

- polls/views.py

    ```python
    polls/views.py¶
    from django.http import HttpResponse

    def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")
    ```

- polls/urls.py

    뷰를 호출하려면 이와 연결된 URL이 있어야하는데, 이를 위해 URLconf가 사용됩니다. polls 디렉토리에서 URLconf를 생성하려면, urls.py라는 파일을 생성해야 합니다.

    ```python
    from django.urls import path

    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
    ]
    ```

- mysite/urls.py

    다음 단계는, 최상위 URLconf 에서 polls.urls 모듈을 바라보게 설정합니다. mysite/urls.py 파일을 열고, django.urls.include를 import 하고, urlpatterns 리스트에 include() 함수를 다음과 같이 추가합니다. 

    ```python
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('polls/', include('polls.urls')),
        path('admin/', admin.site.urls),
    ]
    ```

    include() 함수는 다른 URLconf들을 참조할 수 있도록 도와줍니다. Django가 함수 include()를 만나게 되면, URL의 그 시점까지 일치하는 부분을 잘라내고, 남은 문자열 부분을 후속 처리를 위해 include 된 URLconf로 전달합니다.

- **언제 `[include()](https://docs.djangoproject.com/ko/3.1/ref/urls/#django.urls.include)`를 사용해야 하나요?**

    다른 URL 패턴을 포함할 때마다 항상 **`include()`**를 사용해야 합니다. **`admin.site.urls`**가 유일한 예외입니다.

- **path() 인수**
    - route

        필수 인수, route 는 URL 패턴을 가진 문자열 입니다. 요청이 처리될 때, Django 는 urlpatterns 의 첫 번째 패턴부터 시작하여, 일치하는 패턴을 찾을 때 까지 요청된 URL 을 각 패턴과 리스트의 순서대로 비교합니다. 

    - view

        필수 인수, Django 에서 일치하는 패턴을 찾으면, HttpRequest 객체를 첫번째 인수로 하고, 경로로 부터 〈캡처된〉 값을 키워드 인수로하여 특정한 view 함수를 호출합니다.

    - kwargs

        임의의 키워드 인수들은 목표한 view 에 사전형으로 전달됩니다.

    - name

        URL 에 이름을 지으면, 템플릿을 포함한 Django 어디에서나 명확하게 참조할 수 있습니다. 이 강력한 기능을 이용하여, 단 하나의 파일만 수정해도 project 내의 모든 URL 패턴을 바꿀 수 있도록 도와줍니다.

### 데이터베이스 설치

- mysite/setting.py 파일

    이 파일은 Django 설정을 모듈 변수로 표현한 보통의 Python 모듈이다.

    - INSTALLED_APPS

        Django 인스턴스에서 활성화된 모든 Django 어플리케이션들의  이름이 담겨 있다.

        기본적으로 Django와 함께 딸려오는 기본 앱들을 포함한다. 

        이 어플리케이션들은 일반적인 경우에 사용하기 편리하도록 기본으로 제공됩니다.

        이러한 기본 어플리케이션들 중 몇몇은 최소한 하나 이상의 데이터베이스 테이블을 사용하는데, 그러기 위해서는 데이터베이스에서 테이블을 미리 만들 필요가 있습니다. 이를 위해, 다음의 명령을 실행해봅시다.

        ```python
        python3 manage.py migrate
        ```

### 모델 만들기

- 모델이란 부가적인 메타데이터를 가진 데이터베이스의 구조(layout)을 말한다.
- polls/models.py

    ```python
    from django.db import models

    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

    class Choice(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)
    ```

    데이터베이스의 각 필드는 Field 클래스의 인스턴스로서 표현됩니다. CharField 는 문자(character) 필드를 표현하고, DateTimeField 는 날짜와 시간(datetime) 필드를 표현합니다. 이것은 각 필드가 어떤 자료형을 가질 수 있는지를 Django 에게 말해줍니다

### 모델의 활성화

모델에 대한 이 작은 코드가, Django에게는 상당한 양의 정보를 전달합니다. Django는 이 정보를 가지고 다음과 같은 일을 할 수 있습니다.

- 이 앱을 위한 데이터베이스 스키마 생성(**`CREATE TABLE`** 문)
- **`Question`**과 **`Choice`** 객체에 접근하기 위한 Python 데이터베이스 접근 API를 생성

그러나, 가장 먼저 현재 프로젝트에게 **`polls`** 앱이 설치되어 있다는 것을 알려야 합니다.

앱을 현재의 프로젝트에 포함시키기 위해서는, 앱의 구성 클래스에 대한 참조를 INSTALLED_APPS 설정에 추가해야 합니다. PollsConfig 클래스는 polls/apps.py 파일 내에 존재합니다. 따라서, 점으로 구분된 경로는 'polls.apps.PollsConfig'가 됩니다. 이 점으로 구분된 경로를, mysite/settings.py 파일을 편집하여 INSTALLED_APPS 설정에 추가하면 됩니다. 이는 다음과 같이 보일 것입니다.

- mysite/settings.py

    ```python
    INSTALLED_APPS = [
        'polls.apps.PollsConfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    ```

    ```bash
    python3 manage.py makemigrations polls
    python3 manage.py migrate
    ```

    migrate 명령은 아직 적용되지 않은 마이그레이션을 모두 수집해 이를 실행하며(Django는 django_migrations 테이블을 두어 마이그레이션 적용 여부를 추적합니다) 이 과정을 통해 모델에서의 변경 사항들과 데이터베이스의 스키마의 동기화가 이루어집니다.

- 모델의 변경을 만드는 세 단계의 지침
    - (**`models.py`** 에서) 모델을 변경합니다.
    - **`[python manage.py makemigrations](https://docs.djangoproject.com/ko/3.1/ref/django-admin/#django-admin-makemigrations)`**을 통해 이 변경사항에 대한 마이그레이션을 만드세요.
    - **`[python manage.py migrate](https://docs.djangoproject.com/ko/3.1/ref/django-admin/#django-admin-migrate)`** 명령을 통해 변경사항을 데이터베이스에 적용하세요.

### API 가지고 놀기

- polls/models.py

    ```python
    from django.db import models

    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        def __str__(self):
            return self.question_text
        def was_published_recently(self):
            return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Choice(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)
        def __str__(self):
            return self.choice_text
    ```

- python shell 사용

    ```bash
    python3 manage.py shell
    ```

### 관리자 생성하기

```bash
python3 manage.py createsuperuser

Username: admin
Email address: admin@example.com
Password: **********
Password (again): *********
Superuser created successfully.
```

### 뷰 추가하기

- polls/views.py

    ```python
    def detail(request, question_id):
        return HttpResponse("You're looking at question %s." % question_id)

    def results(request, question_id):
        response = "You're looking at the results of question %s."
        return HttpResponse(response % question_id)

    def vote(request, question_id):
        return HttpResponse("You're voting on question %s." % question_id)
    ```

- polls/urls.py

    ```python
    from django.urls import path

    from . import views

    urlpatterns = [
        # ex: /polls/
        path('', views.index, name='index'),
        # ex: /polls/5/
        path('<int:question_id>/', views.detail, name='detail'),
        # ex: /polls/5/results/
        path('<int:question_id>/results/', views.results, name='results'),
        # ex: /polls/5/vote/
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]
    ```

### 뷰 실제로 사용하기

- polls/views.py

    ```python
    from django.http import HttpResponse
    from django.template import loader

    from .models import Question

    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        template = loader.get_template('polls/index.html')
        context = {
            'latest_question_list': latest_question_list,
        }
        return HttpResponse(template.render(context, request))
    ```

- 지름길: render()

    ```python
    from django.shortcuts import render

    from .models import Question

    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        context = {'latest_question_list': latest_question_list}
        return render(request, 'polls/index.html', context)
    ```

- polls/views.py - 404 에러 일으키기

    ```python
    from django.http import Http404
    from django.shortcuts import render

    from .models import Question
    # ...
    def detail(request, question_id):
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request, 'polls/detail.html', {'question': question})
    ```

- 지름길: get_object_or_404()

    ```python
    polls/views.py¶
    from django.shortcuts import get_object_or_404, render

    from .models import Question
    # ...
    def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/detail.html', {'question': question})
    ```

### 템플릿 시스템 사용하기

- 앱 폴더에 templates 폴더를 만들어서 사용
- polls/templates/polls/detail.html

    ```python
    <h1>{{ question.question_text }}</h1>
    <ul>
    {% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
    {% endfor %}
    </ul>
    ```

### 템플릿에서 하드코딩된 URL 제거하기

- polls/index.html

    ```python
    # 하드코딩된 URL - 바람직하지 않음
    <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    ```

    ```python
    # url 사용으로 의존성 제거 - 바람직한 방법
    <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
    ```

### URL의 이름공간 정하기

- polls/urls.py

    ```python
    from django.urls import path

    from . import views

    app_name = 'polls'
    urlpatterns = [
        path('', views.index, name='index'),
        path('<int:question_id>/', views.detail, name='detail'),
        path('<int:question_id>/results/', views.results, name='results'),
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]
    ```

- polls/index.html

    ```python
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
    ```

### 제너릭 뷰 사용하기

- URLconf 수정
    - polls/urls.py

        ```python
        from django.urls import path

        from . import views

        app_name = 'polls'
        urlpatterns = [
            path('', views.IndexView.as_view(), name='index'),
            path('<int:pk>/', views.DetailView.as_view(), name='detail'),
            path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
            path('<int:question_id>/vote/', views.vote, name='vote'),
        ]
        ```

- views 수정
    - polls/views.py

        ```python
        from django.http import HttpResponseRedirect
        from django.shortcuts import get_object_or_404, render
        from django.urls import reverse
        from django.views import generic

        from .models import Choice, Question

        class IndexView(generic.ListView):
            template_name = 'polls/index.html'
            context_object_name = 'latest_question_list'

            def get_queryset(self):
                """Return the last five published questions."""
                return Question.objects.order_by('-pub_date')[:5]

        class DetailView(generic.DetailView):
            model = Question
            template_name = 'polls/detail.html'

        class ResultsView(generic.DetailView):
            model = Question
            template_name = 'polls/results.html'

        def vote(request, question_id):
            ... # same as above, no changes needed.
        ```

### static 사용하기

- mysite/setting.py

    ```python
    STATIC_URL = 'polls/static/'
    ```

- polls/static/polls/style.css

    ```python
    li a {
        color: green;
    }
    ```

- polls/templates/polls/index.html

    ```python
    #맨 위에 추가
    {% load static %}

    <link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}">
    ```