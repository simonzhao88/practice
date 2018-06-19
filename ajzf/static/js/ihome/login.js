function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $("#submit").on('click', function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return false;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return false;
        }
        $.ajax({
            url: '/auth/login/',
            type: 'POST',
            data: {'mobile': mobile, 'password': passwd},
            dataType: 'json',
            success: function (data) {
                if (data.code==200) {
                    location.href = '/mine/'
                }
                else if(data.code==1006) {
                    $("#mobile-err span").html("用户不存在~");
                    $("#mobile-err").show();
                }
                else if (data.code==1007) {
                    $("#password-err span").html('用户名或密码错误~');
                    $("#password-err").show();
                }else {
                    alert('请填写完所有参数~')
                }
            },
            error: function () {
                alert('连接服务器失败，请稍后再试~')
            }
        })
    });
});