"use strict"; 
$(document).ready(function(){
    $("#ShellArea").html(''); 
    $("#ShellCommand").html(''); 
})

$("#ShellCommand").on("keyup", function(e){
    if(e.key == "Enter" || e.keyCode == 13 ){
        var command = $("#ShellCommand").val(); 
        if (command == "clear"){
            $("#ShellArea").val(''); 
            $("#ShellCommand").val('');
        }else if(command == "close"){

        }else{
            $("#ShellArea").val($("#ShellArea").val() + command + "\n"); 
            var textArea = document.getElementById("ShellArea"); 
            textArea.scrollTop = textArea.scrollHeight; 
            $("#ShellCommand").val(''); 
        }
    }
})