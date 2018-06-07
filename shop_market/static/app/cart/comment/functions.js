function addCart(goods_id) {
    csrf = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: '/xf/addCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if (msg.code == 200) {
                $('#num_' + goods_id).text(msg.c_num)
            } else {
                alert(msg.msg);
                location.href = '/user/login/'
            }
        },
        error: function (msg) {
            console.log('连接服务器失败~')
        }
    })
}

function subCart(goods_id) {
    csrf = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: '/xf/subCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if (msg.code == 200) {
                $('#num_' + goods_id).text(msg.c_num)
            } else if (msg.code == 400) {
                alert(msg.msg);
            } else {
                alert(msg.msg);
                location.href = '/user/login/'
            }
        },
        error: function (msg) {
            console.log('连接服务器失败~')
        }
    })
}
// $(function () {
//     function goodsNum(goods_id) {
//     csrf = $("input[name=csrfmiddlewaretoken]").val();
//     $.ajax({
//         url: '/xf/goodsNum/',
//         type: 'POST',
//         data: {'goods_id': goods_id},
//         dataType: 'json',
//         headers: {'X-CSRFToken': csrf},
//         success: function (msg) {
//             if (msg.code == 200) {
//                 $('#num_' + goods_id).text(msg.c_num)
//             }
//         },
//         error: function (msg) {
//             console.log('连接服务器失败~')
//         }
//     })
// }
// });

$(function () {
    function isChoose() {
        var csrf = $("input[name=csrfmiddlewaretoken]").val();
        var current_li = $(this);
        var cart_id = current_li.parents("li").attr("cartid");
        $.ajax({
            url: '/xf/changeCartStatus/',
            type: 'POST',
            data: {'cart_id': cart_id},
            dataType: 'json',
            headers: {'X-CSRFToken': csrf},
            success: function (data) {
                if (data.code == 200) {
                    if (data.check) {
                        $('#num_' + cart_id).html("√");
                    } else {
                        $('#num_' + cart_id).html("");
                    }
                    current_li.attr("is_select", data["check"]);
                    $('#totalPrice').text(data.total_price);
                }
            },
            error: function (msg) {
                console.log('连接服务器失败~')
            }
        })
    }

    $('.is_choose').on('click', isChoose);
    $('#all_select').on('click', function () {
        var not_selects = [];
        var selects = [];
        var isselect;
        var count=0;
        $(".is_choose").each(function () {
            count += 1;
            if ($(this).attr("is_select").toLowerCase() == "false"){
                // 将未选中添加到指定集合中
                not_selects.push($(this).parents("li").attr("cartid"));
            }else{
                selects.push($(this).parents("li").attr("cartid"));
            }
            if (selects.length < count ){
                isselect = 1;
                $('#choose_all').html("√")
            }
            else {
                isselect = 2
                $('#choose_all').html("")
            }
            var csrf = $("input[name=csrfmiddlewaretoken]").val();
            var current_li = $(this);
            var cart_id = current_li.parents("li").attr("cartid");
            $.ajax({
                url: '/xf/changeCartStatus/',
                type: 'POST',
                data: {'cart_id': cart_id, 'isselect': isselect},
                dataType: 'json',
                headers: {'X-CSRFToken': csrf},
                success: function (data) {
                    if (data.code == 200) {
                        if (data.check) {
                            $('#num_' + cart_id).html("√");
                        } else {
                            $('#num_' + cart_id).html("");
                        }
                        current_li.attr("is_select", data["check"]);
                        $('#totalPrice').text(data.total_price);
                    }
                },
                error: function (msg) {
                    console.log('连接服务器失败~')
                }
            })

        })
    })
});
