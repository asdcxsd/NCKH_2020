'use strict';
var target_start_table; 
var target_id; 
var target_name; 
var target_ip;
var ReconTools = []; 
var ExploitTools = []; 
$(document).ready(function(){
    $(".TargetManagerStart").on('click','table tbody tr td:first-child', function(){
        var targetrow = target_start_table.row($(this).closest('tr'),{selected: true}); 
        if(targetrow.id() != undefined){
            target_id = targetrow.id(); 
            target_ip = targetrow.data()['ip_address']; 
            target_name = targetrow.data()['name']; ;
        }else{
            target_ip = null; 
            target_name = null; 
        }
    });
    checkAuthenOption(); 
    checkCustomOption();
    renderProcessPage();
    $("#ToolStartBody").html($("<td>").attr('colspan',3).css("text-align", "center").text("Bạn chưa chọn công cụ")); 
    getStatusFromServer(); 
    
    
}); 
function renderProcessPage(){
    $.ajax({
        type: "GET", 
        url : "/getallstatus", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
        if(resp['message'] == 'success'){
            $("#processManagerTable").DataTable().clear().destroy();
            $("#processManagerTable").DataTable({
              data: resp['data'],
              "language": {
                "search": "Tìm kiếm ", 
                "emptyTable": "Không có dữ liệu hiển thị", 
                "info": "Hiển thị trang _PAGE_/_PAGES_", 
                "infoEmpty": "Hiển thị trang 0/0", 
                "infoFiltered":   "(Lọc từ tổng cộng _MAX_ đầu vào)",
                "lengthMenu": "Hiển thị _MENU_ hàng", 
                "paginate": {
                  "previous": "Trang trước", 
                  'next': "Trang sau", 
                }
              }, 
              "autoWidth": false,
              rowId: '_id', 
              columns: [
                  { data: "Target" },
                  { data: "Date_Create" }, 
                  { data: "Status", 
                  "render": function(data, row, type){
                      if(data == "StatusRunning"){
                          return `<div class="row" style="display: flex; align-items: center;"><div class="col-md-4" style="padding-left: 11%">
                          <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="background:white; display: block; shape-rendering: auto;" width="50px" height="50px" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                          <circle cx="50" cy="50" r="32" stroke-width="8" stroke="#07abcc" stroke-dasharray="50.26548245743669 50.26548245743669" fill="none" stroke-linecap="round">
                            <animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" keyTimes="0;1" values="0 50 50;360 50 50"></animateTransform>
                          </circle>
                          <!-- [ldio] generated by https://loading.io/ --></svg></div><div class="col-md-8"><span className="custom-input vertical-align">Đang chạy</span></div></div>`; 
                      }
                      if(data == "StatusError"){
                            return `<div class="row" style="display: flex; align-items: center;"><div class="col-md-3 ml-4">
                            <img src="/static/img/error.png" style="height: 45px; width: 45px;"/></div><div class="col-md-8"><span className="custom-input vertical-align">Có lỗi</span></div></div>`;
                        }
                      if(data == "StatusSuccess"){
                          return `<div class="row" style="display: flex; align-items: center;"><div class="col-md-3 ml-4">
                          <img src="/static/img/success.png" style="height: 45px; width: 45px;"/></div><div class="col-md-8"><span className="custom-input vertical-align">Hoàn tất</span></div></div>`;
                      }
                  }
                  },
                  {
                    className: "dt-center editor-delete",
                    defaultContent: '<button id="ViewResult" class="btn btn-primary">Chi tiết</button><button id="ExportReport" class="btn btn-success ml-2" >Báo cáo</button><button id="StopProcess" class="btn btn-danger ml-2" >Dừng</button>',
                    orderable: false
                  }
              ]
            })
        }
    })
}

