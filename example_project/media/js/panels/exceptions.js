var chart;
$(document).ready(function() {
   chart = new Highcharts.Chart({
      chart: {
         renderTo: 'container',
         defaultSeriesType: 'column'
      },
      title: {
         text: 'Monthly Average Rainfall'
      },
      subtitle: {
         text: 'Source: WorldClimate.com'
      },
      xAxis: {
         categories: [
            'Jan', 
            'Feb', 
            'Mar', 
            'Apr', 
            'May', 
            'Jun', 
            'Jul', 
            'Aug', 
            'Sep', 
            'Oct', 
            'Nov', 
            'Dec'
         ]
      },
      yAxis: {
         min: 0,
         title: {
            text: 'Rainfall (mm)'
         }
      },
      legend: {
         layout: 'vertical',
         backgroundColor: '#FFFFFF',
         align: 'left',
         verticalAlign: 'top',
         x: 100,
         y: 70
      },
      tooltip: {
         formatter: function() {
            return ''+
               this.x +': '+ this.y +' mm';
         }
      },
      plotOptions: {
         column: {
            pointPadding: 0.2,
            borderWidth: 0
         }
      },
           series: [{
         name: 'Tokyo',
         data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
   
      }]
   });
   
   
});