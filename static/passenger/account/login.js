console.log("Login Passenger")
$(document).ready(function() {
        $("#passenger-login").submit(function(event) {
           event.preventDefault();
           $("#passenger-login-btn").html(`<i class="fas fa-redo-alt fa-pulse"></i>`);
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    beforeSend: function() {
                        $("#error-username").html('');
                        $("#error-password").html('');
                    },
                    success: function(response) {
                        console.log(response);
                        $("#passenger-login-btn").html('Login');
                        if(response['info']) {
                         iziToast.info({
                            title: 'Account Not Created:',
                            message: response['info'],
                            position: 'topRight'
                          });
                        }
                        if(response['message']) {
                         iziToast.success({
                            title: 'Account Created:',
                            message: response['message'],
                            position: 'topRight'
                          });
                        }
                        if(response['form']['username']) {
                           $("#error-username").html(response['form']['username']);
                        }
                        if(response['form']['password']) {
                           $("#error-password").html(response['form']['password']);
                        }

                    },
                    error: function (request, status, error) {
                        $("#passenger-login-btn").html('Login');
                         console.log(request.responseText);
                         iziToast.error({
                            title: status,
                            message: error,
                            position: 'topRight'
                          });

                    }
           });
       });
    })