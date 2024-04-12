$(document).ready(async function () {
  var next_slide = function () {
    if ($("#slide-kpis").hasClass("d-none")) {
      $("#slide-skills").addClass("fadeOutLeft animated").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
        $(this).removeClass("fadeOutLeft animated");
        $(this).addClass("d-none");

        $("#slide-kpis").removeClass("d-none");
        $("#slide-kpis").addClass("fadeInRight animated").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
          $(this).removeClass("fadeInRight animated");
        });
      });
    } else {
      $("#slide-kpis").addClass("fadeOutLeft animated").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
        $(this).removeClass("fadeOutLeft animated");
        $(this).addClass("d-none");

        $("#slide-skills").removeClass("d-none");
        $("#slide-skills").addClass("fadeInRight animated").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
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

  var data_update = setInterval(async () => {
    await fetch('http://127.0.0.1:8000/dashboard/get_data_inbound/', {
      method: 'GET',
    }).then((result) => {
      result.json().then((data) => {
        console.log(data);
      })
    })
  }, 5000)

});
