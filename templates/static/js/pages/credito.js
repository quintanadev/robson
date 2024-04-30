$(document).ready(async function () {

  var init_chart_ns = async function () {
    var options = {
      series: [0],
      chart: {
        height: 340,
        type: 'radialBar',
      },
      plotOptions: {
        radialBar: {
          hollow: {
            size: '75%',
          },
          dataLabels: {
            name: {
              offsetY: -10,
            },
            value: {
              fontSize: "32px"
            }
          }
        },
      },
      colors: ['#1ABC9C'],
      labels: ['Nível de Serviço'],
    };

    var chart_ns = new ApexCharts(document.querySelector("#chart-ns"), options);
    chart_ns.render();
    return chart_ns;
  };

  let seriesData = []
  let seriesDataNs = []
  let seriesCategories = []

  var init_chart_hour = async function () {
    for (let i = 0; i < 14; i++) {
      seriesData.push(0);
      seriesDataNs.push(0);
      seriesCategories.push("-");
    }

    var options = {
      chart: {
        height: 295,
        type: 'line',
        padding: {
          right: 0,
          left: 0
        },
        stacked: false,
        toolbar: {
          show: false
        }
      },
      stroke: {
        width: [0, 4],
        curve: 'smooth'
      },
      plotOptions: {
        bar: {
          columnWidth: '50%'
        }
      },
      dataLabels: {
        enabled: true,
        formatter: function (val, x) {
          if (x.seriesIndex == 1) {
            return val + "%";
          }
          return val;
        }
      },
      colors: ['#6658dd', '#f672a7'],
      series: [{
        name: 'Propostas',
        type: 'column',
        data: seriesData
      }, {
        name: 'Nível de Serviço',
        type: 'line',
        data: seriesDataNs
      }],
      fill: {
        opacity: [0.85, 1],
        gradient: {
          inverseColors: false,
          shade: 'light',
          type: "vertical",
          opacityFrom: 0.85,
          opacityTo: 0.55,
          stops: [0, 100, 100, 100]
        }
      },
      labels: seriesCategories,
      markers: {
        size: 0
      },
      legend: {
        offsetY: 7,
      },
      xaxis: {
        categories: seriesCategories,
      },
      yaxis: {
        min: 0,
        max: 20,
      },
      grid: {
        borderColor: '#f1f3fa',
        padding: {
          bottom: 10
        }
      }
    }

    var chart_hour = new ApexCharts(document.querySelector("#chart-hour"), options);
    chart_hour.render();
    return chart_hour;
  };

  chart_ns = await init_chart_ns();
  chart_hour = await init_chart_hour();

  (credito_update = async () => {
    var next_update = 60000 * 10;
    await fetch('http://127.0.0.1:8000/api/inbound/credito/', {
      method: 'GET',
    }).then((result) => {
      result.json().then((res) => {
        if (res.result) {
          $.NotificationApp.send('Notificação: ', res.message, 'top-right', res.result, 3e3, 1, 'slide');
          next_update = 15000;
        } else {
          $('#data-atualizacao').html(res.updated);

          var colors_ns = parseFloat(res.data.nivel_servico) >= 90 ? ['#1ABC9C'] : ['#F1556C'];
          chart_ns.updateSeries([parseFloat(res.data.nivel_servico)]);
          chart_ns.updateOptions({
            colors: colors_ns
          });

          seriesCategories = []
          seriesData = []
          seriesDataNs = []
          JSON.parse(res.data.json_hora).forEach(el => {
            seriesCategories.push(el['hora']);
            seriesData.push(parseInt(el['propostas']));
            seriesDataNs.push(parseFloat(el['ns']));
          });
          chart_hour.updateSeries([{ data: seriesData }, { data: seriesDataNs }]);
          chart_hour.updateOptions({
            xaxis: {
              categories: seriesCategories
            },
            yaxis: [{
              min: 0,
              max: Math.max(Math.max(...seriesData)) * 1.5
            }, {
              opposite: true,
              min: 0,
              max: 100,
              axisBorder: {
                show: false
              },
              axisTicks: {
                show: false,
              },
              labels: {
                show: false,
                formatter: function (val) {
                  return val + "%";
                }
              }
            }]
          })

          // console.log(JSON.parse(res.data.json_hora));
        }
      });
    });
    setTimeout(credito_update, next_update);
  })();
});