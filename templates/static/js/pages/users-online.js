$(document).ready(async function () {
  var httpPath = window.location.href.split(/[?#]/)[0].split('/').slice(0, 3).join('/');

  $('[data-plugin="switchery"]').each(function (idx, obj) {
    new Switchery(obj, $(obj).data());
  });

  var table = $('#table-status-online').DataTable({
    language: DataTableLanguage,
    drawCallback: () => {
      $('.dataTables_paginate > .pagination').addClass('pagination-rounded');
    },
    processing: true,
    lengthMenu: [
      [10, 17, 50, -1],
      [10, 17, 50, 'Todos']
    ],
    order: [[4, 'desc']],
    ajax: {
      url: `${httpPath}/api/users/dashboard/`,
      type: 'GET',
      dataSrc: (res) => {
        data = res.data;
        var operacao = $('#operacao').find(':selected').val();
        var lider = $('#lider').find(':selected').val();
        var pausas = $('#pausas').prop('checked');
        var fStatus = $('#filtro-status').val();
        
        if (operacao != 'Todos') {
          data = data.filter(x => x.operacao == operacao);
        }

        if (lider != 'Todos') {
          data = data.filter(x => x.lider == lider);
        }

        if (!pausas && fStatus != 'pausa') {
          data = data.filter(x => x.status.indexOf('Pausa') == -1);
        }

        if (fStatus == 'disponivel') {
          data = data.filter(x => x.status == 'Disponível');
        } else if (fStatus == 'falando') {
          data = data.filter(x => x.status == 'Falando' || x.status == 'Tabulando (Acw)');
        } else if (fStatus == 'pausa') {
          data = data.filter(x => x.status.indexOf('Pausa') > -1);
        } else if (fStatus == 'indisponivel') {
          data = data.filter(x => x.status == 'Indisponível');
        }

        return data;
      },
      complete: (xhr, textStatus) => {
        if (textStatus == 'success') {
          var data = xhr.responseJSON.data;
          $('#hc-disponivel').html(data.filter(x => x.status == 'Disponível').length);
          $('#hc-falando').html(data.filter(x => x.status == 'Falando' || x.status == 'Tabulando (Acw)').length);
          $('#hc-pausa').html(data.filter(x => x.status.indexOf('Pausa') > -1).length);
          $('#hc-indisponivel').html(data.filter(x => x.status == 'Indisponível').length);
        }
      }
    },
    columns: [
      { 'data': 'id', 'visible': false },
      { 'data': 'nome' },
      { 'data': 'lider' },
      { 'data': 'status' },
      { 'data': 'tempo' },
      { 'data': 'skill' }
    ],
    createdRow: (row, data, dataIndex) => {
      var icon = '&nbsp;&nbsp;&nbsp;&nbsp;<i class="fas fa-exclamation-triangle text-danger"></i>'
      data['tempo_int'] = parseInt(data['tempo'].replace(/:/g, ''));

      if (data['status'] == 'Indisponível') {
        $(row).addClass('table-warning');
        if (data['tempo_int'] > 500) {
          $(row).find('td:eq(3)').html(data['tempo'] + icon);
        }
      } else if (data['status'] == 'Disponível') {
        $(row).addClass('table-success');
        if (data['tempo_int'] > 100) {
          $(row).find('td:eq(3)').html(data['tempo'] + icon.replace('text-danger', 'text-warning'));
        }
      } else if (data['status'] == 'Falando' || data['status'] == 'Tabulando (Acw)') {
        $(row).addClass('table-info');
        if (data['tempo_int'] > (data['status'] == 'Falando' ? 1000 : 100)) {
          $(row).find('td:eq(3)').html(data['tempo'] + icon);
        }
      } else if (data['status'].indexOf('Pausa') > -1) {
        $(row).addClass('table-danger');
        if (data['status'].indexOf('Descanso') > -1 && data['tempo_int'] > 1100) {
          $(row).find('td:eq(3)').html(data['tempo'] + icon);
        } else if (data['status'].indexOf('Lanche') > -1 && data['tempo_int'] > 2100) {
          $(row).find('td:eq(3)').html(data['tempo'] + icon);
        } else if (data['status'].indexOf('Particular') > -1 && data['tempo_int'] > 1000) {
          $(row).find('td:eq(3)').html(data['tempo'] + icon);
        }
      }
    },
  });

  $('#operacao, #lider, #pausas').change(() => {
    table.ajax.reload();
  });

  $('#card-disponivel, #card-falando, #card-pausa, #card-indisponivel').click((event) => {
    var nStatus = $(event.target).parent().prop('id').replace('card-', '');
    var oStatus = $('#filtro-status').val();
    if (nStatus == oStatus) {
      nStatus = 'todos';
    }
    $('#filtro-status').val(nStatus);
    table.ajax.reload();
  });

  // (status_update = async () => {
  //   var next_update = 10000;
  //   table.ajax.reload();
  //   setTimeout(status_update, next_update);
  // })();
});