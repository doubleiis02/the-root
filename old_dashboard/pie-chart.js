
Chart.defaults.global.legend.labels.usePointStyle = true;


var ctx = document.getElementById("pieChart");
var pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Completely Understand', 'Somewhat Understand', 'Moderately Understand', 'Don\'t Understand'],
        datasets: [{
            backgroundColor: [
                "#aebafa",
                "#7d64ef",
                "#9981db",
                "#b683ea"
            ],
            data: [64, 11, 13, 12]
        } ]
    },
    options: {
        legend: {
            position: 'bottom'
        },
        tooltips: {
            enabled: false
        },
        plugins: {
            datalabels: {
                formatter: (value, ctx) => {
                    let sum = 0;
                    let dataArr = ctx.chart.data.datasets[0].data;
                    dataArr.map(data => {
                        sum += data;
                    });
                    let percentage = (value*100 / sum)+"%";
                    return percentage;
                },
                color: 'white',
            }
        }
    }
});