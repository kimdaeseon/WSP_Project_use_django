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


const addItem = function(){
    let string = document.getElementById('itemList').innerHTML
    const numberOfItem = document.getElementById('numberOfItem').innerHTML
    document.getElementById('itemList').innerHTML = string + `<br>항목 ${parseInt(numberOfItem)+1} : <input type="text" name="checkList${numberOfItem}" id="checkList${numberOfItem}"><br>`
    document.getElementById('numberOfItem').innerHTML = parseInt(numberOfItem) + 1
}

const deleteItem = function(){
    let string = document.getElementById('itemList').innerHTML
    const numberOfItem = document.getElementById('numberOfItem').innerHTML
    if(numberOfItem >= 1){
        const splitString = string.split('<br><br>')
        splitString.pop()
        console.log(splitString)
        const replaceString = splitString.map( element => element.replace("<br>", ""));
        console.log(replaceString)
        string = ""
        for(let i = 0; i < replaceString.length; i++){
            string = string + '<br>' + replaceString[i] + '<br>'
        }
        document.getElementById('itemList').innerHTML = string
        document.getElementById('numberOfItem').innerHTML = parseInt(numberOfItem) - 1
    }
    else return 
}

const submit = function(){
    numberOfItem = parseInt(document.getElementById('numberOfItem').innerHTML)
    const temp = []
    for(let i = 0; i < numberOfItem; i++){
        temp.push($(`#checkList${i}`).val())
    }
    data = {
        title : $('#checkListName').val(),
        data : temp
    }
    $.ajax({
            type: 'POST',
            url: '/api/v1/makeCheckList',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data)
        }).done(function(arg){
            if(arg.status == 'true') window.location.href = '/index'
            else alert("체크리스트 생성에 실패하였습니다.")
        }).fail(function (error) {
            alert(JSON.stringify(error))
        })
}