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

const login = {
    init : function(){
        const _this = this;
        _this.keydown()
        $('#login').on('click', function(){
            _this.login()
        })
    },
    login : function(){
        const data = {
            userId : $('#userId').val(),
            userPassword : $('#userPassword').val()
        }
        $.ajax({
            type: 'POST',
            url: '/api/v1/login',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data)
        }).done(function(arg){
            if(arg.loginstatus == 'true'){
                alert("로그인에 성공하였습니다.")
                window.location.href = '/index'
            }
            else if (arg.loginstatus == 'false'){
                console.log(arg)
                alert("로그인에 실패하였습니다.")
                window.location.href = '/'
            }           
        }).fail(function (error) {
            alert(JSON.stringify(error))
        })
    },
    keydown : function(){
        const _this = this
        document.addEventListener('keydown', function(e){
            const keyCode = e.keyCode;
            if(keyCode == 13){ // Enter key
                _this.login()
            }
        })
    }
}

login.init()