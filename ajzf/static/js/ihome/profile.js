function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    $('#uploadimage').on('click', function (e) {
        e.preventDefault();
        var options = {
            url: '/api/profile/',
            type: 'patch',
            dataType: 'json',
            success: function (data) {
                if (data.code == 200) {
                    $('#user-avatar').attr("src", '/static/' + data.image_url);
                } else {
                    alert(data.msg)
                }
            },
            error: function () {
                alert('连接服务器失败，请稍后再试~')
            }
        };
        $("#form-avatar").ajaxSubmit(options);
    });
    $('#uploadname').on('click', function (e) {
        e.preventDefault();
        var options = {
            url: '/api/profile/',
            type: 'patch',
            dataType: 'json',
            success: function (data) {
                if (data.code == 200) {
                    showSuccessMsg()
                } else if(data.code==1009){
                    $('.error-msg').css('display', 'block')
                }else {
                    alert(data.msg)
                }
            },
            error: function () {
                alert('连接服务器失败，请稍后再试~')
            }
        };
        $("#form-name").ajaxSubmit(options);
    });
});

