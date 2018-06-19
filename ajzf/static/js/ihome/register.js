function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
}

function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    $.get("/api/smscode", {mobile:mobile, code:imageCode, codeId:imageCodeId}, 
        function(data){
            if (0 != data.errno) {
                $("#image-code-err span").html(data.errmsg); 
                $("#image-code-err").show();
                if (2 == data.errno || 3 == data.errno) {
                    generateImageCode();
                }
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
            }   
            else {
                var $time = $(".phonecode-a");
                var duration = 60;
                var intervalid = setInterval(function(){
                    $time.html(duration + "秒"); 
                    if(duration === 1){
                        clearInterval(intervalid);
                        $time.html('获取验证码'); 
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }
                    duration = duration - 1;
                }, 1000, 60); 
            }
    }, 'json'); 
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $("#submit").on('click', function(e){
        e.preventDefault();
        var mobile = $("#mobile").val();
        // phoneCode = $("#phonecode").val();
        var passwd = $("#password").val();
        var passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return false;
        } 
        // if (!phoneCode) {
        //     $("#phone-code-err span").html("请填写短信验证码！");
        //     $("#phone-code-err").show();
        //     return false;
        // }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return false;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return false;
        }
        $.ajax({
            url: '/auth/register/',
            type: 'POST',
            data: {'mobile': mobile, 'password': passwd, 'password2': passwd2},
            dataType: 'json',
            success: function (data) {
                if (data.code==200) {
                    alert(data.msg);
                    location.href = '/auth/login/'
                }
                else if (data.code==1002) {
                    $("#mobile-err span").html("请填写正确的手机号！");
                    $("#mobile-err").show();
                }
                else if (data.code==1003) {
                    $("#password2-err span").html("两次密码不一致!");
                    $("#password2-err").show();
                }
                else if (data.code==1004) {
                    alert(data.msg)
                }else {
                    alert(data.msg)
                }
            },
            error: function () {
                alert('连接服务器失败，请稍后再试~')
            }
        })
    });
});