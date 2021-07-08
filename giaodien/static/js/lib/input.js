"use strict"; 
$(document).ready(function(){
    renderTargetForInput(); 
})
function renderTargetForInput(){
    $.ajax({
        type: "GET", 
        url : "/getalltarget", 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == 'success'){
            var listTarget = resp['data']
            for(var i = 0; i < listTarget.length; i++){
                var target = listTarget[i]; 
                var option = $("<option>"); 
                option.attr('id', target['_id']); 
                option.text(target['ip_address']); 
                $("#inputTarget").append(option);
            }
        }
    })
}

$("#inputmanagertab").on('click', ()=>{
    $.ajax({
        type: "GET", 
        url : "/getallinput", 
        beforeSend: (request) =>{
            request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp['message'] == 'success'){
            
            $("#inputManagerTable").DataTable().clear().destroy();
            $("#inputManagerTable").DataTable({
                data: resp['data'],
                "language": {
                "search": "Tìm kiếm ", 
                "emptyTable": "Không có dữ liệu hiển thị", 
                "info": "Hiển thị trang _PAGE_/_PAGES_", 
                "infoEmpty": "Hiển thị trang 0/0", 
                "lengthMenu": "Hiển thị _MENU_ hàng", 
                "paginate": {
                    "previous": "Trang trước", 
                    'next': "Trang sau", 
                }
                }, 
                "autoWidth": false,
                rowId: '_id', 
                columns: [
                    { data: "IN_IP" },
                    { data: "date_create" }, 
                    {
                    className: "dt-center editor-delete",
                    defaultContent: '<button id="InputDetail" class="btn btn-primary">Chi tiết</button><button id="InputDelete" class="btn btn-danger ml-3" >Xóa</button>',
                    orderable: false
                    }
                ]
            })
        }
    })
})

$(".inputManagerDiv").on('click', '#InputDelete', function(e){
    var row = $(e.currentTarget).closest("tr"); 
    var inputid = row.attr('id'); 
    swal({
        title: "Bạn có chắc chắn không?",
        text: "Một khi xóa, đầu vào sẽ bị xóa khỏi hệ thống",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          $.ajax({
            type: "DELETE", 
            url : "/deleteinput", 
            data : {"input_id":inputid}, 
            beforeSend: (request) =>{
              request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
            }
          })
          .done((resp)=>{
            if(resp['message'] == 'success'){
              $("#inputManagerTable").DataTable().row(row).remove().draw();
              swal("Đầu vào đã bị xóa!", {
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