function getStatusFromServer(){
    var source = new EventSource('/getallstatusrunning'); 
    source.onmessage = function(event){
        var data = event.data ; 
        var i; 
        var process_table = $("#processManagerTable").DataTable(); 
        if(data.search("StatusRunning") != -1){
            data = JSON.parse(data); 
            if(data['message'] == "success"){
                var list_status = data['data']; 
                for(i=0; i < list_status.length; i++){
                    var status = list_status[i]; 
                    if(status['Status'] == 'StatusRunning'){
                        continue; 
                    }else if (status['Status'] == 'StatusError'){
                        var row_success_id = process_table.row('[id=' +status['_id'] +']').index(); 
                        var row_success_id_real_status = process_table.cell({row: row_success_id, column:2}).data(); 
                        if(row_success_id_real_status == "StatusRunning"){
                            var data_update =  `<div class="row" style="display: flex; align-items: center;"><div class="col-md-3">
                            <img src="/static/img/error.png" style="height: 70px; width: 70px;"/></div><div class="col-md-9"><span className="custom-input vertical-align">Không thành công</span></div></div>`; 
                            process_table.cell({row: row_success_id, column:2}).render(data_update); 
                            process_table.cell({row: row_success_id, column:2}).data("StatusSuccess"); 
                        }
                    }
                    else{
                        var row_success_id = process_table.row('[id=' +status['_id'] +']').index(); 
                        var row_success_id_real_status = process_table.cell({row: row_success_id, column:2}).data(); 
                        if(row_success_id_real_status == "StatusRunning"){
                            var data_update =  `<div class="row" style="display: flex; align-items: center;"><div class="col-md-3">
                            <img src="/static/img/success.png" style="height: 70px; width: 70px;"/></div><div class="col-md-9"><span className="custom-input vertical-align">Hoàn tất</span></div></div>`; 
                            process_table.cell({row: row_success_id, column:2}).render(data_update); 
                            process_table.cell({row: row_success_id, column:2}).data("StatusSuccess"); 
                        }

                    }
                }

            }
            
        }else{
            var row_count = process_table.rows().count(); 
            for(i = 0; i< row_count; i++){
                var row_success_id_real_status = process_table.cell({row: i, column:2}).data(); 
                if(row_success_id_real_status == "StatusRunning"){
                    var data_update =  `<div class="row" style="display: flex; align-items: center;"><div class="col-md-3">
                    <img src="/static/img/success.gif" style="height: 70px; width: 93px;"/></div><div class="col-md-9"><span className="custom-input vertical-align">Hoàn tất</span></div></div>`; 
                    process_table.cell({row: i, column:2}).render(data_update); 
                    process_table.cell({row: i, column:2}).data("StatusSuccess");
                }

            }
            source.close(); 
        }
        
    }
}
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
            
            target_start_table = $("#addTargetTable").DataTable({
                data: resp['data'],
                // "bFilter": false, 
                // "bJQueryUI": true, //Enable smooth theme
                // "sPaginationType": "full_numbers", //Enable smooth theme
                // "sDom": 't',
                "autoWidth": false,
                order: [[1,'asc']], 
                "language": {
                    "search": "Tìm kiếm ", 
                    "emptyTable": "Không có dữ liệu hiển thị", 
                    "info": "Hiển thị trang _PAGE_/_PAGES_", 
                    "infoEmpty": "Hiển thị trang 0/0", 
                    "infoFiltered":   "(Lọc từ tổng cộng _MAX_ đầu vào)",
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
                    defaultContent: '<button id="targetedit" class="btn btn-warning">Sửa</button><button id="targetdelete" class="btn btn-danger ml-3">Xóa</button>',
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

$("#processManagerTable").on("click",'#ViewResult', (e)=>{
    var table = $("#processManagerTable").DataTable(); 
    var row = $(e.currentTarget).closest('tr'); 
    var process_id = row.attr('id'); 
    if(table.row(row).data().Status == "StatusRunning"){
        swal({
            title: "Tiến trình đang chạy",
            text: "Vui lòng đợi đến khi kết thúc tiến trình để xem kết quả!",
            icon: "warning",
            button: "OK!",
          });
    }
    if(table.row(row).data().Status == "StatusError"){
        swal({
            title: "Oops...",
            text: "Có lỗi xảy ra trong quá trình chạy tiến trình!",
            icon: "error",
            button: "OK!",
          });
    }
    if(table.row(row).data().Status == "StatusSuccess"){
        $.ajax({
            type: "POST", 
            url : "/getmoduleprocessrun", 
            data: {"process_id": process_id},
            beforeSend: (request) =>{
              request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
            }
        })
        .done((resp) =>{
            if(resp['message'] == 'success'){
                var Module_list = resp['data']; 
                $("#InputResultDiv").hide();
                $("#ReconResultDiv").hide(); 
                $("#ExploitResultDiv").hide();
                $("#ProcessResultModal").modal("show"); 
                if(Module_list.includes("Module_Input")){
                    $("#InputResultDiv").show();
                    $(".InputResult").attr("id", process_id); 
                }
                if(Module_list.includes("Module_Reconnaissance")){
                    $("#ReconResultDiv").show(); 
                    $(".ReconResult").attr("id", process_id); 
                }
                if(Module_list.includes("Module_Exploit")){
                    $("#ExploitResultDiv").show(); 
                    $(".ExploitResult").attr("id", process_id); 
                }
                if(Module_list.includes("Module_Output")){
                    $("#ShellResultDiv").show(); 
                    $(".ShellResult").attr("id", process_id); 
                }  
            }
        })
    } 
})


$("#processManagerTable").on("click",'#StopProcess', (e)=>{
    var table = $("#processManagerTable").DataTable(); 
    var row = $(e.currentTarget).closest('tr'); 
    var process_id = row.attr('id'); 
    
})


$(".ReconResult").on('click', function(){
    var process_id = $(this).attr('id'); 
    window.open("/recon#reconManagerTab~" + process_id); 
})
$(".InputResult").on('click', function(){
    var process_id = $(this).attr('id'); 
    window.open("/input#inputmanagertab~" + process_id);
})

$(".ExploitResult").on('click', function(){
    var process_id = $(this).attr('id'); 
    window.open("/exploit#exploitManagerTab~" + process_id); 
})

$(".ShellResult").on('click', function(){
    var process_id = $(this).attr('id'); 
    $("#ProcessResultModal").modal("hide");
    $.ajax({
        type: "POST", 
        url : "/getshelllog", 
        data: {"process_id": process_id}, 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == 'success'){
            $("#ShellDataDetailTable").html(''); 
            var data = resp['data']["OUTPUT_LOG_RUN_SHELL"][0]; 
            for (var [key, value] of Object.entries(data)) {
                var row = $("<tr>"); 
                if(key == "id_connect"){
                    key = "ID kết nối"; 
                }
                if(key == "date_connect"){
                    key = "Ngày kết nối"; 
                }
                if(key == "target_connect"){
                    key = "Mục tiêu kết nối"; 
                }
                if(key == "ip_reverse_shell"){
                    key = "Địa chỉ IP shell proxy"; 
                }
                if(key == "port_reverse_shell"){
                    key = "Cổng shell proxy"; 
                }
                row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
                row.append($("<td>").html("<h6>"+value+"</h6>"));
                $("#ShellDataDetailTable").append(row); 
            }
            $("#ShellDataDetailModal").modal('show'); 
            
        }
    })
    
})


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
        if(resp['message'] == false){
           
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
        if(resp['message'] == true){
            $("#AddtargetModal").modal('show');
        }

    })
    
}
$('#startButton').on('click', function(){
    getAccountConfigData();
}); 
$("#AddtargetModal").on('show.bs.modal', (e) => {
    target_id = null; 
    target_name = null; 
    target_ip = null;
    ReconTools = []; 
    ExploitTools = []; 
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
 $(".TargetManagerStart").on('click', '#targetedit', function(e){
     $("#AddtargetModal").modal('hide'); 
    var row = $(e.currentTarget).closest('tr'); 
    var targetid = row.attr('id'); 
    $.ajax({
    type: "POST", 
    url : "/gettarget", 
    data : {"id":targetid}, 
    beforeSend: (request) =>{
        request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
    }
    })
    .done((resp) =>{
        if(resp['message'] == 'success'){
            for(var [key,value] of Object.entries(resp['data'])){
                if(key == "authen"){
                    $("#username").val(value['username']); 
                }
                if(key == "describe"){
                    $("#targetDescription").val(value); 
                }
                if(key == "domain"){
                    $("#targetDomain").val(value); 
                }
                if(key == "ip_address"){
                    $("#targetIP").val(value);  
                }
                if(key == "name"){
                    $("#targetName").val(value); 
                }
            }
            $(".EditTargetStart").attr('id', targetid); 
            $("#EditTargetModal").modal('show'); 
        }
    })
     
 })
 $(".EditTargetStart").on('click', ()=>{
     var targetid = $(".EditTargetStart").attr('id'); 
     var targetName = $("#targetName").val(); 
     var targetIP = $("#targetIP").val(); 
     var targetDomain = $("#targetDomain").val(); 
     var targetDescription = $("#targetDescription").val(); 
     var username = $("#username").val(); 
     var password = $("#password").val();
     $.ajax({
        type: "POST", 
        url : "/updatetarget", 
        data : {"targetid":targetid, "targetName": targetName, "targetIP": targetIP, "targetDomain": targetDomain,"targetDescription": targetDescription, "username": username,"password": password}, 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
        })
        .done((resp) =>{
            if(resp['message'] == 'success'){
                new Noty({
                    type: 'success', 
                    layout: 'topRight',
                    theme: 'bootstrap-v4', 
                    text: 'Chỉnh sửa mục tiêu thành công!', 
                    timeout: 1500, 
                    progressBar: false,
                }).show();
                $("#EditTargetModal").modal("hide"); 
                $("#AddtargetModal").modal('show');
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



 $('#addTarget_next').on('click', function(e){
     e.preventDefault(); 
     e.stopPropagation();
     $("#AddtargetModal").modal('hide');
     if(target_id != undefined){
        $("#Tool_config").modal('show'); 
        renderToolData();
        
     }else{
        swal({
            title: "Oops...",
            text: "Bạn chưa chọn mục tiêu để tiến hành kiểm thử!",
            icon: "error"
          })
          .then((willDelete) => {
            if (willDelete) {
                $("#AddtargetModal").modal('show');
            }
          });
     }
     
 }); 

 function renderToolData(){
    $.ajax({
        type: "POST", 
        url : "/getalltool", 
        data: {"module_name": "Module_Reconnaissance"},
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
        if(resp['message'] == 'success'){
            var listExtension = resp['data'];
            $("#ReconTools").html(''); 
            for(var i = 0; i < listExtension.length; i++){
                var tool = listExtension[i]; 
                var option = $("<option>").attr('value',tool['name']).text(tool['name']); 
                $("#ReconTools").append(option);
            }
            $("#ReconTools").easySelect({
                buttons: true, //
                search: true,
                placeholder: 'Chọn công cụ thu thập thông tin',
                placeholderColor: '#524781',
                selectColor: '#524781',
                itemTitle: 'Countrys selected',
                showEachItem: true,
                width: '100%',
            
            })
        } 
    })
}



 //----------------Cấu hình công cụ-----------------------------
 function renderToolsExploit(){
    $.ajax({
        type: "POST", 
        url : "/getalltool", 
        data: {"module_name": "Module_Exploit"},
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
        if(resp['message'] == 'success'){
            $("#ExploitTools").html(''); 
            var listExploitTools = resp['data']; 
            for(var i = 0; i < listExploitTools.length; i++){
                var tool = listExploitTools[i]; 
                var option = $("<option>").attr('value',tool['name']).text(tool['name']); 
                $("#ExploitTools").append(option);
            }
            $("#ExploitTools").easySelect({
                buttons: true, //
                search: true,
                placeholder: 'Chọn công cụ kiểm tra lỗ hổng bảo mật',
                placeholderColor: '#524781',
                selectColor: '#524781',
                itemTitle: 'Countrys selected',
                showEachItem: true,
                width: '100%',
                dropdownMaxHeight: '450px',
            })
            $("#POC_config").modal('show');  
        }

    })
 }
 $("#Tool_config_next").on('click', function(){
    ReconTools = []; 
    $("#Tool_config").modal('hide');
    ReconTools = ReconTools.concat($("#ReconTools").val()); 
    if(ReconTools.length == 0){
        swal({
            title: "Oops...",
            text: "Bạn chưa chọn Công cụ để thu thập thông tin!",
            icon: "error"
          })
          .then((willDelete) => {
            if (willDelete) {
                $("#Tool_config").modal('show');
            }
          });
    }else{
        
        renderToolsExploit(); 
    }
    
    
 }); 
 $("#tool_config_back").on('click', function(){
     $("#Tool_config").modal('hide');
     $("#AddtargetModal").modal('show');
 }); 


 //-----------------cấu hình POC--------------------------------
 function renderConfigSumary(){
     $("#ConfigStartSumary").html('');
     var row = $("<tr>"); 
     row.append($("<td style='width: 60%'>").html("<h5>IP mục tiêu</h5>")); 
     row.append($("<td>").html("<h6>"+target_ip+"</h6>")); 
     $("#ConfigStartSumary").append(row); 
     row = $("<tr>");
     row.append($("<td style='width: 60%'>").html("<h5>Tên mục tiêu</h5>")); 
     row.append($("<td>").html("<h6>"+target_name+"</h6>")); 
     $("#ConfigStartSumary").append(row); 
     row = $("<tr>");
     row.append($("<td style='width: 60%'>").html("<h5>Công cụ TTTT</h5>")); 
     row.append($("<td>").html("<h6>"+ReconTools.join(", ")+"</h6>")); 
     $("#ConfigStartSumary").append(row); 
     row = $("<tr>");
     row.append($("<td style='width: 60%'>").html("<h5>Công cụ kiểm thử bảo mật</h5>")); 
     row.append($("<td>").html("<h6>"+ExploitTools.join(", ")+"</h6>")); 
     $("#ConfigStartSumary").append(row); 
 }
 $("#POC_Config_continue").on('click', function(){
     $("#POC_config").modal('hide');
     ExploitTools = []; 
     ExploitTools = $("#ExploitTools").val();
     renderConfigSumary();
     $("#Sumary").modal('show');
 }); 
 $("#poc_config_back").on("click", function(){
     $("#POC_config").modal('hide');
     $("#Tool_config").modal('show');
 }); 
 
 //----------------Cấu hình tổng hợp----------------------------
 $("#Scan").on('click', function(){
     var Tools = ReconTools.concat(ExploitTools);
     var ListTools = ['Target']; 
     ListTools = ListTools.concat(Tools); 
     console.log(ListTools);
     $("#Sumary").modal('hide');
     $.ajax({
        type: "POST", 
        url : "/run", 
        data : {"Target":target_id, "Module": ListTools}, 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
        if(resp['message'] == "success"){
            swal({
                title: "Thành công!",
                text: "Tiến trình đang chạy, vui lòng đợi để xem kết quả",
                icon: "success",
                button: "OK!",
              });
              renderProcessPage();
              getStatusFromServer(); 
        }else{
            swal({
                title: "Oops...!",
                text: "Có lỗi xảy ra, hãy thử lại!",
                icon: "error"
              });
        }
    })
 }); 
 $("#sumary_back").on('click', function(){
     $("#Sumary").modal('hide');
     $("#POC_config").modal('show');
 }); 




 

