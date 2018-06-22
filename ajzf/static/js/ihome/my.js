function logout() {
    $.ajax({
        url:"/auth/logout/",
        type: 'delete',
        success: function(relust){
            if (relust.code==200){
                location.href = "/house/index/";
            }

    }
    })
}

$(document).ready(function(){
    $.getJSON('/api/mine/', function (data) {
        if (data.code==200) {
            if (data.data.avatar) {
                $('#user-avatar').attr('src', '/static/' + data.data.avatar)
            }
            $('#user-mobile').text(data.data.phone);
            $('#user-name').text(data.data.name);
        }
    })
});