from django.conf.urls import patterns, include, url
from django.contrib import admin
import main.views as v

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'htMusicBot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index$',v.index),
    url(r'^usercsv$',v.userCsv),
    url(r'^check$',v.check),
    url(r'^facebook_auth/?$',v.MyChatBotView.as_view()),
)
