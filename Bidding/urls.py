from django.conf.urls import include, url
from django.contrib import admin
from accounts.views import UserCreate
from Items.views import ItemCreate,bidOnItemView

BASE_URL = r'^bidengine/webapi/bidservices/'


urlpatterns = [
    # Examples:
    # url(r'^$', 'Bidding.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # name Convention:
    # <Model> - <create/all/top/<verb> >

    url(r'^admin/', include(admin.site.urls)),
    url(BASE_URL+'user',UserCreate.as_view({'post': 'post'}),name='user-create'),
    url(BASE_URL+'biditem',ItemCreate.as_view({'post': 'post'}),name='item-create'),
    url(BASE_URL+'tbiditems',ItemCreate.as_view({'get': 'get_all'}),name='item-all'),

    url(BASE_URL+'biditem/(?P<itemid>[0-9]+)',
        ItemCreate.as_view({'get': 'get'}),name='item-get'),

    url(BASE_URL+'bidder/biditem/(?P<itemid>[0-9]+)',
        bidOnItemView.as_view({'get': 'get_topbidders'}),name='biditem-top'),

    url(BASE_URL+'biditem/(?P<itemid>[0-9]+)',
        bidOnItemView.as_view({'post': 'post'}),name='biditem-create'),

]
