$(function(){

    initTopSwiper();

    initMenuSwiper();

})


function initTopSwiper(){

    var swiper = new Swiper("#topSwiper", {
        loop: true,
        pagination:".swiper-pagination",
        autoloop: 4000,
        autoplay:2500,
        speed: 2000,
        autoplayDisableOnInteraction : false,
    })
}


function initMenuSwiper(){

    var swiper = new Swiper("#swiperMenu", {
        slidesPerView: 3
    })
}