function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


const register = {
    init : function(){
        const _this = this;
        $('#login').on('click', function(){
            _this.login()
        })
    },
    register : function(){
        const data = {
            userId : $('#userId').val(),
            userPassword : $('#userPassword').val(),
            userName : $('#userName').val()
        }
        $.ajax({
            type: 'POST',
            url: '/api/v1/register',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data)
        }).done(function(arg){
            if(arg.status == 'true'){
                alert("회원가입에 성공하였습니다.")
                window.location.href = '/'
            }
            else if (arg.status == 'false'){
                alert("회원가입에에 실패하였습니다.")
                window.location.href = '/register'
            }           
        }).fail(function (error) {
            alert(JSON.stringify(error))
        })
    }
}

register.init()