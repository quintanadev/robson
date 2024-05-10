$(document).ready(async function () {
  var getMap = async () => {
    var impacto = $('#impacto').val();
    var operacao = $('select[name="operacao"]').find(':selected').val();
    var turno = $('select[name="turno"]').find(':selected').val();
    var computador = $('select[name="computador"]').find(':selected').val();
    await fetch('http://127.0.0.1:8000/api/users/map/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({impacto: impacto, operacao: operacao, turno: turno, computador:computador})
    }).then((result) => {
      result.json().then((res) => {
        if (res.result) {
          $.NotificationApp.send('Notificação: ', res.message, 'top-right', res.result, 3e3, 1, 'slide');
          next_update = 60000;
        } else {
          $('#users-map').html(res.mapa);
        }
      });
    });
  };

  $('.filter-impacto').click(async (event) => {
    target = $(event.target).parent();
    impacto = target.data('impacto');
    await $('#impacto').val(impacto);
    await getMap();
  });

  $('.form-filter').change(async () => {
    await getMap();
  });

  (map_update = async () => {
    var next_update = 60000 * 30;
    await getMap();
    setTimeout(map_update, next_update);
  })();
});