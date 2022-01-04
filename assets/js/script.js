function showRegister() {
    $('#register-navbar').hide();
    $('#login-navbar').show();
    $('#form-login').hide();
    $('#form-register').show();
    document.getElementById('h3').innerText = 'Register Here';
}

function showLogin() {
    $('#register-navbar').show();
    $('#login-navbar').hide();
    $('#form-login').show();
    $('#form-register').hide();
    document.getElementById('h3').innerText = 'Login Here';
}

function sendMail() {
    let email = document.getElementById('email').value;
    if (email === '') {
        alert('Please Enter E-mail Address in the Field Below');
    } else {
        $.ajax({
            url: 'send_email',
            type: 'POST',
            data: {
                email: email
            },
            success: function (json) {
                if (json.exist === false){
                    alert("Email doesn't exist, please register!");
                }
                else {
                    if (json.exist === true && json.sent === true){
                        alert('Check Your Inbox & Follow the Instructions!!!');
                    }
                    else {
                        alert("Invalid Email Address or Something went wrong, please contact admin!");
                    }
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ':' + xhr.responseText);
            }
        });
    }
}

function openNav() {
    document.getElementById("mySidepanel").style.width = "210px";
}

function closeNav() {
    document.getElementById("mySidepanel").style.width = "0";
}

$(document).on('submit', '#forgotPassword', function (event) {
    event.preventDefault();
    const password = $('#password').val();
    $.ajax({
        url: 'save_reset_password',
        type: 'POST',
        data: {
            unique_url: window.location.pathname.slice(-16),
            password: password
        },
        success: function (json) {
            if (json.success) {
                alert("Success, You will be redirected to login");
                window.location.assign('/');
            }
            else {
                alert('Something went Wrong, please contact admin');
            }
        },
        error: function (xhr, err, errmsg) {
            console.log(xhr.status + ':' + xhr.responseText);
        }
    });
});

