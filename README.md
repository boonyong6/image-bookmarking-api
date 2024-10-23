# Preface

## What this book covers

- Four fully-featured web applications
  1. **Blog** (chapters 1 to 3)
     - Content management
     - Commenting
     - Post sharing
     - Search
     - Post recommendations
  2. **Image bookmarking** (chapters 4 to 7)
  3. **Online shop** (chapters 8 to 11)
  4. **e-learning platform** (chapters 12 to 17)

# 1 Building a Blog Application

- Covers the essential building blocks, **important Django project settings**.
- **Major components** - models, templates, views, and URLs.
- Features to build:
  - Navigate through all **published** posts.
  - Read individual posts.
  - **Admin site** to manage and publish posts.

## Installing Python

- In **Windows**, `py` is the Python launcher. It delegates to the **latest version**.

## Django overview

### Main framework components

- **MTV (Model-Template-View)** pattern:

  | Component | Responsibility                                                                                                                                  |
  | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
  | Model     | - Data structure.<br />- **Data handler** between the database and the view.<br />- Provides **data definitions** and **behaviors** (ORM APIs). |
  | Template  | - **Presentation layer**.                                                                                                                       |
  | View      | - Communicates with the database via the **model**.<br />- Transfers the data to the **template** for viewing.                                  |

- Django sends a **request** to the appropriate **view**, according to the **URL configuration**.

### The Django architecture

![1-1-request-response-cycle](images/1-1-request-response-cycle.png)

## Creating your first project - `django-admin startproject`

- To create a Django project, named `mysite`:
  ```bash
  $ django-admin startproject mysite
  ```
- **Outer** `mysite/` is the **container for our project**. It contains:
  - `manage.py` - **Command-line utility** used to interact with your project.
  - `mysite/` - **Python package for your project**. It contains:
    - `__init__.py`
    - `asgi.py`
      - **Configuration** to run your project with **ASGI-compatible web servers**.
      - **Emerging standard** for **asynchronous** web servers and applications.
    - `settings.py` - Settings and configuration for your project.
    - `urls.py` - Contains **URL patterns**. Each URL is **mapped to a view**.
    - `wsgi.py` - **Configuration** to run your project with **WSGI-compatible web servers**.

### Applying initial database migrations - `migrate`

- In `settings.py`, `INSTALLED_APPS` constant contains **common Django applications** that are **added** to your project **by default**.
- To complete the project setup, you need to **create the tables** associated with the models of the **default Django applications**.
  ```bash
  $ python manage.py migrate
  ```

### Running the development server - `runserver`

- Keeps **checking for changes** and **reloads** automatically.
- **Might not notice** some actions, such as **adding new files**.
- To start the development server:

  ```bash
  $ python manage.py runserver

  # To run on a custom host and port or to load a specific settings file.
  $ python manage.py runserver 127.0.0.1:8001 --settings=mysite.settings
  ```

- Only intended for development.
- **For production**, use the following web servers:
  1. **WSGI**-compatible - Apache, Gunicorn, or uWSGI.
  2. **ASGI**-compatible - Daphne or Uvicorn.

### Project settings - `settings.py`

