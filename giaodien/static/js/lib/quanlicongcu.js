'use strict';
var tools_update_filename = []; 
var setInterval_status; 
$(document).ready(function(){
    renderToolManager(); 
    renderToolDownloaded(); 

})
function renderToolManager(){
    $.ajax({
        type: "POST", 
        url : "/getalltool", 
        data:{"module_name": "all"}, 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == 'success'){
            $("#ToolManagerTable").DataTable().clear().destroy();
            $("#ToolManagerTable").DataTable({
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
                rowId: 'name', 
                columns: [
                    { data: "name" },
                    { data: "typemodule" }, 
                    { data: "version" }, 
                    {
                        data:"service", 
                        'defaultContent': "None"

                    }, 
                    {
                    className: "dt-center editor-delete",
                    defaultContent: '<button id="tooldelete" class="btn btn-danger ml-3">Xóa <i class="fa fa-trash fa-sm"/></button>',
                    orderable: false
                    }
                ]
            }); 

        }
    })
}

function renderToolDownloaded(){
    $.ajax({
        type: "GET", 
        url : "/gettoolsdownloaded", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == 'success'){
            $("#ToolUpdateManagerTable").DataTable().clear().destroy();
            $("#ToolUpdateManagerTable").DataTable({
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
                rowId: 'tool_filename', 
                columns: [
                    { data: "toolname" },
                    { data: "toolversion" }, 
                    {
                    className: "dt-center editor-delete",
                    defaultContent: '<button id="toolImport" class="btn btn-primary">Import <i class="fa fa-download fa-sm"/></button>',
                    orderable: false
                    }
                ]
            }); 

        }
    })
}

$(".ToolUpdateManagerDiv").on('click', "#toolImport", function(e){
    var row = $(e.currentTarget).closest("tr"); 
    var tool_import = row.attr('id'); 
    $.ajax({
        type:"POST", 
        url: "/importtool", 
        data: {"tool_filename": tool_import}, 
        beforeSend: (request) => {
          request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
        }
    })
    .done((resp) =>{
        console.log(resp); 
        if(resp['message'] == 'success' && resp['data'].includes("success") == true){
            new Noty({
                    type: 'success', 
                    layout: 'topRight',
                    theme: 'bootstrap-v4', 
                    text: 'Import công cụ vào hệ thống thành công', 
                    timeout: 1500, 
                    progressBar: false,
            }).show();
            renderToolManager();
        }else{
            new swal({
                icon: "error", 
                title: 'Oops...',
                text: 'Có lỗi xảy ra hoặc công cụ đã tồn tại trên hệ thống. Hãy thử lại!',
              }); 
            
        }
    })
})


$(".ToolManagerDiv").on('click', "#tooldelete", function(e){
    var row = $(e.currentTarget).closest('tr'); 
    var toolname = row.attr('id'); 
    new swal({
        title: "Bạn có chắn chắn muốn xóa?",
        text: "Một khi hoàn tất,công cụ sẽ bị xóa khỏi hệ thống",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "OK",
        
    })
    .then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type:"DELETE", 
                url: "/deletetool", 
                data: {"tool": toolname}, 
                beforeSend: (request) => {
                  request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
                }
            })
            .done((resp)=>{
                if(resp['message'] == 'success'){
                    new swal({
                        icon: "success", 
                        title: 'Thành công',
                        text: 'Đã xóa công cụ thành công!',
                    }); 
                    $("#ToolManagerTable").DataTable().row(row).remove().draw();
                }else{
                    new swal("Có lỗi xảy ra, hãy thử lại!", {
                        icon: "error", 
                    });
                }
            })

            
        } 
        
    });
})
function checkUpdateStatus(){
    var sum_tool = tools_update_filename.length; 
    $.ajax({
        type: "POST", 
        url : "/updatestatus",
        data: {"sum_tool": sum_tool}, 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == 'success' && resp['data'] == 100){
            let id = window.setInterval(() => {}, 0);
            while (id) {
            window.clearInterval(id);
            id--;
            }
            setInterval_status = false; 
            swal.close(); 
            new swal({
                icon: "success", 
                title: 'Thành công',
                text: 'Đã cập nhật công cụ cho hệ thống thành công!',
            }); 
            renderToolDownloaded(); 
        }
    })

}
function showLoadingUpdateTool(){
    new swal({
        title: 'Loading',
        text: "Đang cập nhật công cụ của hệ thống", 
        allowEscapeKey: false,
        allowOutsideClick: false,
        didOpen: () => {
          swal.showLoading();
        }
      }); 
    let id = window.setInterval(checkUpdateStatus, 1000); 
    setInterval_status = true; 
}



$(document).on("click", "#updateTools", function(){
    
    $.ajax({
        type: "GET", 
        url : "/checktoolforupdate", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == "success"){
            tools_update_filename = []; 
            var List_tool_update_name_for_display = ''; 
            var list_tools_update = resp['data']
            for(var i = 0; i < list_tools_update.length; i++){
                var tool_update = list_tools_update[i]; 
                tools_update_filename.push(tool_update['tool_filename']);
                if (i+1 ==list_tools_update.length ){
                    List_tool_update_name_for_display = List_tool_update_name_for_display + tool_update['toolname']; 
                }
                else{
                    List_tool_update_name_for_display = List_tool_update_name_for_display + tool_update['toolname'] + ", ";
                }
            }
            if(tools_update_filename.length > 0){
                new swal({
                    title: "Xác nhận!",
                    text: "Các công cụ " + List_tool_update_name_for_display + " đã có phiên bản mới. Bạn có muốn cập nhật không?",
                    icon: "info",
                    buttons: true,
                })
                .then((willDelete) => {
                    if (willDelete) {
                        $.ajax({
                            type: "POST", 
                            url : "/updatetool", 
                            data :{"list_tools": tools_update_filename}, 
                            beforeSend: (request) =>{
                              request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
                            }
                        })
                        .done((resp) => {
                            if(resp['message'] == 'success'){
                                showLoadingUpdateTool(); 
    
                            }else{
                                new swal({
                                    icon: "error", 
                                    title: 'Oops...',
                                    text: 'Có lỗi xảy ra trong quá trình cập nhật. Hãy thử lại!',
                                  }); 
    
                            }
    
                        })
                    }
                });
            }else{
                new swal({
                    title: "Đã cập nhật!",
                    text: "Không có công cụ cần cập nhật!",
                    icon: "success",
                    buttons: true,
                })
            }
        }
    })
})



