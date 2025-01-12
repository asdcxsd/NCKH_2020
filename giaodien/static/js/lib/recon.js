'use strict'; 
var Tools = [];
var Input; 
var Recon_result;
var id_process_detail; 
$(document).ready(function(){
    renderInputdata(); 
    renderToolData(); 
    renderReconDataOption();
    var activeTab = window.location.hash;
    if(activeTab.includes("~")){
        var temp = activeTab.split("~"); 
        $(temp[0])[0].click();
        showReconDetailModal(temp[1]); 
    }else{
        $( activeTab )[0].click();
    }
})

function renderReconDataOption(){
    $.ajax({
        type: "GET", 
        url : "/getallrecon", 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
        if(resp['message'] == "success"){
            var listRecon = resp['data']
            $("#ReconResultInput").append($("<option>").html(''));
            for(var i = 0; i < listRecon.length; i++){
                var recon = listRecon[i]; 
                var option = $("<option>"); 
                option.attr('id', recon['_id']); 
                option.text(recon['target_ip'] + "  ("+recon['date_end']+")"); 
                $("#ReconResultInput").append(option);
            }
        }
    })
}
$("#ReconResultInput").on("click","option",function(){
    var option = $(this); 
    if(option.text() == ""){
        Recon_result = ""; 
        $(".dropdown-text-recon-results").text("Chọn kết quả TTTT"); 
    }else{
        Recon_result = $(this).attr("id"); 
        $(".dropdown-text-recon-results").text(option.text()); 
    }
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
            $("#reconInput").append($("<option>").html(''));
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


$("#reconInput").on("click","option",function(){
    var option = $(this); 
    if(option.text() == ""){
        Input = ""; 
        $(".dropdown-text-input").text("Chọn đầu vào"); 
    }else{
        Input = $(this).attr("id"); 
        $(".dropdown-text-input").text(option.text()); 
    }
    
})

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
            $("#SelectedTools").html(''); 
            var obj = $('<input />'); 
            obj.attr('type', 'checkbox'); 
            obj.attr('class', 'selectall');
            var wrapper = $('<label />'); 
            wrapper = $('<label />').append(obj);
            var text = $('<span > '); 
            text.attr("class", 'select-text'); 
            text.text('Select'); 
            wrapper.append(text) ;
            wrapper.append(" all")
            var a  = $('<a href="#" />').append(wrapper)
            var extension = $('<li />').append(a);  
            $("#SelectedTools").append(extension); 
            for(var i = 0; i < listExtension.length; i ++){
                extension = listExtension[i]; 
                var name = extension['name']; 
                obj = $('<input />'); 
                obj.attr('type', 'checkbox'); 
                obj.attr('name', 'options[]'); 
                obj.attr('class', 'option justone');
                obj.attr('id','check');  
                obj.attr('value', name); 
                var wrapper = $('<label />'); 
                wrapper = $('<label />').append(obj);
                wrapper.append(name) ;
                var a  = $('<a href="#" />').append(wrapper)
                var extension = $('<li />').append(a);  
                $("#SelectedTools").append(extension);
            }
        } 
    })
}
$(document).on("change", ".selectall", function () {
    Tools = [];
    if ($(this).is(':checked')) {
        $('.option').prop('checked', true);
        var total = $('input[name="options[]"]:checked').length;
        $('input[name="options[]"]:checked').each(function(){
          Tools.push($(this).val()); 
        });
        $(".dropdown-text-tools").html('(' + total + ') Selected');
        $(".select-text").html(' Deselect');
    } else {
        $('.option').prop('checked', false);
        $(".dropdown-text-tools").html('Chọn công cụ');
        $(".select-text").html(' Select');
    }
  }); 
