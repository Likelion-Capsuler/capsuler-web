from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .img2cap_func import printCaption, printKorCaption, find_nouns, printVidCaption
from .translate import translator


# main page
def index(request):
    return render(request, 'img2cap/main.html', {})

# caption select page
def cap_list(request):
    return render(request, 'img2cap/cap_list.html', {})


############# image caption #############


### 영어
# upload image page
def upload_eng(request):
    return render(request, 'img2cap/upload_eng.html', {})


# predict eng-cap
def predict_eng(request):

    if 'img_uploaded' not in request.FILES:
        return render(request, 'img2cap/upload_eng.html', {'error': 1})

    uploaded_file = request.FILES['img_uploaded']
    target_lang = request.POST["lang"]


    # 이미지 저장
    fs = FileSystemStorage()
    uploaded_filename = fs.save(uploaded_file.name, uploaded_file)
    uploaded_file_url = fs.url(uploaded_filename) # "/media/~~~.jpg"

    # 영어 캡션 생성
    result_eng = printCaption(settings.MEDIA_ROOT_URL + uploaded_file_url)

    # 번역
    result_translate = translator(result_eng, target_lang)

    context = {
        'uploaded_file_url' : uploaded_file_url,
        'uploaded_file_name' : uploaded_filename,
        'result_eng' : result_eng,
        'result_translate' : result_translate,
        'target_lang' : target_lang,
    }

    return render(request, 'img2cap/result_eng.html', context)




### 한국어
# upload image page for kor-cap
def upload_kor(request):
    return render(request, 'img2cap/upload_kor.html', {})


# predict kor-cap
def predict_kor(request):

    if 'img_uploaded' not in request.FILES:
        return render(request, 'img2cap/upload_kor.html', {'error': 1})

    uploaded_file = request.FILES['img_uploaded']

    # 이미지 저장
    fs = FileSystemStorage()
    uploaded_filename = fs.save(uploaded_file.name, uploaded_file)
    uploaded_file_url = fs.url(uploaded_filename) # "/media/~~~.jpg"

    # 한국어 생성
    result_kor = printKorCaption(settings.MEDIA_ROOT_URL + uploaded_file_url)
    print("kor->>>", result_kor)
    hashtags = find_nouns(result_kor)
    print("hash->>>", hashtags)

    context = {
        'uploaded_file_url' : uploaded_file_url,
        'uploaded_file_name' : uploaded_filename,
        'result_kor' : result_kor,
        'hashtags' : hashtags,
    }

    return render(request, 'img2cap/result_kor.html', context)



# delete storage image & return to home
def delete_img(request, file_name):

    fs = FileSystemStorage()
    fs.delete(file_name)

    return redirect('img2cap:cap_list')


############# video caption #############

# upload video page
def upload_vid(request):
    return render(request, 'img2cap/upload_vid.html', {})


# predict video page
def predict_vid(request):

    if 'vid_uploaded' not in request.FILES:
        return render(request, 'img2cap/upload_vid.html', {'error': 1})

    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    uploaded_vid = request.FILES['vid_uploaded']

    fs = FileSystemStorage()
    uploaded_vidname = fs.save(uploaded_vid.name, uploaded_vid)
    uploaded_vid_url = fs.url(uploaded_vidname)

    predict_result_vid = printVidCaption(settings.MEDIA_ROOT_URL + uploaded_vid_url)

    context = {
        'uploaded_vid_url': uploaded_vid_url,
       'uploaded_vid_name': uploaded_vidname,
       'predict_result_vid' : predict_result_vid,
    }

    return render(request, 'img2cap/result_vid.html', context)
