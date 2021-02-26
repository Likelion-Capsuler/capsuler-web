$(document).ready(function(){

  $(".img-area ").click(function(){
    $("#input_vid").click();
  })

   var fileTarget = $('#input_vid');

    fileTarget.on('change', function(){

      var imgBox = $('.img-area');

      if (window.FileReader){

        // 형식에 맞지 않는 파일 거르기
        if (!$(this)[0].files[0].type.match(/video\//)) {
          alert('동영상만 입력 가능합니다!');
          return;
        }

        // 썸네일 넣기
        imgBox.empty();
        var reader = new FileReader();
        reader.onload = function(e){
            var src = e.target.result;
            var vType = src.split(';')[0].split('/').reverse()[0];
            imgBox.append('<video class="img-thumb"><source src="'+src+'" type="video/webm"; /></video>');
        }
        reader.readAsDataURL($(this)[0].files[0]);

        // 파일명 추출
        var filename = $(this)[0].files[0].name;
        $('#img_name > span').text(filename);

      } else {
          // Old IE 파일명 추출
          var filename = $(this).val().split('/').pop().split('\\').pop();

          // 이건 뭔지 모르겠는걸!
          $(this)[0].select();
          $(this)[0].blur();

          var imgSrc = document.selection.createRange().text;
          imgBox.append('<img src="imgs/ico-video.png" class="img-icon"><span>화면을 눌러 동영상을 업로드해 주세요<span>');

          var img = imgBox.find('img');
          img[0].style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(enable='true',sizingMethod='scale',src=\""+imgSrc+"\")";

      }

    });

});
