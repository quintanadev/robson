$(document).ready(async function () {
  theme = $("html").attr("data-bs-theme");
  color_theme = theme == "dark" ? "#40475D" : "#F5F6F8";

  var init_chart_nps_total = function () {
    var options = {
      series: [0],
      chart: {
        height: 260,
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
              formatter: function (val) {
                return parseFloat(val);
              },
              fontSize: "32px"
            }
          }
        },
      },
      colors: ['#1ABC9C'],
      labels: ['NPS'],
    };

    var chart_nps = new ApexCharts(document.querySelector("#chart-nps"), options);
    chart_nps.render();
    return chart_nps;
  };

  var init_chart_nps = function () {
    var options = {
      chart: {
        height: 70,
        type: 'bar',
        stacked: true,
        sparkline: {
          enabled: true
        }
      },
      plotOptions: {
        bar: {
          horizontal: true,
          barHeight: '20%',
          colors: {
            backgroundBarColors: [color_theme]
          }
        },
      },
      stroke: {
        width: 0,
      },
      series: [{
        name: '-----',
        data: [0]
      }],
      title: {
        floating: true,
        offsetX: -10,
        offsetY: 5,
        text: '-----'
      },
      subtitle: {
        floating: true,
        align: 'right',
        offsetY: 0,
        text: '0%',
        style: {
          fontSize: '20px'
        }
      },
      tooltip: {
        enabled: false
      },
      yaxis: {
        max: 100
      },
      fill: {
        type: 'gradient',
        gradient: {
          inverseColors: false,
          gradientToColors: ['#6078ea']
        }
      },
    };

    var chart_nps_promotor = new ApexCharts(document.querySelector("#chart-nps-promotor"), options);
    var chart_nps_neutro = new ApexCharts(document.querySelector("#chart-nps-neutro"), options);
    var chart_nps_detrator = new ApexCharts(document.querySelector("#chart-nps-detrator"), options);
    chart_nps_promotor.render();
    chart_nps_neutro.render();
    chart_nps_detrator.render();
    return { "chart_promotor": chart_nps_promotor, "chart_neutro": chart_nps_neutro, "chart_detrator": chart_nps_detrator };
  };

  chart_nps = init_chart_nps();
  chart_nps_total = init_chart_nps_total();

  (whatsapp_update = async () => {
    var next_update = 60000;
    if (res.result) {
      $.NotificationApp.send('Notificação: ', res.message, 'top-right', res.result, 3e3, 1, 'slide');
      next_update = 15000;
    } else {
      await fetch('http://127.0.0.1:8000/api/inbound/whatsapp/', {
        method: 'GET',
      }).then((result) => {
        result.json().then((res) => {
          $('.date-update').html(res.updated);
          $('.tickets-fila').html(res.data.waiting);
          $('.tempo-fila').html(res.data.maxQueueTime);
          $('.tempo-resposta').html(res.data.maxFirstResponseTime);
          $('.agentes-online').html(res.data.online);
          $('.agentes-pausa').html(res.data.pause);
          $('.agentes-invisiveis').html(res.data.invisible);

          $('#tickets-em-atendimento').html(res.data.inAttendance);
          $('#tickets-fechados').html(res.data.closed);
          $('#tickets-por-agente').html(res.data.ticketsPerAttendant);
          $('#minimo-por-agente').html(res.data.minOpenedTickets);
          $('#maximo-por-agente').html(res.data.maxOpenedTickets);
          $('#negocios').html(res.data.ticketsNegocio);
          $('#percentual-conversao').html(res.data.percentualConversao);
          $('#tempo-atendimento').html(res.data.avgAttendanceTime.substr(0, 8));
          $('#tempo-resposta').html(res.data.avgResponseTime.substr(0, 8));
          $('#tempo-espera').html(res.data.avgWaitTime.substr(0, 8));
          $('#tempo-primeira-resposta').html(res.data.avgFirstResponseTime.substr(0, 8));

          if (parseFloat(res.data.ticketsPerAttendant) > 10) {
            $('#tickets-por-agente').parent().removeClass("text-success");
            $('#tickets-por-agente').parent().addClass("text-danger");
          } else {
            $('#tickets-por-agente').parent().removeClass("text-danger");
            $('#tickets-por-agente').parent().addClass("text-success");
          }

          if (parseInt(res.data.avgAttendanceTime.substr(0, 8).replace(/\:/g, "")) > 5000) {
            $('#tempo-atendimento').parent().removeClass("text-success");
            $('#tempo-atendimento').parent().addClass("text-danger");
          } else {
            $('#tempo-atendimento').parent().removeClass("text-danger");
            $('#tempo-atendimento').parent().addClass("text-success");
          }

          if (parseInt(res.data.avgResponseTime.substr(0, 8).replace(/\:/g, "")) > 500) {
            $('#tempo-resposta').parent().removeClass("text-success");
            $('#tempo-resposta').parent().addClass("text-danger");
          } else {
            $('#tempo-resposta').parent().removeClass("text-danger");
            $('#tempo-resposta').parent().addClass("text-success");
          }

          if (parseInt(res.data.avgWaitTime.substr(0, 8).replace(/\:/g, "")) > 100) {
            $('#tempo-espera').parent().removeClass("text-success");
            $('#tempo-espera').parent().addClass("text-danger");
          } else {
            $('#tempo-espera').parent().removeClass("text-danger");
            $('#tempo-espera').parent().addClass("text-success");
          }

          if (parseInt(res.data.avgFirstResponseTime.substr(0, 8).replace(/\:/g, "")) > 20) {
            $('#tempo-primeira-resposta').parent().removeClass("text-success");
            $('#tempo-primeira-resposta').parent().addClass("text-danger");
          } else {
            $('#tempo-primeira-resposta').parent().removeClass("text-danger");
            $('#tempo-primeira-resposta').parent().addClass("text-success");
          }

          var colors_nps = ['#F1556C']
          chart_nps_total.updateSeries([parseFloat(res.data.npsTotal)]);
          if (parseFloat(res.data.npsTotal) <= 0) {
            colors_nps = ['#F1556C'];
            zona = "Zona Crítica";
          } else if (parseFloat(res.data.npsTotal) <= 50) {
            colors_nps = ['#F1556C'];
            zona = "Zona de Aperfeiçoamento";
          } else if (parseFloat(res.data.npsTotal) <= 75) {
            colors_nps = ['#FCCF31'];
            zona = "Zona de Qualidade";
          } else if (parseFloat(res.data.npsTotal) <= 90) {
            colors_nps = ['#1ABC9C'];
            zona = "Zona de Excelência";
          } else {
            colors_nps = ['#1ABC9C'];
            zona = "Zona de Encantamento";
          }
          chart_nps_total.updateOptions({ colors: colors_nps });
          $("#nps-zona").html(zona);

          theme = $("html").attr("data-bs-theme");
          color_theme = theme == "dark" ? "#40475D" : "#F5F6F8";

          chart_nps.chart_promotor.updateOptions({
            xaxis: {
              categories: ['Promotor']
            },
            title: {
              text: "Promotor"
            },
            series: [{
              data: [parseFloat(res.data.npsPromotor)]
            }],
            subtitle: {
              text: res.data.npsPromotor + "%"
            },
            colors: ['#1ABC9C'],
            fill: {
              gradient: {
                gradientToColors: ["#1ABC9C"]
              }
            },
            plotOptions: {
              bar: {
                colors: {
                  backgroundBarColors: [color_theme]
                }
              },
            },
          });

          chart_nps.chart_neutro.updateOptions({
            xaxis: {
              categories: ['Neutro']
            },
            title: {
              text: "Neutro"
            },
            series: [{
              data: [parseFloat(res.data.npsNeutro)]
            }],
            subtitle: {
              text: res.data.npsNeutro + "%"
            },
            colors: ['#FCCF31'],
            fill: {
              gradient: {
                gradientToColors: ["#FCCF31"]
              }
            },
            plotOptions: {
              bar: {
                colors: {
                  backgroundBarColors: [color_theme]
                }
              },
            },
          });

          chart_nps.chart_detrator.updateOptions({
            xaxis: {
              categories: ['Detrator']
            },
            title: {
              text: "Detrator"
            },
            series: [{
              data: [parseFloat(res.data.npsDetrator)]
            }],
            subtitle: {
              text: res.data.npsDetrator + "%"
            },
            colors: ['#F1556C'],
            fill: {
              gradient: {
                gradientToColors: ["#F1556C"]
              }
            },
            plotOptions: {
              bar: {
                colors: {
                  backgroundBarColors: [color_theme]
                }
              },
            },
          });
        });
      });
    }
    setTimeout(whatsapp_update, next_update);
  })();
});