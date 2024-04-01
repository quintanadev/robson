!function (p) {
  "use strict";
  function t() { }
  t.prototype.send = function (t, i, o, n, a, s, r) {

    var color = '#98a6ad';
    if (n == 'success') {
      color = '#5ba035';
    } else if (n == 'error') {
      color = '#bf441d';
    } else if (n == 'warning') {
      color = '#da8609';
    } else if (n == 'info') {
      color = '#3b98b5';
    }

    var c = {
      heading: t,
      text: i,
      position: o,
      loaderBg: color,
      icon: n,
      hideAfter: a = a || 3e3,
      stack: s = s || 1
    };
    r && (c.showHideTransition = r),
      p.toast().reset("all"),
      p.toast(c)
  },
    p.NotificationApp = new t,
    p.NotificationApp.Constructor = t
}(window.jQuery),
  function (i) {
    var notification = sessionStorage.getItem('PAGE_NOTIFICATION');

    if (notification) {
      json_data = JSON.parse(notification);

      i.NotificationApp.send('Notificação: ', json_data.message, 'top-right', json_data.result, 3e3, 1, 'slide');
      sessionStorage.removeItem('PAGE_NOTIFICATION');
    }
  }(window.jQuery);
