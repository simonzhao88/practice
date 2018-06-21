function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(function () {
   $('#authentication').on('click', function (e) {
       e.preventDefault();
       $('#form-auth').ajaxSubmit({
           url: '/api/authentication/',
           dataType: 'json',
           type: 'patch',
           success: function (data) {
               if (data.code==200){
                   showSuccessMsg();
                   $('#authentication').hide()
               }else if(data.code==1010){
                   $('.error-msg').css('display', 'block')
               }else if(data.code==1012){
                   $('.popup_con p').text(data.msg);
                   showSuccessMsg();
               }
           },
           error: function () {
               alert('连接服务器失败，请稍后再试~')
           }
       })
   });
    $.get('/api/authentication/', function (data) {
        if (data.code==200) {
            if (data.data.id_name){
                var id_card = data.data.id_card.substr(0,5)
                    + '********' + data.data.id_card.substr(5);
                $('#real-name').val(data.data.id_name);
                $('#id-card').val(id_card);
                $('#real-name').attr('readonly', 'readonly');
                $('#id-card').attr('readonly', 'readonly');
                $('#authentication').hide()
            }
        }
    })
});