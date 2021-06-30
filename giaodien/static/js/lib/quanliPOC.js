'use strict';
$(document).ready(function(){
    InitPOCManager(); 
})
function InitPOCManager(){
    $.ajax({
        type: "GET", 
        url : "/fetchpocs", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp) =>{
        if(resp["message"] == 'success'){
            $("#POCManagerTable").DataTable().clear().destroy();
            $("#POCManagerTable").DataTable({
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
                rowId: 'name', 
                columns: [
                    { data: "ID" },
                    { data: "pocName" }, 
                    { data: "Date" },
                    { data: "Name" }, 
                    {
                    className: "dt-center editor-delete",
                    defaultContent: '<i class="fa fa-info-circle" title="Xem thông tin chi tiết của POC"/>&nbsp;&nbsp;<i class="fa fa-trash" title="Xóa POC khỏi hệ thống"/>',
                    orderable: false
                    }
                ]
            }); 
        }
    })
}
$(document).on('click', '.fa-trash', function(e){
    var row = $(e.currentTarget).closest('tr'); 
    var pocname = $("#POCManagerTable").DataTable().row(row).data()['pocName']; 
    e.stopPropagation();
    swal({
        title: "Bạn có chắn chắn muốn xóa?",
        text: "Một khi hoàn tất, POC sẽ bị xóa hoàn toàn khỏi hệ thống",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
            $.ajax({
                type: "DELETE", 
                url : "/removepoc", 
                data: {"pocname": pocname}, 
                beforeSend: (request) =>{
                  request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
                }
            })
            .done((resp)=>{
                if(resp['message'] == 'success'){
                    
                    swal("POC đã được xóa!", {
                        icon: "success",
                        });
                    InitPOCManager(); 
                }else{
                    swal("Có lỗi xảy ra, hãy thử lại!", {
                        icon: "error", 
                    });
                }
            })

            
        } 
    });
})
$(document).on('click', '.fa-info-circle', function(e){
    e.stopPropagation();
    var row = $(e.currentTarget).closest('tr'); 
    var pocname = $("#POCManagerTable").DataTable().row(row).data()['pocName']; 
    $.ajax({
        type: "GET", 
        url : "/detailpoc", 
        data: {"pocname": pocname}, 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
    })
    .done((resp)=>{
        if(resp['message'] == 'success'){
            showDetailInformationModal(resp['data']); 
        }
    })
    
})

function showDetailInformationModal(data){
    document.getElementById('appVersion').innerHTML = '&emsp;' + data['appVersion']; 
    document.getElementById('name').innerHTML = '&emsp;' + data['name']; 
    document.getElementById('vulType').innerHTML = '&emsp;' + data['vulType']; 
    document.getElementById('author').innerHTML = '&emsp;' + data['author'].join(', '); 
    document.getElementById('current_protocol').innerHTML = '&emsp;' + data['current_protocol']; 
    document.getElementById('createDate').innerHTML = '&emsp;' + data['createDate']; 
    document.getElementById('updateDate').innerHTML = '&emsp;' + data['updateDate']; 
    document.getElementById('desc').innerHTML = '&emsp;' + data['desc']; 
    document.getElementById('references').innerHTML = '&emsp;' +"<a href='" + data['references']+"'>"+data['references']+"</a>";  
    $("#pocdetailmodal").modal('show'); 
}