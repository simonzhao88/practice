function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    });
    $(".book-house").show();
});
$(function () {
   var house_id = parseInt(decodeQuery().house_id);
   $.get('/api/house/detail/',{house_id: house_id}, function (result) {
        if (result.code==200){
            var image_html = '';
            for (var i=0; i<result.data.images.length; i++){
                image_html += '<li class="swiper-slide"><img src="/static/' +
                    result.data.images[i] + '"></li>'
            }
            $('.swiper-wrapper').append(image_html);
            $('.house-price span').text(result.data.price);
            $('.house-title').text(result.data.title);
            $('.landlord-pic img').attr('src', '/static/' + result.data.user_avatar);
            $('.landlord-name span').text(result.data.user_name);
            $('#address').text(result.data.address);
            $('#house-area h3').text('出租' + result.data.room_count + '间');
            $('#house-area p:first').text('房屋面积:' + result.data.acreage + '平米');
            $('#house-area p:last-child').text('房屋户型:' + result.data.unit);
            $('#people-num h3').text('宜住:' + result.data.capacity + '人');
            $('#beds p').text(result.data.beds);
            $('.house-info-list li:first-child span').text(result.data.deposit);
            $('.house-info-list li:nth-child(2) span').text(result.data.min_days);
            if (result.data.max_days==0){
                var max_day = '无限制';
            }else {
                max_day = result.data.max_days
            }
            $('.house-info-list li:last-child span').text(max_day);
            var facility = '';
            for (var j=0;j<result.data.facilities.length; j++){
                facility += '<li><span class="' + result.data.facilities[j].css +
                    '"></span>' + result.data.facilities[j].name + '</li>'
            }
            $('.house-facility-list').append(facility);
            $('.book-house').attr('href', '/house/booking?house_id=' + house_id)

        }else {
            alert('无此房屋信息，请查验后再查询~')
        }
});
});
