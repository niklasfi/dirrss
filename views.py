# -*- coding: utf-8 -*-

import mimetypes
# Create your views here.
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.utils import feedgenerator

dirrss_path = settings.DIRRSS_MEDIA_ROOT
dirrss_url = settings.DIRRSS_MEDIA_URL

def index(request):
    folders = [f for f in os.listdir(dirrss_path.encode('utf-8')) if os.path.isdir(os.path.join(dirrss_path, f.decode('utf-8')).encode('utf-8')) and (len(f) == 0 or f[0] != ".")]
    folders.sort()
    return render_to_response('dirrss/index.html', {"folders": folders})

class File:
    def __init__(self, filename, folder):
        filename = filename.decode('utf-8')
        folder = folder.decode('utf-8')

        self.filename = filename
        self.absolute_path = os.path.join(dirrss_path, folder, filename)
        self.absolute_url = os.path.join(dirrss_url, folder, filename)

        self.stat = os.stat(self.absolute_path.encode('utf-8'))
        self.length = self.stat.st_size
        self.ctime = datetime.fromtimestamp(self.stat.st_ctime)
        self.mtime = datetime.fromtimestamp(self.stat.st_mtime)
        self.mime = mimetypes.guess_type(self.absolute_path)[0]

    def get_absolute_url(self):
        return self.absolute_url

class FolderFeed(Feed):
    feed_type = feedgenerator.Rss201rev2Feed

    def get_object(self, request, folder):
        return folder

    def title(self, folder):
        return folder

    def link(self, folder):
        return u"" + reverse('dirrss_feed', args=[folder])

    def description(self, folder):
        return u""

    def items(self, folder):
        sub = os.path.join(dirrss_path, folder)
        try:
            all_files = os.listdir(sub.encode('utf-8'))
            files = [File(f, folder.encode('utf-8')) for f in all_files]
        except OSError:
            raise Http404
        files = [f for f in files if datetime.now() - f.mtime > timedelta(minutes=1)]
        files.sort(key=lambda f: f.ctime, reverse=True)
        return files

    def item_updatedate(self, item):
        return item.ctime
    def item_title(self, item):
        return item.filename
    def item_link(self, item):
        return item.get_absolute_url()
    def item_description(self, item):
        return u""
    #def item_enclosure(self, item):
    #	return feedgenerator.Enclosure(item.absolute_url, item.length, item.mime)

    def item_enclosure_url(self, item):
        return 'http://' + Site.objects.get_current().domain + item.absolute_url

    def item_enclosure_length(self, item):
        return item.length

    def item_enclosure_mime_type(self, item):
        return 'audio/mpeg' #'item.mime

    #def item_pubdate(self, item):
    #	return item.ctime
