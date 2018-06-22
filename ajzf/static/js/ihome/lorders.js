//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

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

$(document).ready(function () {
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

    function showModal() {
        $(".order-accept").on("click", function () {
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-accept").attr("order-id", orderId);
            $('#accept-modal').modal('show');
        });
        $(".order-reject").on("click", function () {
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-reject").attr("order-id", orderId);
            $('#reject-modal').modal('show')
        });
    }

    $.get('/api/customer/order/', function (result) {
        if (result.code == 200) {
            var order_html = template('orders-list-tmpl', {orders: result.orders});
            $('.orders-list').html(order_html);
            showModal();
        }
    });

});
$(function () {
    $('.modal-accept').on('click', function () {
        var order_id = $(this).attr('order-id');
        var status = 'WAIT_PAYMENT';
        $.ajax({
            url: '/api/accept/order/',
            data: {order_id: order_id, status:status},
            dataType: 'json',
            type: 'patch',
            success: function (result) {
                if (result.code == 200) {
                    $('#accept-modal').modal('hide');
                    $('li[order-id=\"'+ order_id +'\"] .order-operate').hide();
                }else {
                }
                $('.popup p').text(result.msg);
                showSuccessMsg()
            },
            error:function () {
                alert('服务器繁忙，请稍后再试~')
            }
        })
    });
    $('.modal-reject').on('click', function () {
        var order_id = $(this).attr('order-id');
        var reject_reason = $('#reject-reason').val();
        var status = 'REJECTED';
        $.ajax({
            url: '/api/accept/order/',
            data: {order_id: order_id, status:status, reject_reason:reject_reason},
            dataType: 'json',
            type: 'patch',
            success: function (result) {
                if (result.code == 200) {
                    $('#reject-modal').modal('hide');
                    $('li[order-id=\"'+ order_id +'\"] .order-operate').hide();
                }else {
                }
                $('.popup p').text(result.msg);
                showSuccessMsg()
            },
            error:function () {
                alert('服务器繁忙，请稍后再试~')
            }
        })
    })
});