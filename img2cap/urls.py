from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'img2cap'

urlpatterns = [
    path('', views.index, name='index'),
    path('cap_list/', views.cap_list, name="cap_list"),
    path('upload_eng/', views.upload_eng, name='upload_eng'),
    path('upload_kor/', views.upload_kor, name='upload_kor'),
    path('upload_vid/', views.upload_vid, name='upload_vid'),
    path('predict_eng/', views.predict_eng, name='predict_eng'),
    path('predict_kor/', views.predict_kor, name='predict_kor'),
    path('predict_vid/', views.predict_vid, name='predict_vid'),
    path('delete_img/<str:file_name>/', views.delete_img, name='delete_img'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