$(document).on("change", "input[type='checkbox'].justone", function () {
    Tools = []; 
    var a = $("input[type='checkbox'].justone");

    if(a.length == a.filter(":checked").length){
        $('.selectall').prop('checked', true);
        $(".select-text").html(' Deselect');
    }
    else {
        $('.selectall').prop('checked', false);
        $(".select-text").html(' Select');
    }
  var total = $('input[name="options[]"]:checked').length;
  if(total == 0 ){
    $(".dropdown-text-tools").html("Chọn công cụ");
  }else { 
    $(".dropdown-text-tools").html('(' + total + ') Selected');
  }
  $('input[name="options[]"]:checked').each(function(){
    Tools.push($(this).val()); 
  });
});

function renderReconResult(){
    $.ajax({
        type: "GET", 
        url : "/getallrecon", 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
    if(resp['message'] == 'success'){
        $("#reconResultManagerTable").DataTable().clear().destroy();
        $("#reconResultManagerTable").DataTable({
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
        rowId: '_id_process', 
        columns: [
            { data: "target_ip" },
            { data: "date_start" },
            { data: "date_end" }, 
            {
                className: "dt-center editor-delete",
                defaultContent: '<button id="reconDetail" class="btn btn-primary">Chi tiết</button><button id="reconDelete" class="btn btn-danger ml-3" >Xóa</button>',
                orderable: false
            }
        ]
        })
    }
    })
    .fail(()=>{
    })
}

$("#reconManagerTab").on('click',function(){
    renderReconResult();
})

