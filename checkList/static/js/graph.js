
let itemData = []



const makeGraph = function(ctx, chartData){
    const myChart = new Chart(ctx, chartData)
    return myChart
}
const barChart = function(myChart, chartData, ctx){
    myChart.destroy()
    chartData.type = 'bar'
    const newChart = new Chart(ctx, chartData)
    return newChart
}
const lineChart = function(myChart, chartData, ctx){
    myChart.destroy()
    chartData.type = 'line'
    const newChart = new Chart(ctx, chartData)
    return newChart
}

const chartData = {
    type: 'bar', 
    data: { 
        labels: ['mon', 'tue', 'wen', 'thr', 'fri', 'sat', 'sun'], 
        datasets: [
            { 
                label: '# of Votes', 
                data: [10, 19, 3, 5, 2, 3, 5],
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)', 
                borderWidth: 1 
            },
            {
                label: '# of Votes', 
                data: [12, 22, 8, 1, 11, 2, 10],
                backgroundColor:   'rgba(255, 255, 255, 0.2)',
                borderColor:  'rgba(54, 162, 235, 1)', 
                borderWidth: 1  
            },
            {
                label: '# of Votes', 
                data: [7, 20, 5, 4, 18, 1, 1],
                backgroundColor:   'rgba(255, 255, 255, 0.2)',
                borderColor:  'rgba(90, 255, 50, 1)', 
                borderWidth: 1  
            }
        ]
    }, 
    options: {
        tooltips: {
            callbacks: {
                label: function(t, d) {
                    const checkListName = d.datasets[t.datasetIndex].label
                    const itemDate = d.labels[t.index]
                    const value = t.value
                    let string = ""
                    for(i of itemData){
                        if(i.name == checkListName){
                            for(j of i.items){
                                if(j.date == itemDate){
                                    string = `${checkListName} 체크한 항목 :${j.items.toString()} (${itemDate})`
                                }
                            }
                        }
                    }

                    return string
                }
            }
        }
    } 
}



const saveItemData = function(data){
    itemData = []
    index = 0
    for(i of data){
        itemData.push({
            'name' : i.name,
            'items' : []
        })
        for(j of i.data){
            itemData[index].items.push({
                'date' : j.date,
                'items' : j.items
            })
        }
        index = index + 1
    }
    console.log(itemData)
}

const getDataLabels = function(differ){
    const today = new Date()
    const year = today.getFullYear()
    const month = today.getMonth() + 1
    const date = today.getDate()
    const monthData = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if(date - differ < 1){
        if(month - 1 < 1){
            return `${year-1}.${12}.${monthData[month-1] + (date - differ)}.`
        }
        else{
            return `${year}.${month - 1}.${monthData[month-1] + (date - differ)}.`
        }
    }
    else{
        return `${year}.${month}.${date - differ}.`
    }
}

const changeData = function(chartData, newData, myChart){

    const tempData = []
    const ctx = document.getElementById('myChart')

    chartData.data.labels =  [getDataLabels(6), getDataLabels(5), getDataLabels(4), getDataLabels(3), getDataLabels(2), getDataLabels(1), getDataLabels(0)]
    chartData.data.datasets = []

    rgbSet = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(90, 255, 50, 1)','rgba(255, 255, 0, 0.9)']
    for(index in newData){
        tempData.push({
            labelName : newData[index].name,
            data : [0, 0, 0, 0, 0, 0, 0],
        })
        for(data of newData[index].data){
            for(let i = 0; i < 7; i++){
                console.log(chartData.data.labels[i], data.date)
                if(chartData.data.labels[i] == data.date){
                    tempData[index].data[i] = data.value
                }
            }
        }
        chartData.data.datasets.push(
            {
                label: tempData[index].labelName, 
                data: tempData[index].data,
                borderColor: rgbSet[index],
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                borderWidth: 1  
            }
        )
    }
    myChart.destroy()
    const newChart = new Chart(ctx, chartData)
    console.log(chartData)
    return newChart
}

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
        checkListName : []
    }
    checkList = document.getElementsByClassName('checkList-item')
    for(let i = 0; i < checkList.length; i++){
        if(checkList[i].checked){
            data.checkListName.push(checkList[i].name)
        }
    }
    $.ajax({
            type: 'POST',
            url: '/api/v1/graph',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data)
        }).done(function(arg){
            if(arg.status == 'true'){
                myChart = changeData(chartData, arg.newData, myChart)
                saveItemData(arg.newData)
            }
            else alert("아마도 실패?")
        }).fail(function (error) {
            alert(JSON.stringify(error))
        })
}



$('#lineG').on('click', function(){
    myChart = lineChart(myChart, chartData, ctx)
})
$('#barG').on('click', function(){
    myChart = barChart(myChart, chartData, ctx)
})

const checkList = document.getElementsByClassName('checkList-item')
const ctx = document.getElementById('myChart')
let myChart
if(checkList.length != 0){
    const firstData = {
        checkListName : []
    }
    firstData.checkListName.push(checkList[0].name)
    myChart = makeGraph(ctx, chartData)
    $.ajax({
        type: 'POST',
        url: '/api/v1/graph',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(firstData)
    }).done(function(arg){
        if(arg.status == 'true'){
            myChart = changeData(chartData, arg.newData, myChart)
            saveItemData(arg.newData)
        }
        else alert("아마도 실패?")
    }).fail(function (error) {
        alert(JSON.stringify(error))
    })
}


