$(document).ready(function(){
    $(".auth-warn").show();
});

$(function () {
    $.get('/api/authentication/', function (data) {
        if (data.code==200) {
            if (data.data.id_name) {
                $('.auth-warn').hide()
            }
        }
    });
    $.get('/api/house/', function (result) {
        if (result.code==200) {
            var house = '';
            for (var i=0; i<result.data.length;i++){
                house += '<a href="/house/detail?house_id=' + result.data[i].id +
                    '">' + '<div class="house-title"><h3>房屋ID:' + result.data[i].id +
                    '—— 房屋标题:' + result.data[i].title + '</h3></div><div class="house-content">' +
                    '<img src="/static/' + result.data[i].image + '"><div class="house-text"><ul><li>位于：'+
                    result.data[i].area + '</li><li>价格：' + result.data[i].price + '</li><li>发布时间：' +
                    result.data[i].create_time + '</li></ul></div></div></a></li>'
            }
            $('#houses-list').append(house)
        }else if (result.code == 1013) {
            $('.new-house').hide()
        }
    })
});
