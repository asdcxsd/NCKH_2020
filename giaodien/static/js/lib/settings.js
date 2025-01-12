'use strict';

$("#submitsetting").on('click', ()=>{
    var Cf_PublicIP = $("#Cf_PublicIP").val(); 
    $("#Cf_PublicIP").val(''); 
    var Cf_Username_VPS = $("#Cf_Username_VPS").val(); 
    $("#Cf_Username_VPS").val(''); 
    var Cf_Password_VPS = $("#Cf_Password_VPS").val(); 
    $("#Cf_Password_VPS").val('');
    var Cf_PublicPort = $("#Cf_PublicPort").val(); 
    $("#Cf_PublicPort").val(''); 
    var Cf_Host_Check_Connect = $("#Cf_Host_Check_Connect").val();
    $("#Cf_Host_Check_Connect").val('');
    var Cf_Server_OpenPort = $("#Cf_Server_OpenPort").val(); 
    $("#Cf_Server_OpenPort").val(''); 
    var Cf_Host_Check_Metasploit_AI = $("#Cf_Host_Check_Metasploit_AI").val(); 
    $("#Cf_Host_Check_Metasploit_AI").val(''); 
    var Cf_Server_Metasploit_OpenPort = $("#Cf_Server_Metasploit_OpenPort").val(); 
    $("#Cf_Server_Metasploit_OpenPort").val(''); 
    $.ajax({
        type: "POST", 
        url : "/addsetting", 
        data : {"Cf_PublicIP":Cf_PublicIP,"Cf_Username_VPS": Cf_Username_VPS, "Cf_Password_VPS": Cf_Password_VPS, "Cf_PublicPort": Cf_PublicPort, "Cf_Host_Check_Connect": Cf_Host_Check_Connect,"Cf_Server_OpenPort":Cf_Server_OpenPort, "Cf_Host_Check_Metasploit_AI":Cf_Host_Check_Metasploit_AI, "Cf_Server_Metasploit_OpenPort":Cf_Server_Metasploit_OpenPort}, 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
        if(resp['message'] == "success"){
            new Noty({
                    type: 'success', 
                    layout: 'topRight',
                    theme: 'bootstrap-v4', 
                    text: 'Cấu hình cài đặt thành công', 
                    timeout: 1500, 
                    progressBar: false,
            }).show();
            $("#targetName").val(''); 
            $("#targetDescription").val(''); 
        }else{
            new Noty({
            type: 'error', 
            layout: 'topRight',
            theme: 'bootstrap-v4', 
            text: 'Có lỗi xảy ra, hãy thử lại!', 
            timeout: 1500, 
            progressBar: false,
            }).show();
        }
    })
    
})