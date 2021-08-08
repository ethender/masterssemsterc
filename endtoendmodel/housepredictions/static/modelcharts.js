

function finalResult(high,med,low){
    google.charts.load('current', {'packages':['bar']});
    google.charts.setOnLoadCallback(drawChart); 

    function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Model', 'High', 'Medium', 'Low'],
          ['Predict', high, med, low],
        ]);
      
        var options = {
          chart: {
            title: 'House Price',
            subtitle: 'Mostly price can be paid maximum for this house.',
          }
        };
      
        var chart = new google.charts.Bar(document.getElementById('bellcurve'));
      
        chart.draw(data, google.charts.Bar.convertOptions(options));
      }
}

function finalResultOtherModel(arr){
    google.charts.load('current', {'packages':['bar']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable(arr);
        var options = {
          chart: {
            title: 'House Price Suggested By Other Models.',
            subtitle: 'Mostly price can be paid maximum for this house. Suggested by various models.',
          }
        };

        var chart = new google.charts.Bar(document.getElementById('otherModelsGraph'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }
}


