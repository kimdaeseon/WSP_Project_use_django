
chartData = {
    type: 'bar', 
    data: { 
        labels: ['mon', 'tue', 'wen', 'thr', 'fri', 'sat', 'sun'], 
        datasets: [{ label: '# of Votes', data: [10, 19, 3, 5, 2, 3, 5],
        backgroundColor: 'rgba(255, 255, 255, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)', 
        borderWidth: 1 
    },
    {
        label: '# of Votes', data: [12, 22, 8, 1, 11, 2, 10],
        backgroundColor:   'rgba(255, 255, 255, 0.2)',
        borderColor:  'rgba(54, 162, 235, 1)', 
        borderWidth: 1  
    }]}, 
    options: {
        lengend:{
            display:true
        }
    } 
}
const barChart = function(){
    var ctx = document.getElementById('myChart')
    chartData.type = 'bar'
    myChart = new Chart(ctx, chartData)
}
const lineChart = function(){
    var ctx = document.getElementById('myChart')
    chartData.type = 'line'
    mychar = new Chart(ctx, chartData)
}
