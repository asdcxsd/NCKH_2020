'use strict';
$(document).ready(function(){
    checkAuthenOption(); 
    checkCustomOption();
}); 
function checkAuthenOption(){
    if($("#authencheckbox").is(":checked")){
        $(".accountdiv").show(); 
    }else{
        $(".accountdiv").hide(); 
    }
}
function checkCustomOption(){
    if($("#autocheckbox").is(":checked")){
        $(".custompocdiv").show(); 
    }else{
        $(".custompocdiv").hide(); 
    }
}

function redrawTargetModal(){
    $.ajax({
        type: "GET", 
        url : "/getalltarget", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) => {
        if(resp['message'] == 'success'){
            $("#addTargetTable").DataTable().clear().destroy();
            $("#addTargetTable").DataTable({
                data: resp['data'],
                "autoWidth": false,
                order: [[1,'asc']], 
                "language": {
                    "search": "Tìm kiếm ", 
                    "emptyTable": "Không có dữ liệu hiển thị", 
                    "info": "Hiển thị trang _PAGE_/_PAGES_", 
                    "infoEmpty": "Hiển thị trang 0/0", 
                    "lengthMenu": "Hiển thị _MENU_ hàng", 
                    "paginate": {
                      "previous": "Trang trước", 
                      'next': "Trang sau", 
                    },
                    select: {
                        rows: "Chọn %d mục tiêu"
                    }
                },
                rowId: '_id', 
                columns: [
                    {
                        data: null, 
                        defaultContent: '', 
                        className: 'select-checkbox', 
                        orderable: false
                    }, 
                    { data: "ip_address" },
                    { data: "name" }, 
                    {
                    className: "dt-center editor-delete",
                    defaultContent: '<button id="targetdelete" class="btn btn-danger">Xóa <i class="fa fa-trash fa-sm"/></button>',
                    orderable: false
                    }
                ], 
                select:{
                    style: 'os', 
                    selector: 'td:first-child'
                }
                
            });
        }
    })
}

//---------------Cấu hình mục tiêu-----------------------------

function getAccountConfigData(){
    
    $.ajax({
        type: "GET", 
        url : "/getconfigdata", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
        if(resp['message'] == "fail"){
            swal({
                title: "Chưa cấu hình cài đặt!",
                text: "Bạn hãy cấu hình server trước khi thực hiện kiểm thử!",
                icon: "error",
                buttons: true
              })
              .then((willDelete) => {
                if (willDelete) {
                  window.location.href = "/setting";  
                }
              });
        }
        if(resp['message'] == 'success'){
            $("#AddtargetModal").modal('show');
        }

    })
    
}
$('#startButton').on('click', function(){
    getAccountConfigData();
}); 
$("#AddtargetModal").on('show.bs.modal', (e) => {
    redrawTargetModal(); 
 });
 $(".TargetManagerStart").on('click', '#targetdelete', function(e){
     var row = $(e.currentTarget).closest('tr'); 
     var targetid = row.attr('id'); 
     $.ajax({
         type: "DELETE", 
         url : "/deletetarget", 
         data : {"targetid":targetid}, 
         beforeSend: (request) =>{
         request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
         }
     })
     .done((resp) =>{
         if(resp['message'] == 'success'){
             $("#addTargetTable").DataTable().row(row).remove().draw();
         }
     })
 })
 $("#TargetSubmitStartModal").on('click', function(e){
     var TargetIPModal = $("#TargetIPModal").val(); 
     $("#TargetIPModal").val('');
     var TargetNameModal = $("#TargetNameModal").val(); 
     $("#TargetNameModal").val(''); 
     $.ajax({
         type: "POST", 
         url : "/addtarget", 
         data : {"targetIP":TargetIPModal, "targetname":TargetNameModal}, 
         beforeSend: (request) =>{
           request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
         }
     })
     .done((resp) =>{
         if(resp['data'] == "Update success"){
             redrawTargetModal();
         }
     })
 }); 
 $('#addTarget_next').on('click', function(){
     $("#AddtargetModal").modal('hide');
     $("#Tool_config").modal('show'); 
 }); 
 //----------------Cấu hình công cụ-----------------------------
 $("#Tool_config_next").on('click', function(){
     $("#Tool_config").modal('hide');
     $("#POC_config").modal('show');  
 }); 
 $("#tool_config_back").on('click', function(){
     $("#Tool_config").modal('hide');
     $("#AddtargetModal").modal('show');
 }); 
 //-----------------cấu hình POC--------------------------------
 $("#POC_Config_continue").on('click', function(){
     $("#POC_config").modal('hide');
     $("#Sumary").modal('show');
 }); 
 $("#poc_config_back").on("click", function(){
     $("#POC_config").modal('hide');
     $("#Tool_config").modal('show');
 }); 
 $("#authencheckbox").change(function(){
     if(this.checked){
         $(".accountdiv").show(); 
     }else{
         $(".accountdiv").hide(); 
     }
 });
 $("#autocheckbox").change(function(){
     if(this.checked){
         $(".custompocdiv").show();
     }else{
         $(".custompocdiv").hide();
     }
 })
 //----------------Cấu hình tổng hợp----------------------------
 $("#Scan").on('click', function(){
     $("#Sumary").modal('hide');
     alert('Quá trình scan bắt đầu, vui lòng đợi'); 
 }); 
 $("#sumary_back").on('click', function(){
     $("#Sumary").modal('hide');
     $("#POC_config").modal('show');
 }); 
 

