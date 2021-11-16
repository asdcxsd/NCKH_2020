"use strict";
$(document).ready(function(){
    $.ajax({
        type:"GET", 
        url : "/getusername", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == "success"){
            $("#username").text(resp['data']); 
        }
    })
})