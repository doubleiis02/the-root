
Chart.defaults.global.legend.labels.usePointStyle = true;


var ctx = document.getElementById("pieChart");
var pieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Completely Understand', 'Mostly Understand', 'Don\'t Fully Understand', 'Don\'t Understand'],
        datasets: [{
            backgroundColor: [
                "#553AFA",
                "#954ECD",
                "#56B0D2",
                "#3AB74E"
            ],
            data: [30, 37, 13, 20]
        } ]
    },
    options: {
        legend: {
            position: 'right'
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