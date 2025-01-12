"use strict"; 
var Target; 
$(document).ready(function(){
    renderTargetForInput(); 
    var activeTab = window.location.hash;
    if(activeTab.includes("~")){
        var temp = activeTab.split("~"); 
        console.log(temp[0]); 
        console.log(temp[1]); 
        $(temp[0]).click();
        var data_request = {"process_id": temp[1]}; 
        showInputDetailModal(data_request); 
    }else{
        $( activeTab )[0].click();
    }
    
})
function showInputDetailModal(data){
  $.ajax({
    type: "POST", 
    url : "/getinput", 
    data : data, 
    beforeSend: (request) =>{
      request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
    }
  })
  .done((resp)=>{
    if(resp['message'] == 'success'){
      $("#InputDetailTable").html(''); 
      for (var [key, value] of Object.entries(resp['data'])) { 
        var row = $("<tr>"); 
        if(key == '_id'){
          key = "ID đầu vào"; 
        }
        if(key == "IN_NAME"){
          key = "Tên đầu vào"; 
        }
        if(key == "IN_IP"){
          key = "Địa chỉ IP"; 
        }
        if(key == "IN_DOMAIN"){
          key = "Website"; 
        }
        if(key == "IN_DESCRIBE"){
          key = "Mô tả";
        }
        if(key == "IN_AUTHEN"){
          key = "Xác thực"; 
        }
        if(key == "_id_process"){
          key = "ID tiến trình"; 
        }
        if(key == "date_create"){
          key = "Ngày tạo"; 
        }
        if(key == "pre_type_module"){
          key = "Module tạo nên"; 
        }
        row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
        if(key == "Xác thực" || key == "Module tạo nên"){
          row.append($("<td>").jsonPresenter({
            json: value
          }))
        }else if(key == "Website"){
          if (!value[0].match(/^[a-zA-Z]+:\/\//))
          {
              var result = 'http://' + value;
          }
          row.append($("<td>").html("<h6><a href='"+result+"'>"+value+"</a></h6>"));
        }
        else{
          row.append($("<td>").html("<h6>"+value+"</h6>"));
        }
        $("#InputDetailTable").append(row); 
      }
      $("#InputDetailModal").modal("show"); 
    }
  })

}
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
            var listTarget = resp['data']; 
            $("#inputTarget").append($("<option>").html(''));
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
$("#inputTarget").on("click","option",function(){
  Target = ''; 
  var option = $(this); 
  if(option.text() == ""){
      $(".dropdown-text-target").text("Chọn mục tiêu"); 
  }else{
      Target = $(this).attr("id"); 
      $(".dropdown-text-target").text(option.text()); 
  }
  console.log(Target); 
})
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
      .then((result) => {
        if (result) {
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
$(".inputManagerDiv").on('click', "#InputDetail", function(e){
  var row = $(e.currentTarget).closest('tr'); 
  var input_id = row.attr("id"); 
  var data_request = {"input_id":input_id}; 
  showInputDetailModal(data_request); 

})

$("#AddInput").on('click', function(){
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
        if(typeof Target !== "undefined"){
          var module = []; 
          module[0] = "Target"; 
          // module[1] = "Module_Input"; 
          $.ajax({
            type: "POST", 
            url : "/run", 
            data : {"Target": Target, "Module": module}, 
            beforeSend: (request) =>{
              request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
            }
          })
          .done((resp) => {
            if(resp['message'] == "success"){
              new Noty({
                      type: 'success', 
                      layout: 'topRight',
                      theme: 'bootstrap-v4', 
                      text: 'Thêm đầu vào thành công', 
                      timeout: 1500, 
                      progressBar: false,
              }).show();
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
          
        }
      }

  })
  
})

$("#AddTargetInInputForm").on('click', function(e){
  e.preventDefault();
  window.location.href = "/target"; 
})
$("#AddReportInInputForm").on('click', function(e){
  e.preventDefault();
})