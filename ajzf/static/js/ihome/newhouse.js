function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
});
function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 3000)
    });
}
$(function () {
    $.get('/house/area_facility/', function (data) {
        if (data.code==200) {
            var area_str = '';
            for (var i = 0; i < data.areas.length; i++) {
                area_option = '<option value=' + data.areas[i].id +
                    '>' + data.areas[i].name + '</option>';
                area_str += area_option;
            }
            $('#area-id').html(area_str);
            var facility_li = '';
            for (var j=0; j< data.facilitys.length; j++) {
                facility_li += '<li><div class="checkbox"><label>' +
                    '<input type="checkbox" name="facility" value=' + data.facilitys[j].id +
                    '>' + data.facilitys[j].name + '</label></div></li>';
            }
            $('.house-facility-list').html(facility_li)
        }
    });
    $('#publish').on('click', function (e) {
        e.preventDefault();
        getfacilitys();
        $('#form-house-info').ajaxSubmit({
            url: '/api/house/',
            dataType: 'json',
            type: 'post',
            success: function (data) {
                if (data.code==200) {
                    $('.popup_con').text('添加房源成功，请上传房源图片~');
                    showSuccessMsg();
                    $('#form-house-info').hide();
                    $('#house-id').val(data.house_id);
                    $('#form-house-image').css('display', 'block')
                }else if (data.code==2001){
                    $('.popup_con').text(data.msg);
                    showSuccessMsg()
                }else {
                    $('.popup_con').text(data.msg);
                    showSuccessMsg()
                }
            },
            error: function () {
                alert('服务器繁忙，请稍后再试~')
            }
        })
    });
    function getfacilitys(){
    var obj = document.getElementsByName("facility");
    var check_val = [];
    for(var k in obj){
        if(obj[k].checked)
            check_val.push(obj[k].value);
    }
    $('#facility_li').val(check_val)
};
    $('#upload').on('click', function (e) {
        e.preventDefault();
        $('#form-house-image').ajaxSubmit({
            url: '/api/house/image/',
            dataType: 'json',
            type: 'post',
            success: function (result) {
                if (result.code==200) {
                    location.href = '/house/myhouse/'
                }else {
                    alert('上传失败，请重试~~')
                }
            },
            error: function () {
                alert('服务器繁忙，请稍后再试~')
            }
        })
    })
});