function showReconDetailModal(process_id){
    $.ajax({
        type: "POST", 
        url : "/detailrecon", 
        data: {"process_id": process_id}, 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == 'success'){
            $("#reconResultDetailTable").html(''); 
            for (var [key, value] of Object.entries(resp['data'])){
                var row = $("<tr>"); 
                var data = resp['data']; 
                if(key == "_id"){
                    key = "id"; 
                    row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
                    row.append($("<td>").html("<h6>"+value+"</h6>"));
                    $(".exportReport").attr("id", value); 
                    $("#reconResultDetailTable").append(row); 
                    delete data['_id']; 
                }
                if(key == "_id_process"){
                    key = "ID tiến trình"; 
                    row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
                    row.append($("<td style='width:50%;'>").html("<h6>"+value+"</h6>"));
                    $("#reconResultDetailTable").append(row); 
                    delete data['_id_process']; 
                }
                if(key == "pre_type_module"){
                    key = "Module Input"; 
                    row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
                    row.append($("<td style='width:50%;'>").html("<h6>"+value[0]['_id']+"</h6>"));
                    $("#reconResultDetailTable").append(row); 
                    delete data['pre_type_module']; 
                }
                if(key == "date_start"){
                    key = "Thời gian bắt đầu"; 
                    row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
                    row.append($("<td style='width:50%;'>").html("<h6>"+value+"</h6>"));
                    $("#reconResultDetailTable").append(row); 
                    delete data['date_start']; 
                }
                if(key == "date_stop"){
                    key = "Thời gian kết thúc"; 
                    row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
                    row.append($("<td style='width:50%;'>").html("<h6>"+value+"</h6>"));
                    $("#reconResultDetailTable").append(row); 
                    delete data['date_stop']; 
                }
                if(key == "target_ip"){
                    key = "Địa chỉ IP"; 
                    row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
                    row.append($("<td style='width:50%;'>").html("<h6>"+value+"</h6>"));
                    $("#reconResultDetailTable").append(row); 
                    delete data['target_ip']; 
                }
                if(key == "target_domain"){
                    key = "Domain"; 
                    row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
                    if (!value[0].match(/^[a-zA-Z]+:\/\//))
                    {
                        var result = 'http://' + value;
                    }
                    row.append($("<td>").html("<h6><a href='"+result+"'>"+value+"</a></h6>"));
                    $("#reconResultDetailTable").append(row); 
                    delete data['target_domain']; 
                }
                
            }
            row.html(''); 
            row.append($("<td style='width:50%;'>").html("<h5><strong>Kết quả TTTT</strong></h5>"));
            var row_data = $("<td>"); 
            row_data.jsonPresenter({json: data}); 
            row.append(row_data); 
            id_process_detail = process_id; 
            $("#reconResultDetailModal").modal('show'); 
        }
    })
}
$(".reconResultManagerDiv").on('click', '#reconDelete', function(e){
    var row = $(e.currentTarget).closest('tr'); 
    var process_id = row.attr('id'); 
    swal({
        title: "Bạn có chắc chắn không?",
        text: "Một khi xóa, kết quả thu thập thông tin sẽ bị xóa khỏi hệ thống",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((result) => {
        if (result.isConfirmed) {
        $.ajax({
            type: "DELETE", 
            url : "/deleterecon", 
            data : {"process_id":process_id}, 
            beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
            }
        })
        .done((resp)=>{
            if(resp['message'] == 'success'){
            $("#reconResultManagerTable").DataTable().row(row).remove().draw();
            swal("Kết quả thu thập thông tin đã bị xóa!", {
                icon: "success",
            });
            }else{
            swal("Có lỗi xảy ra, hãy thử lại!", {
                icon: "error",
            });
            }
        })
        }
    });
})

$(".reconResultManagerDiv").on('click', "#reconDetail", function(e){
    var row = $(e.currentTarget).closest('tr'); 
    var process_id = row.attr('id'); 
    showReconDetailModal(process_id); 
})

$(".exportReport").on("click", function(e){
    var module_id = $(e.currentTarget).attr("id"); 
    var module = []; 
    module[0] = "OutputReport"; 
    $.ajax({
        type: "POST", 
        url : "/run", 
        data : {"Module_Reconnaissance": module_id,"db_process":id_process_detail, "Module": module}, 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) => {
    if(resp['message'] == "success"){
        window.location.href = "/start";
    }
    else{
        new Noty({
        type: 'error', 
        layout: 'topRight',
        theme: 'bootstrap-v4', 
        text: 'Có lỗi xảy ra, hãy thử lại', 
        timeout: 1500, 
        progressBar: false,
        }).show();
    }
    })
})

$("#InputRecon").on('click', function(){
    //kiểm tra đã cấu hình cài đặt chưa
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
            var Module_Input = Input; 
            var list_tool = Tools; 
            if(typeof Module_Input == "undefined" || Module_Input == ""){
                swal("Bạn chưa chọn đầu vào!", {
                    icon: "error",
                });

            }else{
                if(Tools.length == 0){
                    new Noty({
                        type: 'error', 
                        layout: 'topRight',
                        theme: 'bootstrap-v4', 
                        text: 'Chọn ít nhất một công cụ để thu thập thông tin', 
                        timeout: 1500, 
                        progressBar: false,
                    }).show();
                }else{
                    
                    $.ajax({
                        type: "POST", 
                        url : "/getlastrecon", 
                        data : {"Module_Input":Module_Input}, 
                        beforeSend: (request) =>{
                        request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
                        }
                    })
                    .done((resp) =>{
                        if(resp['message'] == "fail" && resp['last_recon'] == 1){
                            swal({
                                title: "Bạn có muốn thu thập thông tin mới không?",
                                text: "Lần cuối bạn thu thập thông tin là vào lúc " + resp['data'] + " giờ trước",
                                icon: "warning",
                                buttons: true,
                                dangerMode: true,
                                })
                                .then((result) => {
                                if (result.isConfirmed) {
                                    $.ajax({
                                        type: "POST", 
                                        url : "/run", 
                                        data : {"Module_Input":Module_Input, "Module":list_tool, "Module_Reconnaissance":Recon_result}, 
                                        beforeSend: (request) =>{
                                        request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
                                        }
                                    })
                                    .done((resp)=>{
                                        if(resp['message'] == "success"){
                                            window.location.href = "/start"; 
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
                                }
                                });
                        }else{
                            $.ajax({
                                type: "POST", 
                                url : "/run", 
                                data : {"Module_Input":Module_Input, "Module":list_tool}, 
                                beforeSend: (request) =>{
                                request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
                                }
                            })
                            .done((resp)=>{
                                if(resp['message'] == "success"){
                                    window.location.href = "/start"; 
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
                        }
                    })
                }
            }
        }

    })
    
    
})