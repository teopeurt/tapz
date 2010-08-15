Highcharts.setOptions({
    colors: ['#2d3736', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4']
});
var chart;
$(document).ready(function() {
   chart = new Highcharts.Chart({
      chart: {
         renderTo: 'container',
         defaultSeriesType: 'line',
         margin: [50, 25, 60, 60]
      },
      credits: {
         enabled: false
      },
      legend: {
         enabled: false
      },
      title: {
         text: 'Pages loaded at a certain speed'
      },
      subtitle: {
         text: 'Left side is good. Right side is bad.'
      },
      xAxis: {
         labels: {
             rotation: 90,
             y: 30
         },
         categories: [
            '0ms', 
            '500ms', 
            '1000ms', 
            '1500ms', 
            '2000ms', 
            '2500ms', 
            '3000ms', 
            '3500ms', 
            '4000ms', 
            '4500ms', 
            '5000ms', 
            '5500ms',
            '6000ms',
            '6500ms',
            '7000ms',
            '7500ms',
            '8000ms',
            '8500ms',
            '9000ms',
            '9500ms',
            '10000ms'
         ]
      },
      yAxis: {
         min: 0,
         title: {
            text: 'Pages loaded (in thousands)'
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
            borderWidth: 0
         }
      },
           series: [{
         name: 'Errors',
         data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4, 49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4]
   
      }]
   });
   
   
});