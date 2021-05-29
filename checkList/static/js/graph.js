
const chartData = {
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
    options: {} 
}
const ctx = document.getElementById('myChart')

const makeGraph = function(ctx, chartData){
    const myChart = new Chart(ctx, chartData)
    return myChart
}
const barChart = function(myChart, chartData, ctx){
    myChart.destroy()
    chartData.type = 'bar'
    newChart = new Chart(ctx, chartData)
    return newChart
}
const lineChart = function(myChart, chartData, ctx){
    myChart.destroy()
    chartData.type = 'line'
    newChart = new Chart(ctx, chartData)
    return newChart
}
let myChart = makeGraph(ctx, chartData)
$('#lineG').on('click', function(){
    myChart = lineChart(myChart, chartData, ctx)
})
$('#barG').on('click', function(){
    myChart = barChart(myChart, chartData, ctx)
})
