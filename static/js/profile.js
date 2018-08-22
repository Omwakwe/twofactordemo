$(document).ready(function(){
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


    // $(document).on('click','#signup',(function(e) {
    //     e.preventDefault();
    //     signup_function(); 
    // }));

    $(document).on('submit','#profileForm',(function(e) {
        e.preventDefault();
        profile_update_function(); 
    }));

    function profile_update_function() {
        
        var formdata = $("#profileForm").serializeArray();
        console.log("Inside profile_update_function",formdata);
        $.ajax({
            url: "/accountInfo/",
            type: "POST",
            data: formdata,

            success: function(data) {
                console.log("data response",data);
                if (data.success=='yes') {
                    window.location.assign('/accountInfo/');
                }

            },
            error: function(xhr, errmsg, err) {
                console.log("Error on the server");
            }
        });

    }; //end of updatefunct



    //CSRF protetction for Django to work with Ajax
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});