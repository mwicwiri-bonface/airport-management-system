console.log("Register Passenger")
$(document).ready(function() {
        $("#passenger-register").submit(function(event) {
           event.preventDefault();
           $("#passenger-register-btn").html(`<i class="fas fa-redo-alt fa-pulse"></i>`);
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    beforeSend: function() {
                        $("#error_last_name").html('');
                        $("#error_email").html('');
                        $("#error_username").html('');
                        $("#error_first_name").html('');
                        $("#error_password1").html('');
                        $("#error_password2").html('');
                    },
                    success: function(response) {
                        console.log(response);
                        $("#passenger-register-btn").html('Register');
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
                        if(response['last_name']) {
                           $("#error_last_name").html(response['last_name']);
                        }
                        if(response['first_name']) {
                           $("#error_first_name").html(response['first_name']);
                        }
                        if(response['username']) {
                           $("#error_username").html(response['username']);
                        }
                        if(response['email']) {
                           $("#error_email").html(response['email']);
                        }
                        if(response['password1']) {
                           $("#error_password1").html(response['password1']);
                        }
                        if(response['password2']) {
                           $("#error_password2").html(response['password2']);
                        }

                    },
                    error: function (request, status, error) {
                    $("#passenger-register-btn").html('Register');
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