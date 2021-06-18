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

const submit = function(){
    const data = {
        checkListName : document.getElementById('checkListName').innerHTML,
        itemList : []
    }
    checkList = document.getElementsByClassName('checkList-item')
    
    for(let i = 0; i < checkList.length; i++){
        if(checkList[i].checked && !checkList[i].disabled){
            data.itemList.push(checkList[i].name)
        }
    }


    $.ajax({
            type: 'POST',
            url: '/api/v1/saveCheckList',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data)
        }).done(function(arg){
            if(arg.status == 'true') window.location.href = '/index'
            else alert("아마도 실패?")
        }).fail(function (error) {
            alert(JSON.stringify(error))
        })
}