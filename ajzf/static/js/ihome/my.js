function logout() {
    $.get("/auth/logout/", function(data){
            location.href = "/index/";
    })
}

$(document).ready(function(){
    $.getJSON('/api/mine/', function (data) {
        if (data.code==200) {
            $('#user-avatar').attr('src', '/static/' + data.data.avatar);
            $('#user-mobile').text(data.data.phone);
            $('#user-name').text(data.data.name);
        }
    })
});