$(document).ready(async function () {

  (outbound_update = async () => {
    var next_update = 120000;
    await fetch('http://127.0.0.1:8000/api/users/dashboard/', {
      method: 'GET',
    }).then((result) => {
      result.json().then((res) => {
        if (res.result) {
          $.NotificationApp.send('Notificação: ', res.message, 'top-right', res.result, 3e3, 1, 'slide');
          next_update = 60000;
        } else {
          console.log(res);
        }
      });
    });
    setTimeout(outbound_update, next_update);
  })();
});