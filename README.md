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

  | Template tag        | Description                                                                                      |
  | ------------------- | ------------------------------------------------------------------------------------------------ |
  | `{% load static %}` | - Loads the **`static` template tags**.<br />- Provided by the `django.contrib.staticfiles` app. |
  | `{% static %}`      | - To include static files.<br />- `<app>/static/` is the **default directory** for static files. |
  | `{% block %}`       | - Templates that inherit from the `base.html` can fill in the block.                             |

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
  ```
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
