Highcharts.setOptions({
    colors: ['#2d3736', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4']
});
var chart;
var chartOptions = {
    chart: {
        renderTo: 'chart',
        defaultSeriesType: 'line',
        margin: [50, 25, 25, 60]
        },
    credits: {
        enabled: false
        },
    legend: {
        enabled: false
        },
    title: {
        text: 'Error Frequency'
        },
    subtitle: {
        text: 'Last Month'
        },
    xAxis: {
        labels: {
            enabled: false
            },
        categories: []
        },
    yAxis: {
        min: 0,
        title: {
            text: 'Number of Errors'
            }
        },
    tooltip: {
        formatter: function() {
            return ''+
                this.x +': '+ this.y +' errors';
            }
        },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            groupPadding: 0,
            borderWidth: 0
            }
        },
    series: [{
        name: 'Errors',
        data: []
        }]
    };

$(document).ready(function() {
   chart = new Highcharts.Chart(chartOptions);
});