# dirrss feed generation module

## Setup

### Existing django project

If you already have a django project ready, clone this repository into your project and skip right to the *settings* section.

### New django project

- install [django](https://www.djangoproject.com/) from your favourite package repository
- `cd` to your desired destination path
- [create a django project](https://docs.djangoproject.com/en/dev/intro/tutorial01/) to host the dirrss app
- `cd` into your newly created project and clone dirrss with `git clone https://github.com/niklasfi/dirrss.git`

### settings.py

For dirrss to work properly, a few settings in your `<project_name>/settings.py` have to be adjusted:

- **`INSTALLED_APPS`** dirrss needs the sites app. Add `django.contrib.sites` and `dirrss` to your `INSTALLED_APPS`.
- **`MEDIA_URL`** configure a media url. This is the path clients direct requests at to download media files. A typical value is `/media/`
- **`MEDIA_ROOT`** configure the media root. This is the file system location at which your media files are located. A typical value is `os.path.join(BASE_DIR, 'media')`
- **`DIRRSS_MEDIA_URL`** path under which the media files to be served by dirrss are located. A typical value is `MEDIA_URL + 'dirrss/'`.
- **`DIRRSS_MEDIA_ROOT`** filesystem location at which the media files to be served by dirrss can be found. A typical value is `os.path.join(MEDIA_ROOT, 'dirrss')`

- **`SITE_ID`** after you have completed the step *sites setup* make sure to set `SITE_ID` to the primary key of the site you want to use.

### Create media directory

Create the directory specified in the `DIRRSS_MEDIA_ROOT` setting. If you are using [radioman](https://github.com/niklasfi/radioman.git) to create your media files, configure its destinationPath to be the same as `DIRRSS_MEDIA_ROOT`.

### urls.py

Delegate calls to `/dirrss` to the dirrss app. Import `include` with

    from django.conf.urls import include

and add the line

    url(r'^dirrss/', include('dirrss.urls')),

to your urlpatterns in `<project_name>/urls.py`. If you want to use django's built in static file hosting, also add

    urlpatterns += static(settings.DIRRSS_MEDIA_URL, document_root=settings.DIRRSS_MEDIA_ROOT)

to the file. For this to work, it may be necessary, first import static with

    from django.conf.urls.static import static

In total, a minimal `urls.py` may look something like this

    from django.conf.urls import url, include
    from django.contrib import admin

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^dirrss/', include('dirrss.urls'))
    ] + static(settings.DIRRSS_MEDIA_URL, document_root=settings.DIRRSS_MEDIA_ROOT)


Of course, if you want the path to call dirrss to be something else, feel free to change it to your liking.

### Sites setup

Create a django site to be used by dirrss to create absolute links to its media files. There are multiple ways to do so. You can use the admin site, for example. In this guide we are using the django shell.

Open the django shell with `python manage.py shell`. In the shell execute an adjusted version of the following script. Set `domain` and `name` to appropriate values for your applications. If you want to host dirrss on a public server, you likely want `domain` and `name` to be the server's fully qualified domain name (e.g. `example.com`). If you only want to host dirrss locally, you can leave `domain` and `name` as they are. They will point to the local server available trough `python manage.py runserver`.

    domain = 'localhost:8000'
    name = 'localhost:8000'
    from django.contrib.sites.models import Site
    s = Site.objects.create(domain=domain, name=name)
    print "SITE_ID = {}".format(s.pk)

Finally, tell the django project to use your site by adding the printed site id to your `<project_name>/settings.py` file.

### You're done

Start your local webserver with `python manage.py runserver` and visit `http://localhost:8000/dirrss/` or whatever url you have previously configures.
