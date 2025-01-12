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
            $("#username_profile").text(resp['data']); 
        }
    })
})
$("#submitpassword").on('click', function(){
    var currentPassword = $("#currentPassword").val(); 
    $("#currentPassword").val(''); 
    var NewPassword = $("#newPassword").val(); 
    $("#newPassword").val(''); 
    var confirmPassword = $("#confirmPassword").val(); 
    $("#confirmPassword").val('');
    if(NewPassword != confirmPassword){
        new swal({
            icon: "error", 
            title: 'Oops...',
            text: 'Xác nhận mật khẩu không khớp với mật khẩu mới!',
          }); 
    }
    else if(currentPassword == ""){
        new swal({
            icon: "error", 
            title: 'Oops...',
            text: 'Vui lòng nhập mật khẩu cũ!',
          }); 
    }
    else{
        $.ajax({
            type: "POST", 
            url : "/changepassword",
            data: {"currentPassword":currentPassword,"NewPassword":NewPassword , "confirmPassword": confirmPassword}, 
            beforeSend: (request) =>{
                request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
            }
        })
        .done((resp) =>{
            if(resp['message'] == "success"){
                if(resp['data'] == "confirm password mismatch"){
                    new swal({
                        icon: "error", 
                        title: 'Oops...',
                        text: 'Xác nhận mật khẩu không khớp!',
                      }); 
                }
                else{
                    new swal({
                        icon: "success", 
                        title: 'Thành công!',
                        text: 'Đổi mật khẩu thành công',
                      }); 
                }
            }
            if(resp['message'] == "fail"){
                if(resp['data'] == "currentpassword is incorrect"){
                    new swal({
                        icon: "error", 
                        title: 'Oops...',
                        text: 'Mật khẩu cũ không đúng!',
                      }); 
                }
            }
        })
    }
})