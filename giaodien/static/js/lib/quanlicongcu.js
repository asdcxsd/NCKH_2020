'use strict';
$(document).ready(function(){
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
                    {
                        data:"service", 
                        'defaultContent': "None"

                    }, 
                    {
                    className: "dt-center editor-delete",
                    defaultContent: '<button id="tooldelete" class="btn btn-danger">Xóa <i class="fa fa-trash fa-sm"/></button>',
                    orderable: false
                    }
                ]
            }); 

        }
    })
})
$(".ToolManagerDiv").on('click', "#tooldelete", function(e){
    var row = $(e.currentTarget).closest('tr'); 
    var toolname = row.attr('id'); 
    swal({
        title: "Bạn có chắn chắn muốn xóa?",
        text: "Một khi hoàn tất,công cụ sẽ bị xóa khỏi hệ thống",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
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
                    swal("Công cụ đã được xóa!", {
                        icon: "success",
                        });
                    $("#ToolManagerTable").DataTable().row(row).remove().draw();
                }else{
                    swal("Có lỗi xảy ra, hãy thử lại!", {
                        icon: "error", 
                    });
                }
            })

            
        } 
    });
})
$(document).on("click", "#updateTools", function(){
    $.ajax({
        type: "GET", 
        url : "/updatetool", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == "success"){
            
        }
    })
})



