/*$(function () {

    $("#alipay").click(function () {

        var order_id = $(this).attr("orderid");

        console.log(order_id);
    //    调用支付宝支付，不小心就支付成功了
    //    想集成哪种支付就去相应的官网去认证  （企业，个人营业执照）    蚂蚁金服开放平台     Ping++
        $.getJSON("/axf/changeorderstatus/", {"status":"1","order_id":order_id}, function (data) {
            console.log(data);

            if (data["status"] == "200"){
                window.open("/axf/mine/", target="_self");
            }
        })
    })

})
*/
$(function () {

    $("#alipay").on('click', function (e) {

        var order_id = $(e.target).attr("orderid");
        var csrf = $("input[name=csrfmiddlewaretoken]").val();
        console.log(order_id);
        $.ajax({
             url: '/xf/changeOrderStatus/',
            type: 'POST',
            data: {'order_id': order_id},
            dataType: 'json',
            headers: {'X-CSRFToken': csrf},
            success: function (data) {
                if (data.code == 200) {
                    location.href = '/xf/mine/'
                }
            },
            error: function (msg) {
                console.log('连接服务器失败~')
            }
        })

    })

})
