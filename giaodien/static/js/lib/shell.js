"use strict"; 
var process_id; 
var setInterval_status; 
var shell_source;
$(document).ready(function(){
    $("#ShellArea").html(''); 
    $("#ShellCommand").html(''); 
    
    process_id = window.location.hash.slice(1); 
    if(process_id != ""){
        showLoadingShell();
    }else{
        if(setInterval_status){
            let id = window.setInterval(() => {}, 0);
            while (id) {
            window.clearInterval(id);
            id--;
            }
            setInterval_status = false;
        }
    }
    
})
function decode_utf8(s) {
    return decodeURIComponent(escape(s));
  }
function getShellDataFromServer(){
    shell_source = new EventSource('/getshelldata'); 
    shell_source.onmessage = function(event){
        var data = JSON.parse(event.data);
        var shell_data = unescape(data['data']);
        // var shell_data = data.replace(/\t/g, "\n")
        $("#ShellArea").val($("#ShellArea").val() + shell_data); 
        var textarea = document.getElementById('ShellArea');
        textarea.scrollTop = textarea.scrollHeight;
        
    }
}

function checkShellStatus(){
    $.ajax({
        type: "GET", 
        url : "/getshellstatus", 
        data: {"process_id": process_id}, 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) => {
        if(resp['message'] == "success"){
            var result = resp['data']; 
            console.log()
            if(result.includes("Success") && typeof result  == "string"){
                let id = window.setInterval(() => {}, 0);
                while (id) {
                window.clearInterval(id);
                id--;
                }
                setInterval_status = false; 
                swal.close(); 
                $("#ShellArea").val('Connect to target successfully!' + "\n"
                + "type 'clear' to clear the screen" + "\n"
                + "type 'close' to close shell to target" + "\n"
                )
                getShellDataFromServer();
            }
            if(result.includes("Success") == false && typeof result  == "string"){
                let id = window.setInterval(() => {}, 0);
                while (id) {
                window.clearInterval(id);
                id--;
                }
                setInterval_status = false; 
                swal.close(); 
                new swal({
                    icon: "error", 
                    title: 'Oops...',
                    text: 'Đã có lỗi xảy ra, hãy thử lại!',
                  }); 
            }
        }
    })
}

function showLoadingShell(){
    new swal({
        title: 'Loading',
        text: "Đang đợi kết nối đến mục tiêu", 
        allowEscapeKey: false,
        allowOutsideClick: false,
        didOpen: () => {
          swal.showLoading();
        }
      }); 
    let id = window.setInterval(checkShellStatus, 1000); 
    setInterval_status = true; 
}

$("#ShellCommand").on("keyup", function(e){
    if(e.key == "Enter" || e.keyCode == 13 ){
        var command = $("#ShellCommand").val(); 
        var textarea = document.getElementById('ShellArea');
        textarea.scrollTop = textarea.scrollHeight;
        if (command == "clear"){
            $("#ShellArea").val(''); 
            $("#ShellCommand").val('');
        }else if(command == "close"){
            $("#ShellCommand").val('');
            shell_source.close();
            $.ajax({
                type: "GET", 
                url : "/closeshell",
                beforeSend: (request) =>{
                    request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
                }
            })
            .done((resp) =>{
                console.log(resp.includes("Close port")); 
                if(resp.includes("Close port")){
                    $("#ShellArea").val($("#ShellArea").val() + "\nclose shell to target successfully!" + "\n");
                    var textarea1 = document.getElementById('ShellArea');
                    textarea1.scrollTop = textarea.scrollHeight;
                }
            })

            

        }else{
            $("#ShellArea").val($("#ShellArea").val() + command + "\n"); 
            $("#ShellCommand").val(''); 
            $.ajax({
                type: "POST", 
                url : "/sendshelldata", 
                data: {"cmd": command}, 
                beforeSend: (request) =>{
                    request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
                }
            })

        }
    }
})