- By default, Django includes **only part** of [all the settings](https://docs.djangoproject.com/en/5.0/ref/settings/).
- Notable project settings:

  | Setting          | Description                                                                                                      |
  | ---------------- | ---------------------------------------------------------------------------------------------------------------- |
  | `ALLOWED_HOSTS`  | When `DEBUG` is `False` (production), you'll have to add your domain/host to allow it to serve your Django site. |
  | `INSTALLED_APPS` | Indicates which applications are active for this site.                                                           |
  | `USE_TZ`         | Provides support for timezone-aware datetime.                                                                    |

### Projects and applications

- **Project** is a **Django installation** with some **settings**.
- **Application** is a **group** of models, views, templates, and URLs.

### Creating an application - `startapp`

- To create an application, named `blog`:
  ```bash
  $ python manage.py startapp blog
  ```
- `blog/` contains:
  - `__init__.py`
  - `admin.py` - **Register models** to include them in the **Django admin site**.
  - `apps.py` - Main **configuration** of the application.
  - `migrations/` - Contains **database migrations**.
  - `models.py` - All Django applications **must have** a `models.py` file.
  - `tests.py`
  - `views.py` - Logic of your application.

## Creating the blog data models

- A Django model is a **source of information** about the **behaviors** of your data.
- Subclass `django.db.models.Model` to create a model.
- Each model maps to a **single database table**.

### Creating the Post model

- **Model field types** used:

  | Field           | Description                                                                                                                                                                                                                                        |
  | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | `CharField`     | - `VARCHAR` column.                                                                                                                                                                                                                                |
  | `SlugField`     | - `VARCHAR` column.<br />- A short label that **contains only letters, numbers, underscores, or hyphens**.<br />- **E.g.** Django Reinhardt: A legend of Jazz -> django-reinhardt-legend-jazz<br />- **Use case:** To build **SEO-friendly URLs**. |
  | `TextField`     | - `TEXT` column.                                                                                                                                                                                                                                   |
  | `DateTimeField` | - `DATETIME` column.                                                                                                                                                                                                                               |

- Django uses `__str__()` to display the object name in many places, such as the **admin site**.
- **By default**, Django **adds an auto-incrementing primary key field** (`id`) to each model.
  - **Field type for this** is specified in each app config (`apps.py`) or globally in the `settings.py` (`DEFAULT_AUTO_FIELD`).
  - Default field type - `BigAutoField` (64-bit integer)
  - Set `primary_key=True` on a field to make it the primary key.

### Adding datetime fields - `models.DateTimeField()`

- Ways to define the **default value** for the `DateTimeField`:

  ```py
  class Post(models.Model):
      # Method 1:
      # Use `django.utils.timezone` module to handle datetime in
      #   a timezone-aware manner.
      publish = models.DateTimeField(default=timezone.now)

      # Method 2:
      # Database-computed default values (introduced in Django 5)
      #   by using `django.db.models.functions.Now`.
      publish = models.DateTimeField(db_default=Now())
  ```

- By using `auto_now_add`, the date will be **saved automatically when creating** an object.
- By using `auto_now`, the date will be **updated automatically when saving** an object.
- Additional resources:
  - [`db_default` attribute](https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.Field.db_default)
  - [Database functions](https://docs.djangoproject.com/en/5.0/ref/models/database-functions/)

### Defining a default sort order - `<Model>.Meta.ordering`

- Takes effect **when retrieving objects** (`ORDER BY`) from the database.

  ```py
  class Post(models.Model):
      ...

      # Defines metadata.
      class Meta:
          ...
          ordering = ["-publish"]  # Descending order.
  ```

### Adding a database index - `<Model>.Meta.indexes`

- **Note:** Index ordering is not supported on MySQL. A descending index will be created as a normal index.

  ```py
  class Post(models.Model):
      ...

      # Defines metadata.
      class Meta:
          ...
          indexes = [
              models.Index(fields=["-publish"])  # Descending index.
          ]
  ```

- Additional resource - [How to define indexes for models](https://docs.djangoproject.com/en/5.0/ref/models/indexes/)

### Activating the application - `INSTALLED_APPS`

- Activate the `blog` application **in the project** and be able to **create database tables** for its models.
- Add the app config (`blog.apps.BlogConfig`) to the `INSTALLED_APPS` setting in `settings.py`. This enables the project to load the app models.

### Adding a status field (enum) - `models.TextChoices`

```py
class Post(models.Model):
    # Enum type
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    # Model fields.
    ...
    status = models.CharField(
        max_length=2,
        choices=Status,  # <--
        default=Status.DRAFT
    )
```

| `TextChoices` attribute | Description                                              |
| ----------------------- | -------------------------------------------------------- |
| `Post.Status.choices`   | Available choices (tuple).                               |
| `Post.Status.names`     | Names of the choices (class variables).                  |
| `Post.Status.labels`    | Human-readable names (2nd element of the tuple).         |
| `Post.Status.values`    | Actual values of the choices (1st element of the tuple). |

- Specify the field's `choices` parameter to limit the value.
- **Good practice:** Define choices **inside the model class**, allowing you to **easily reference** choice labels, values, or names.

### Adding a many-to-one relationship - `models.ForeignKey`

- **One author** (user) can create **many posts**.
- Can use the `User` model provided by the **Django authentication framework** (`django.contrib.auth` package).
- Use `AUTH_USER_MODEL` setting (points to `auth.models.User` by default) **when defining the foreign key** field.

  ```py
  from django.conf import settings  # Project's settings.

  class Post(models.Model):
      # Model fields
      ...
      author = models.ForeignKey(
          settings.AUTH_USER_MODEL,
          # `CASCADE` - Deleting a user will also delete his/her posts as well.
          on_delete=models.CASCADE,
          # Specifies the name of the reverse relationship, `user.blog_posts`.
          related_name="blog_posts"
      )
  ```

- Additional resources:
  - [Possible values for `on_delete`](https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ForeignKey.on_delete)
  - [Field types](https://docs.djangoproject.com/en/5.0/ref/models/fields/)

### Creating and applying migrations - `makemigrations` and `migrate`

- To create a migration for an app, named `blog`:
  ```bash
  python manage.py makemigrations blog
  ```
- A migration specifies **dependencies** on other migrations and **operations** to perform in the database.
- To get the **SQL** for a migration:
  ```bash
  $ python manage.py sqlmigrate blog 0001
  ```
- Django generates the **table names** by **combining** the **app name** and the **model name in lowercase**, `blog_post`.
- Define `Meta.db_table` attribute to **explicitly specify** the table name.
- Fields that **create an index by default**:
  - `SlugField`
  - `ForeignKey`
- To apply the **pending migrations** of all **activated apps** (`INSTALLED_APPS`):
  ```bash
  $ python manage.py migrate
  ```

## Creating an administration site for models

- Django has a **built-in admin site**. It is **built dynamically** by reading the **model metadata**.

### Creating a superuser - `createsuperuser`

- To create a user **to manage the admin site**.
  ```bash
  $ python manage.py createsuperuser
  ```

### The Django administration site

- Default URL - `http://<host>:<port>/admin/`

### Adding models to the administration site

```py
admin.site.register(Post)
```

- Django uses **different form widgets** for each type of field.

### Customizing how models are displayed

```py
# blog/admin.py

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]  # Search bar
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]  # User lookup widget
    date_hierarchy = "publish"  # Date breadcrumbs (below search bar)
    ordering = ["status", "publish"]  # Overrides the default sort order of the model.
    show_facets = admin.ShowFacets.ALWAYS  # Object counts for each filter.
```

- Model (`Post`) is registered in the site using a **custom class** that inherits from `ModelAdmin`.
- `show_facets` is introduced in **Django 5.0**.
- Additional resource: [Django admin site](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/)

## Working with QuerySets and managers (Django ORM)

- Django ORM **supports** MySQL, PostgreSQL, SQLite, Oracle, and MariaDB.
- `DATABASES` setting in `settings.py` defines the database used.
- Can implement **database routers** to create custom **data routing schemes** to work with **multiple databases**.
- Django ORM is based on **QuerySets** (SQL `SELECT`).
- **Filters** are limiting SQL clauses such as `WHERE` or `LIMIT`.
- Additional resource: [Model API reference](https://docs.djangoproject.com/en/5.0/ref/models/)

### Creating objects

```py
from django.contrib.auth.models import User
from blog.models import Post

# Ues `get()` to retrieve a single object.
# If no results, raise a `User.DoesNotExist`.
# If more than one result, raise a `User.MultipleObjectsReturned`.
user = User.objects.get(username="admin")

post = Post(title="Another post", slug="another-post", body="Post body.", author=user)
post.save()  # Save to database.

# Use `create()` to create the object and persist it to the database in
#   a single operation.
Post.objects.create(title="One more post", slug="one-more-post", body="Post body.", author=user)

# Use `get_or_create()` to fetch an object from the database or create it
#   if it's absent.
# Returns a tuple (object_retrieved, is_newly_created)
user2, created = User.objects.get_or_create(username="user2")
```

### Updating objects

```py
post.title = "New title"
post.save()
```

### Retrieving objects

- Each model has **at least one manager**.
- `<Model>.objects` is the default manager.
- Use `all()` to retrieve all objects from a table.
  ```py
  # This QuerySet has not been executed yet (lazy).
  all_posts = Post.objects.all()
  ```

### Filtering objects

- Use `filter()` to filter a QuerySet (SQL `WHERE`).
  ```py
  posts = Post.objects.filter(title="Who was Django Reinhardt?")
  print(posts.query)  # SQL generated
  ```

### Using field lookups

- QuerySet API provides multiple **lookup types**. (**CI** - case-insensitive)

  | Lookup type                           | Description                                                                        |
  | ------------------------------------- | ---------------------------------------------------------------------------------- |
  | `exact`,<br />`iexact` (CI)           | - Exact match (Default).                                                           |
  | `contains`,<br />`icontains` (CI)     | - SQL `LIKE`.<br />- E.g. `WHERE title LIKE '%Django%'`                            |
  | `in`                                  | - Lookup with a iterable (list, tuple, another QuerySet).<br />- SQL `IN`          |
  | `gt`, `gte`, `lt`, `lte`              | - Greater than, greater than or equal to, less than, less than or equal to lookup. |
  | `startswith`,<br />`istartswith` (CI) | - Starts-with lookup.<br />- SQL `LIKE`                                            |
  | `endswith`,<br />`iendswith` (CI)     | - Ends-with lookup.<br />- SQL `LIKE`                                              |

- Lookup types for `DateField` or `DateTimeField`:

  | Date lookup type       | Description                 |
  | ---------------------- | --------------------------- |
  | `date`                 | Exact date lookup.          |
  | `year`, `month`, `day` | Filter by year, month, day. |

- **Two underscores** (`__`) are used to define the lookup type.
- Examples:

  ```py
  # Exact match.
  Post.objects.filter(id__exact=1)
  Post.objects.filter(id=1)
  #   Case-insensitive version.
  Post.objects.filter(title__iexact="who was django reinhardt?")

  # SQL `LIKE`
  Post.objects.filter(title__contains="Django")
  #   Case-insensitive version
  Post.objects.filter(title__icontains="django")

  # Lookup with a iterable.
  Post.objects.filter(id__in=[1, 3])

  # Greater than lookup.
  Post.objects.filter(id__gt=3)
  # Greater than or equal to lookup.
  Post.objects.filter(id__gte=3)
  # Less than lookup.
  Post.objects.filter(id__lt=3)
  # Less than or equal to lookup.
  Post.objects.filter(id__lte=3)

  # Starts-with lookup.
  Post.objects.filter(title__istartswith="who")
  # Ends-with lookup.
  Post.objects.filter(title__iendswith="reinhardt?")

  # Exact date lookup.
  from datetime import date
  Post.objects.filter(publish__date=date(2024, 1, 31))

  # Filter by year.
  Post.objects.filter(publish__year=2024)
  # Filter by month.
  Post.objects.filter(publish__month=1)
  # Filter by day.
  Post.objects.filter(publish__day=1)

  # Chain additional lookups.
  Post.objects.filter(publish__date__gt=date(2024, 1, 1))

  # Lookup related object fields.
  Post.objects.filter(author__username="admin")
  #   Chain additional lookups for related fields.
  Post.objects.filter(author__username__startswith="ad")

  # Filter by multiple fields.
  Post.objects.filter(publish__year=2024, author__username="admin")
  ```

### Chaining filters

```py
Post.objects.filter(publish__year=2024) \
            .filter(author__username="admin")
```

### Excluding objects - `exclude()`

```py
Post.objects.filter(publish__year=2024) \
            .exclude(title__startswith="Why")
```

### Ordering objects - `order_by()`

```py
# Ascending order.
Post.objects.order_by("title")

# Descending order.
Post.objects.order_by("-title")

# Order by multiple fields.
Post.objects.order_by("author", "title")

# Use `?` to order randomly.
Post.objects.order_by("?")
```

### Limiting QuerySets (array-slicing)

```py
# SQL `LIMIT 5`
Post.objects.all()[:5]

# SQL `LIMIT 3 OFFSET 3`
Post.objects.all()[3:6]

# To retrieve a single object in random order.
Post.objects.order_by("?")[0]
```

### Counting objects - `count()`

```py
# SQL `SELECT COUNT(*)`
Post.objects.filter(id__lt=3).count()
```

### Checking if an object exists - `exists()`

```py
# To check if a QuerySet contains any results.
Post.objects.filter(title__startswith="Why").exists()
```

### Deleting objects - `delete()`

```py
post = Post.objects.get(id=1)
post.delete()
```

### Complex lookups with `Q` objects

- Field lookups using `filter()` are joined with a SQL `AND`.
- Use `Q` objects to build **complex queries**, such as queries with `OR`.
- `Q` object encapsulates **a collection of field lookups**.
- Can **compose statements** by combining `Q` objects with the `&`, `|`, and `^` operators.

  ```py
  from django.db.models import Q

  starts_who = Q(title__istartswith="who")
  starts_why = Q(title__istartswith="why")
  Post.objects.filter(starts_who | starts_why)
  ```

- Additional resource: [Q objects](https://docs.djangoproject.com/en/5.0/topics/db/queries/#complex-lookups-with-q-objects)

### When QuerySets are evaluated

- QuerySets are **only evaluated** when:
  - **Iterate** over them.
  - **Pickle** or cache them
  - Call `repr()` or `len()` on them
  - Call `list()` on them.
  - **Test** them in a statement, such as `bool()`, `or`, `and`, `if`

### More on QuerySets

- Additional resources:
  - [QuerySet API reference](https://docs.djangoproject.com/en/5.0/ref/models/querysets/)
  - [Making queries](https://docs.djangoproject.com/en/5.0/topics/db/queries/)

### Creating model managers - `models.Manager`

- `<Model>.objects` is the default manager. It retrieves all the objects.
- Can define **custom managers** to **filter** the objects to be retrieved.
- Two ways to add or customize managers:

  1. **Add methods** to an **existing** manager.
     - `Post.objects.my_manager()`
  2. Create a **new** manager by **modifying the initial QuerySet** - `super().get_queryset()`.

     - `Post.my_manager.all()`
     - **First manager** defined becomes the **default manager**.
     - Django will **not create** the `objects` manager if the model **defines another manager**. So, **define it explicitly** to keep it.

     ```py
     class PublishedManger(models.Manager):
         def get_queryset(self):
             return super().get_queryset().filter(status=Post.Status.PUBLISHED)

     class Post(models.Model):
         # Model fields.
         ...
         objects = models.Manager()  # Default manager.
         published = PublishedManager()  # Custom manager.
     ```

## Building list and detail views

- Three steps to build web pages:
  1. Create your application views.
  2. Define a URL pattern for each view.
  3. Create HTML templates to render the data generated by the views.

### Creating list and detail views

- `request` parameter is **required** by all views.
- Use **`render()` shortcut** to render the web page with the given **template** and the **context object**.

### Using the `get_object_or_404` shortcut

- Same as `<Model>.objects.get()` except it raises `Http404` exception if no object is found.

### Adding URL patterns for your views - `urlpatterns`

- URL patterns **map** URLs to views.
- **First**, create a `<app>/urls.py` for your app as it is **not created by default**.

  - `<parameter>` is captured as a **string**.
  - Use [**path converters**](https://docs.djangoproject.com/en/5.0/topics/http/urls/#path-converters) for matching.
    - `<int:year>` - Match and return an integer.
    - `<slug:post>` - Match a slug.

  ```py
  # blog/urls.py

  from django.urls import path
  from . import views

  app_name = "blog"  # App namespace

  urlpatterns = [
      # Post views
      path("", views.post_list, name="post_list"),
      # Use `<>` to capture values from the URL.
      path("<int:id>/", views.post_detail, name="post_detail"),
  ]
  ```

- Use `re_path()` to define **complex** URL patterns with **regular expressions**.
- Creating a `urls.py` for each application makes your apps reusable by other projects.
- **Next**, include the **app URL patterns** (`<app>/urls.py`) in the **project (main) URL patterns** (`<proj>/urls.py`).

  - Use `include()` to define the **app URLconf**.
  - [**URL namespaces**](https://docs.djangoproject.com/en/5.0/topics/http/urls/#url-namespaces) have to be **unique** across entire project.

  ```py
  # mysite/urls.py

  from django.contrib import admin
  from django.urls import path, include

  urlpatterns = [
      path("admin/", admin.site.urls),
      path("blog/", include("blog.urls", namespace="blog")),
  ]
  ```

## Creating templates for your views

- [Django template language reference](https://docs.djangoproject.com/en/5.0/ref/templates/language/)
- **File structure** for the templates inside the **app directory**:
  - `base.html` include the main HTML structure.
  - `list.html` and `detail.html` inherit from the `base.html`.
  ```
  templates/
      blog/
          base.html
          post/
              list.html
              detail.html
  ```
- Components that **control how data is displayed**:

  | Component                                 | Description                     |
  | ----------------------------------------- | ------------------------------- |
  | Template tags `{% tag %}`                 | - Control the rendering.        |
  | Template variables `{{ variable }}`       | - Get replaced with values.     |
  | Template filters `{{ variable\|filter }}` | - Modify variables for display. |

- Additional resource: [Built-in template tags and filters](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/)

### Creating a base template - `base.html`

- Template tags used:

  | Template tag        | Description                                                                                             |
  | ------------------- | ------------------------------------------------------------------------------------------------------- |
  | `{% load static %}` | - Loads the **`static` custom template tags**.<br />- Provided by the `django.contrib.staticfiles` app. |
  | `{% static %}`      | - To include static files.<br />- `<app>/static/` is the **default directory** for static files.        |
  | `{% block %}`       | - Templates that inherit from the `base.html` can fill in the block.                                    |

### Creating the post list template - `post/list.html`

- Template tags used:

  | Template tag    | Description                                                                                                    |
  | --------------- | -------------------------------------------------------------------------------------------------------------- |
  | `{% extends %}` | - To **inherit** from the `<app>/base.html`.                                                                   |
  | `{% url %}`     | - To **build URLs dynamically** by URLs name.<br />- `<a href="{% url "blog:post_detail" post.id %}">Link</a>` |

- Template filters used:
  - `truncatewords`
  - `linebreaks` - Converts newline (e.g. `\n`) into HTML line breaks (e.g. `<p>`).
- Can **concatenate** multiple template filters. Each filter will be applied to the output generated by the **preceding one**.
  ```django
  {{ post.body|truncatewords:30|linebreaks }}
  ```

## The request/response cycle

- **Basic reference** for how Django processes requests (**doesn't include middleware**, for the sake of simplicity).

  ![1-19-the-django-request-response-cycle](images/1-19-the-django-request-response-cycle.png)

## Management commands used in this chapter

- [`startproject`](#creating-your-first-project---django-admin-startproject)
- [`startapp`](#creating-an-application---startapp)
- [`migrate`](#applying-initial-database-migrations---migrate)
- [`makemigrations`, `sqlmigrate`](#creating-and-applying-migrations---makemigrations-and-migrate)
- [`runserver`](#running-the-development-server---runserver)
- [`createsuperuser`](#creating-a-superuser---createsuperuser)
- Additional resource: [Full list of available management commands](https://docs.djangoproject.com/en/5.0/ref/django-admin/)

# 2 Enhancing Your Blog and Adding Social Features

- Features to build:
  - Canonical URL for the model
  - SEO-friendly URL
  - Pagination
  - Class-based view
  - Send emails via SMTP
  - Share posts via email using `forms.Form`
  - Add comments using `forms.ModelForm`

## Functional overview

![2-1-diagram-of-functionalities-built-in-chapter-2](images/2-1-diagram-of-functionalities-built-in-chapter-2.png)

## Using canonical URLs for models - `get_absolute_url()`

- **Canonical URL** - The preferred/most representative/main URL for a resource.
- Implement `get_absolute_url()` **in models** to return the canonical URL.
- Use a **URL pattern name** (e.g. `blog:post_detail`) in `blog/urls.py` to build the canonical URL.
- Django has **different URL resolver functions** to build URLs dynamically, such as `django.urls.reverse()`.

  ```py
  from django.urls import reverse

  def get_absolute_url(self):
      return reverse(
          "blog:post_detail",  # URL name.
          args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
      )
  ```

- Additional resource: [URL's utility functions](https://docs.djangoproject.com/en/5.0/ref/urlresolvers/)

## Creating SEO-friendly URLs for posts

- Create a SEO-friendly URL using the `publish` date and `slug`, such as `/blog/2024/1/1/who-was-django-reinhardt/`.
- **Must ensure** that no post can be stored in the database with the same `publish` date and `slug`.

  - Define `slug` to be unique for the `publish` date.
  - Check for unique values **only against the date** (not the time).
  - `unique_for_date` is **not enforced at the database level**, so no database migration.
  - **However**, we will still **create a migration** and apply it since Django uses migrations **to keep track of all model changes**.

  ```py
  class Post(models.Model):
      slug = models.SlugField(
          max_length=250,
          unique_for_date="publish"
      )
  ```

## Adding pagination - `Paginator`

- Django has a built-in pagination class to manage paginated data easily by specifying the number of objects per page.

### Adding pagination to the post list view

```py
from django.core.paginator import Paginator

def post_list(request):
    post_list = Post.published.all()

    # Pagination with 3 posts per page.
    paginator = Paginator(post_list, 3)
    # Retrieve the HTTP `GET` parameter. (Default: 1st page)
    page_number = request.GET.get("page", 1)
    posts = paginator.page(page_number)  # `Page` object.

    ...
```

### Creating a pagination template - `pagination.html`

- A generic template (**reusable**) to display **pagination links**.
- The template **expects** to have a `Page` object (`page`) in the context.
- Use `{% include %}` to load the pagination template (e.g. `pagination.html`) into a page template (e.g. `blog/post/list.html`).

  - Use `with` to pass **additional context variables**.

  ```django
  ...

  {% block content %}
    ...
    {% include "pagination.html" with page=posts %}
  {% endblock content %}
  ```

### Handling pagination errors - `EmptyPage`, `PageNotAnInteger`

- `page` **query string parameter** could have wrong values:

  - Non-existing page numbers (out of range)
    - `Paginator` object throws an `EmptyPage` exception.
    - Can return the **last page** to handle it.
  - Not an integer -`Paginator` object throws an `PageNotAnInteger` exception.
    - Can return the **First page** to handle it.

  ```py
  from django.core.paginator import EmptyPage, PageNotAnInteger
  ...

  def post_list(request):
      ...
      try:
          posts = paginator.page(page_number)
      except EmptyPage:
          # If page_number is out of range get last page of results.
          posts = paginator.page(paginator.num_pages)
      except PageNotAnInteger:
          # If page_number is not an integer get the first page.
          posts = paginator.page(1)

      ...
  ```

## Building class-based views - `django.views.generic`

- **Alternative** to function-based views.
- Django provides **base view classes** (all inherit from `View`), which handles **HTTP method dispatching**.

### Why use class-based views

- **Organize code** related to **HTTP methods**, instead of using conditional branching.
- Use multiple inheritance (**mixins**) to create **reusable** view classes.

### Using a class-based view to list posts - `ListView`

- Create a class that **inherit** from `ListView`.

  ```py
  # Similar to the `post_list` view, except the exception handling is a bit different.
  class PostListView(ListView):
      """
      Alternative post list view.
      """
      # Alternatively, define `model = Post` and Django will built
      #   the generic `Post.objects.all()` QuerySet.
      queryset = Post.published.all()
      context_object_name = "posts"  # Default: `object_list`
      paginate_by = 3
      template_name = "blog/post/list.html"  # Default: `blog/post_list.html`
  ```

- To use the `PostListView` class in a URL pattern (`blog/urls.py`):

  ```py
  urlpatterns = [
      # path("", views.post_list, name="post_list"),
      path("", views.PostListView.as_view(), name="post_list"),
  ]
  ```

- `ListView` passes the `Page` object in a variable called `page_obj`.

  ```django
  ...

  {% block content %}
    ...
    {% include "pagination.html" with page=page_obj %}
  {% endblock content %}
  ```

- **Exception handling is different** - `ListView` returns `Http404` when the `page` query string parameter is invalid.
- **More** about class-based views in **Chapter 13**.
- Additional resource: [Introduction to class-based views](https://docs.djangoproject.com/en/5.0/topics/class-based-views/intro/)

## Recommending (sharing) posts by email

- To share posts via email:
  1. Create a **Django form** (`EmailPostForm`).
  2. Create a **view** (`post_share`) to **handle posted data** and **send email**.
  3. Add a URL pattern.
  4. Create a template to display the form.

### Creating forms with Django - `<app>/forms.py`

- Django has a **built-in forms framework**.
  - To define **form fields** (how they are **displayed**, how they **validate input**).
- Two **base classes** to build forms:

  1. `forms.Form`

     - Standard forms.
     - Each **field type** has a **default widget** (**can be overriden** with the `widget` attribute), such as `CharField` is rendered as an `<input type="text">`.

     ```py
     from django import forms

     class EmailPostForm(forms.Form):
         # * Form fields.
         # Use different field types to validate data.
         name = forms.CharField(max_length=25)
         email = forms.EmailField()
         to = forms.EmailField()
         # Optional field.
         comments = forms.CharField(required=False, widget=forms.Textarea)
     ```

  2. `ModelForm`

     - Forms that are tied to **model instances**.
     - **Form fields** can be **explicitly defined**, or automatically **generated from model fields**.

- Additional resource: [Field types](https://docs.djangoproject.com/en/5.0/ref/forms/fields/)

### Handling forms in views - `views.post_share()`

- Use the **same view** to:
  - **Display the initial form** (`GET` request)
    ```py
    form = EmailPostForm()
    ```
  - **Process the submitted data** (`POST` request).
    ```py
    if request.method == "POST":
        # Form was submitted.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            ...
    ```
- **Validation errors** can be obtained with `form.errors`.
- If the form **is invalid**, it is **rerendered**, including the data submitted (**validation errors** will be displayed).
  - `cleaned_data` **will contain** only the valid fields.
- If the form **is valid**, the validated data is retrieved with `form.cleaned_data`. Forms clean the data by **normalizing it to a consistent format**.
  - Can implement `clean_<field>()` or `clean()` **custom protocol** to customize the clean behavior.

### Sending emails with Django (SMTP)

- Settings for the **SMTP configuration**:
  - `EMAIL_HOST`
  - `EMAIL_PORT`
  - `EMAIL_HOST_USER`
  - `EMAIL_HOST_PASSWORD`
  - `EMAIL_USE_TLS`
  - `EMAIL_USE_SSL`

### Working with environment variables - `python-decouple`

- **Good practice:** Load the **SMTP credentials** from **environment variables**, and avoid embedding credentials in the source code.
- Use `python-decouple` to facilitate the **separation of configuration from code**.
  - **Simplify** the use of environment variables.
  - Create a `.env` file inside the **project's root directory**. It contains key-value pairs of environment variables.
- `DEFAULT_FROM_EMAIL` setting specify the **default sender**.
  - Can take any format valid in the chosen email sending protocol, such as `My Blog <your_account@gmai.com>`.
- To send emails **using your own domains**, considering **email services** such as **SendGrid** or **Amazon Simple Email Service (SES)**.
- `django-anymail` application **simplifies** the task of **adding email service providers**.
  - [Installation instructions](https://anymail.dev/en/stable/installation/)
  - [Supported email service providers](https://anymail.dev/en/stable/esps/)
- To write emails to the **console**.
  - Useful for testing your application without an SMTP server.
  ```py
  EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
  ```
- Additional resource: [Sending email](https://docs.djangoproject.com/en/5.0/topics/email/)

### Sending emails in views - `send_mail()`

```py
from django.core.mail import send_mail

def post_share(request: HttpRequest, post_id):
    ...
    sent = False  # True to display a success message.

    if request.method == "POST":
        ...
        if form.is_valid():
            ...

            # * Send email
            # To build a complete URL, including the HTTP schema and hostname.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            ...
            send_mail(
                subject=subject,
                message=message,
                from_email=None,  # Use `DEFAULT_FROM_EMAIL setting`.
                recipient_list=[cd["to"]],
            )
            sent = True
    ...
```

### Rendering forms in templates - `templates/blog/post/share.html`

- **Template tags** and **template variable** used:

  | Component          | Description                                                                                                                                                  |
  | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  | `{% if sent %}`    | - To **differentiate** whether to display the **form** or the **success message**.                                                                           |
  | `{{ form.as_p }}`  | - To render **form fields** using `<p>` (`as_p` is a **method**).<br />- Use `as_ul` to render as an `<ul>`.<br />- Use `as_table` to render as a `<table>`. |
  | `{% csrf_token %}` | - To add a hidden field with a token **to avoid CSRF attacks**.<br />- **By default**, Django checks for the CSRF token in all `POST` requests.              |

- To test the Django form validation, you can **skip the browser form validation** by:
  ```html
  <form method="post" novalidate>...</form>
  ```

## Creating a comment system

### Creating a model for comments

- **One** post can have **many** comments.
- `Comment` model has a **foreign key** to `Post` model. If the `related_name` attribute is **not specified** when defining the `models.ForeignKey()`, it **defaults to** `<model>_set`, such as `comment_set`.
- Additional resource: [Many-to-one relationship](https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_one/)

### Creating forms from models - `forms.ModelForm`

- Use `forms.ModelForm` and leverage on the `Comment` model **to build a form dynamically**.

  - Each **model field type** has a corresponding **default form field type**.
  - **Attributes of model fields** are taken into account for **form validation**.
  - **By default**, Django creates a form field for each field.

  ```py
  from .models import Comment

  class CommentForm(forms.ModelForm):
      class Meta:
          # Indicates which model to build the form.
          model = Comment
          # Defines which fields to include. Use `exclude` attribute
          #   to define which fields to exclude.
          fields = ["name", "email", "body"]
  ```

- Additional resource: [Creating forms from models](https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/)

### Handling ModelForms in views

- Add the comment form to the **post detail page**.
- Implement a **separate view** to handle the form submission.

  - Use `require_POST` decorator **to only allow POST requests** for this view. Django **throws an HTTP `405` (method not allowed) error** if you access it with other HTTP methods.
  - `<form_obj>.save()` is **not available** for `Form` instances.

  ```py
  from django.views.decorators.http import require_POST

  @require_POST
  def post_comment(request: HttpRequest, post_id):
      post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
      comment = None

      # A comment was posted.
      form = CommentForm(request.POST)
      if form.is_valid():
          # Create a Comment object without saving it to the database.
          comment = form.save(commit=False)
          # Assign the post to the comment.
          comment.post = post
          # Save the comment to the database.
          comment.save()

      return render(
          request,
          "blog/post/comment.html",
          {"post": post, "form": form, "comment": comment},
      )
  ```

### Creating templates for the comment form

- Comment form template - `templates/blog/post/includes/comment_form.html`
- Use in **two places**:
  1. `templates/blog/post/detail.html`
  2. `templates/blog/post/comment.html`
- Use `{% include %}` to include the comment form template in the two other templates.

### Adding comments to the post detail view

- Add the **list of comments** and the **comment form**.

### Adding comments to the post detail template

```django
{% block content %}
  ...

  {% comment %}
  - `comments.count` is an ORM method.
  - `with` tag assigns a value to a new variable that will be available until
    the `endwith` tag.
  {% endcomment %}
  {% with total_comments=comments.count %}
    <h2>{{ total_comments }} comment{{ total_comments|pluralize }}</h2>
  {% endwith %}

  {% for comment in comments %}
    <div class="comment">
      <p class="info">
        Comment {{ forloop.counter }} by {{ comment.name }}
        {{ comment.created }}
      </p>
      {{ comment.body|linebreaks }}
    </div>
  {% empty %}
    <p>There are no comments.</p>
  {% endfor %}

  ...
{% endblock content %}
```

- `{% with %}` is useful for **avoiding** hitting the database or accessing expensive methods **multiple times**.

### Using simplified templates for form rendering

- Use **custom HTML** for rendering form fields.
  - Access each form field directly - `{{ form.email }}`
  - **Iterate** through the form fields - `{% for field in form %}`
- Notable **`field` attributes**:
  - `{{ field.errors }}`
  - `{{ field.label_tag }}` - Render the HTML label.
  - `{{ field }}` - Render the actual field.
  - `{{ field.help_text|safe }}`
- **Django 5.0** introduces **field groups** and **field group templates**.
  - Field groups **simplify** the rendering of labels, widgets, help texts, and field errors.
- Use custom HTML **to reposition the form fields**.

  - `as_field_group` method renders each field including help text and errors. It uses the [`django/forms/field.html`](https://github.com/django/django/blob/stable/5.0.x/django/forms/templates/django/forms/field.html) template **by default**.
  - Can create **custom field templates** and reuse them by adding the `template_name` attribute to any form field.
  - Additional resource: [Reusable form templates](https://docs.djangoproject.com/en/5.0/topics/forms/#reusable-field-group-templates)

  ```django
  <h2>Add a new comment</h2>
  <form action="{% url "blog:post_comment" post.id %}" method="post">
    <div class="left">{{ form.name.as_field_group }}</div>
    <div class="left">{{ form.email.as_field_group }}</div>
    {{ form.body.as_field_group }}

    {% csrf_token %}
    <p>
      <input type="submit" value="Add comment">
    </p>
  </form>
  ```
