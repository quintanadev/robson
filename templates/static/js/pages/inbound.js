$(document).ready(async function () {
  var next_slide = function () {
    if ($("#slide-kpis").hasClass("d-active")) {
      $("#slide-kpis").addClass("fadeOutLeft animated").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
        $(this).removeClass("fadeOutLeft animated d-active");
        $(this).addClass("d-none");

        $("#slide-skills").removeClass("d-none");
        $("#slide-skills").addClass("fadeInRight animated d-active").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
          $(this).removeClass("fadeInRight animated");
        });
      });
    } else if ($("#slide-skills").hasClass("d-active")) {
      $("#slide-skills").addClass("fadeOutLeft animated").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
        $(this).removeClass("fadeOutLeft animated d-active");
        $(this).addClass("d-none");

        $("#slide-dispositions").removeClass("d-none");
        $("#slide-dispositions").addClass("fadeInRight animated d-active").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
          $(this).removeClass("fadeInRight animated");
        });
      });
    } else if ($("#slide-dispositions").hasClass("d-active")) {
      $("#slide-dispositions").addClass("fadeOutLeft animated").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
        $(this).removeClass("fadeOutLeft animated d-active");
        $(this).addClass("d-none");

        $("#slide-kpis").removeClass("d-none");
        $("#slide-kpis").addClass("fadeInRight animated d-active").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
          $(this).removeClass("fadeInRight animated");
        });
      });
    };
  };

  var slide = null
  $(".play-slide").click(function () {
    if ($(this).children("i").hasClass("fe-play")) {
      slide = setInterval(function () {
        next_slide();
      }, 30000);
    } else {
      clearInterval(slide);
    }
    $(this).children("i").removeClass("font-16").toggleClass("fe-play fe-pause").addClass("font-16");
  });

  $(".next-slide").click(function () {
    next_slide();
    clearInterval(slide);
    $(".play-slide").children("i").removeClass("fe-pause font-16").addClass("fe-play font-16");
  });

  let seriesData = []
  let seriesDataFore = []
  let seriesCategories = []

  var init_chart_ns = function () {
    var options = {
      series: [0],
      chart: {
        height: 295,
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

  var init_chart_contacts = async function () {
    for (let i = 0; i < 30; i++) {
      seriesData.push(0);
      seriesDataFore.push(0);
      seriesCategories.push("-");
    }

    var options = {
      chart: {
        height: 336,
        type: 'line',
        shadow: {
          enabled: false,
          color: '#bbb',
          top: 3,
          left: 2,
          blur: 3,
          opacity: 1
        },
        animations: {
          enabled: true,
          easing: 'linear',
          dynamicAnimation: {
            speed: 1000
          }
        },
        toolbar: {
          show: false
        },
        zoom: {
          enabled: false
        }
      },
      subtitle: {
        text: "0",
        floating: true,
        align: "right",
        offsetY: 0,
        style: {
          fontSize: "22px"
        }
      },
      stroke: {
        width: 3,
        curve: 'smooth'
      },
      series: [{
        name: 'Forecast',
        data: seriesDataFore
      }, {
        name: 'Em Atendimento',
        data: seriesData
      }],
      xaxis: {
        categories: seriesCategories,
      },
      yaxis: {
        min: 0,
        max: 20,
      },
      colors: ['#b5b5b5', '#1abc9c'],
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark',
          gradientToColors: ['#8c8c8c', '#f672a7'],
          shadeIntensity: 1,
          type: 'horizontal',
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100, 100, 100]
        },
      },
      grid: {
        row: {
          colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
          opacity: 0.2
        },
        borderColor: '#185a9d'
      },
      responsive: [{
        breakpoint: 600,
        options: {
          chart: {
            toolbar: {
              show: false
            }
          },
          legend: {
            show: false
          },
        }
      }]
    }

    var chart_contacts = new ApexCharts(document.querySelector("#chart-contacts"), options);
    chart_contacts.render();

    return chart_contacts;
  };

  chart_ns = init_chart_ns();
  chart_contacts = await init_chart_contacts();

  (data_update = async () => {
    await fetch('http://127.0.0.1:8000/api/inbound/cards/', {
      method: 'GET',
    }).then((result) => {
      result.json().then((res) => {
        console.log(res);
        $('#data-atualizacao').html(res.data.data_atualizacao);
        $('#fila').html(res.data.fila);
        $('#tempo-fila').html(res.data.tempo_fila);
        $('#agentes-logados').html(res.data.agentes_logados + ' / ' + res.data.agentes_pausas);
        $('#agentes-disponiveis').html(res.data.agentes_disponiveis);
        $('#contatos-abandonados').html(parseInt(res.data.contatos_abandonados).toLocaleString('pt-BR'));
        $('#contatos-recebidos').html(parseInt(res.data.contatos_recebidos).toLocaleString('pt-BR'));
        $('#percentual-abandono').html(res.data.percentual_abandono);
        $('#percentual-atendimento').html(res.data.percentual_atendimento);
        $('#tma').html(res.data.tma);
        $('#tmt_segundos').html(parseInt(res.data.tmt_segundos).toLocaleString('pt-BR'));
        $('#tme').html(res.data.tme);
        $('#ns-projetado').html(res.data.nivel_servico_projetado);
        $('#forecast-percentual-volume').html(res.data.forecast_percentual_volume);
        $('#negocios').html(res.data.negocios);
        $('#percentual-conversao').html(res.data.percentual_conversao);
        $('#percentual-negocios-comparativo').html(res.data.percentual_negocios_comparativo);
        $('#percentual-abandono-comparativo').html(res.data.percentual_abandono_comparativo);
        $('#percentual-volume-comparativo').html(res.data.percentual_volume_comparativo);
        $('#percentual-tma-comparativo').html(res.data.percentual_tma_comparativo);


        if (res.data.fila > 5) {
          $('.card-fila').addClass("border-danger");
        } else if (res.data.fila > 0) {
          $('.card-fila').addClass("border-warning");
        } else {
          $('.card-fila').removeClass("border-danger");
          $('.card-fila').removeClass("border-warning");
        }

        if (res.data.tempo_fila_segundos > 20) {
          $('.card-tempo-fila').addClass("border-danger");
        } else if (res.data.tempo_fila_segundos > 0) {
          $('.card-tempo-fila').addClass("border-warning");
        } else {
          $('.card-tempo-fila').removeClass("border-danger");
          $('.card-tempo-fila').removeClass("border-warning");
        }

        if (res.data.agentes_disponiveis > 0) {
          if (res.data.fila > 0 || res.data.agentes_disponiveis > 5) {
            $('.card-agentes-disponiveis').removeClass("border-warning");
            $('.card-agentes-disponiveis').addClass("border-danger");
          } else {
            $('.card-agentes-disponiveis').removeClass("border-warning");
            $('.card-agentes-disponiveis').removeClass("border-danger");
          }
        } else {
          $('.card-agentes-disponiveis').removeClass("border-danger");
          $('.card-agentes-disponiveis').addClass("border-warning");
        }

        if (res.data.agentes_logados > res.data.forecast_agentes) {
          $('.card-agentes-logados').removeClass("border-danger");
        } else {
          $('.card-agentes-logados').addClass("border-danger");
        }

        if (res.data.percentual_atendimento >= res.data.forecast_percentual_atendimento) {
          $('#icon-percentual-atendimento').removeClass("fe-arrow-down text-danger me-1");
          $('#icon-percentual-atendimento').addClass("fe-arrow-up text-success me-1");
        } else {
          $('#icon-percentual-atendimento').removeClass("fe-arrow-up text-success me-1");
          $('#icon-percentual-atendimento').addClass("fe-arrow-down text-danger me-1");
        }

        if (res.data.tme_segundos > 20) {
          $('#icon-tme').removeClass("fe-arrow-down text-success me-1");
          $('#icon-tme').addClass("fe-arrow-up text-danger me-1");
        } else {
          $('#icon-tme').removeClass("fe-arrow-up text-danger me-1");
          $('#icon-tme').addClass("fe-arrow-down text-success me-1");
        }

        if (res.data.nivel_servico_projetado >= 80) {
          $('#icon-ns-projetado').removeClass("fe-arrow-down text-danger me-1");
          $('#icon-ns-projetado').addClass("fe-arrow-up text-success me-1");
        } else {
          $('#icon-ns-projetado').removeClass("fe-arrow-up text-success me-1");
          $('#icon-ns-projetado').addClass("fe-arrow-down text-danger me-1");
        }

        if (res.data.percentual_volume_comparativo >= 0) {
          $('#icon-percentual-volume-comparativo').removeClass("fa fa-caret-down text-danger me-1");
          $('#icon-percentual-volume-comparativo').addClass("fa fa-caret-up text-success me-1");
          $('#card-volume h2').removeClass("text-danger");
          $('#card-volume h2').addClass("text-success");
        } else {
          $('#icon-percentual-volume-comparativo').removeClass("fa fa-caret-up text-success me-1");
          $('#icon-percentual-volume-comparativo').addClass("fa fa-caret-down text-danger me-1");
          $('#card-volume h2').removeClass("text-success");
          $('#card-volume h2').addClass("text-danger");
        }

        if (res.data.percentual_abandono_comparativo <= 0) {
          $('#icon-percentual-abandono-comparativo').removeClass("fa fa-caret-up text-danger me-1");
          $('#icon-percentual-abandono-comparativo').addClass("fa fa-caret-down text-success me-1");
          $('#card-abandono h2').removeClass("text-danger");
          $('#card-abandono h2').addClass("text-success");
        } else {
          $('#icon-percentual-abandono-comparativo').removeClass("fa fa-caret-down text-success me-1");
          $('#icon-percentual-abandono-comparativo').addClass("fa fa-caret-up text-danger me-1");
          $('#card-abandono h2').removeClass("text-success");
          $('#card-abandono h2').addClass("text-danger");
        }
      
        if (res.data.percentual_negocios_comparativo >= 0) {
          $('#icon-percentual-negocios-comparativo').removeClass("fa fa-caret-down text-danger me-1");
          $('#icon-percentual-negocios-comparativo').addClass("fa fa-caret-up text-success me-1");
          $('#card-negocios h2').removeClass("text-danger");
          $('#card-negocios h2').addClass("text-success");
        } else {
          $('#icon-percentual-negocios-comparativo').removeClass("fa fa-caret-up text-success me-1");
          $('#icon-percentual-negocios-comparativo').addClass("fa fa-caret-down text-danger me-1");
          $('#card-negocios h2').removeClass("text-success");
          $('#card-negocios h2').addClass("text-danger");
        }

        if (res.data.percentual_tma_comparativo <= 0) {
          $('#icon-percentual-tma-comparativo').removeClass("fa fa-caret-up text-danger me-1");
          $('#icon-percentual-tma-comparativo').addClass("fa fa-caret-down text-success me-1");
          $('#card-tma h2').removeClass("text-danger");
          $('#card-tma h2').addClass("text-success");
        } else {
          $('#icon-percentual-tma-comparativo').removeClass("fa fa-caret-down text-success me-1");
          $('#icon-percentual-tma-comparativo').addClass("fa fa-caret-up text-danger me-1");
          $('#card-tma h2').removeClass("text-success");
          $('#card-tma h2').addClass("text-danger");
        }

        var colors_ns = parseFloat(res.data.nivel_servico) >= 80 ? ['#1ABC9C'] : ['#F1556C'];
        chart_ns.updateSeries([parseFloat(res.data.nivel_servico)]);
        chart_ns.updateOptions({
          colors: colors_ns
        });

        seriesData.shift()
        seriesData.push(parseInt(res.data.contatos_em_atendimento))
        seriesDataFore.shift()
        seriesDataFore.push(parseInt(res.data.forecast_em_atendimento))
        seriesCategories.shift()
        seriesCategories.push(res.data.data_atualizacao.substr(-8))

        chart_contacts.updateSeries([{data: seriesDataFore}, {data: seriesData}]);
        chart_contacts.updateOptions({
          xaxis: {
            categories: seriesCategories
          },
          yaxis: {
            min: 0,
            max: Math.max(Math.max(...seriesData), Math.max(...seriesDataFore)) * 1.2
          },
          subtitle: {
            text: res.data.contatos_em_atendimento
          }
        })

        JSON.parse(res.data.skills).forEach(el => {
          obj = $("#skill-" + el["id_skill"])
          obj.find(".skill-volume").html(parseInt(el["qtd_contatos_oferecidos"]).toLocaleString('pt-BR'));
          obj.find(".skill-em-atendimento").html(parseInt(el["qtd_contatos_ativos"]).toLocaleString('pt-BR'));
          obj.find(".skill-percentual-abandono").html(el["per_abandono"]);
          obj.find(".skill-agentes-disponiveis").html(parseInt(el["qtd_agentes_disponiveis"]).toLocaleString('pt-BR'));
        });
      })
    });
    setTimeout(data_update, 5000);
  })();

  (disposition_update = async () => {
    await fetch('http://127.0.0.1:8000/api/inbound/dispositions/', {
      method: 'GET',
    }).then((result) => {
      result.json().then((res) => {
        console.log(res);
      });
    });
    setTimeout(disposition_update, 30000);
  })();
});