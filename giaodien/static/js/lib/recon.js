'use strict'; 
$(document).ready(function(){
    renderInputdata(); 
    renderToolData(); 
})
function renderInputdata(){
    $.ajax({
        type: "GET", 
        url : "/getallinput", 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == 'success'){
            var listInput = resp['data']
            for(var i = 0; i < listInput.length; i++){
                var input = listInput[i]; 
                var option = $("<option>"); 
                option.attr('id', input['_id']); 
                option.text(input['IN_IP'] + "  ("+input['date_create']+")"); 
                $("#reconInput").append(option);
            }
        }
    })
}
function renderToolData(){
    $.ajax({
        type: "GET", 
        url : "/getalltool", 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
        if(resp['message'] == 'success'){
            console.log(resp['data']); 
        }
    })
}