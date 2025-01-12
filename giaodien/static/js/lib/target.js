'use strict';
var target_datatable; 
// $('#submittarget').on('click', function() {
//     new Noty({
//         type: 'info', //alert (default), success, error, warning, info - ClassName generator uses this value → noty_type__${type}
//       layout: 'topRight', //top, topLeft, topCenter, topRight (default), center, centerLeft, centerRight, bottom, bottomLeft, bottomCenter, bottomRight - ClassName generator uses this value → noty_layout__${layout}
//       theme: 'bootstrap-v4', //relax, mint (default), metroui - ClassName generator uses this value → noty_theme__${theme}
//       text: 'My beautiful snackbar', //This string can contain HTML too. But be careful and don't pass user inputs to this parameter.
//       timeout: 3000, // false (default), 1000, 3000, 3500, etc. Delay for closing event in milliseconds (ms). Set 'false' for sticky notifications.
//       progressBar: false, //Default, progress before fade out is displayed
//       //closeWith: 'click' //default; alternative: button
      
//       /*animation: {
//               open: 'animated bounceInRight', // Animate.css class names
//               close: 'animated bounceOutRight' // Animate.css class names
//           }*/
//     }).show();
  
//   });

//thêm mục tiêu
$(document).ready(function(){
  if($('input[type="checkbox"]').is(":checked")){
    $(".TargetAuthenGroup").show(); 
  }else{
    $(".TargetAuthenGroup").hide(); 
  }
})
$('input[type="checkbox"]').change(function(){
  if ($(this).is(":checked")){
    $(".TargetAuthenGroup").show(); 
  }else{
    $(".TargetAuthenGroup").hide(); 
  }
})

$('#submittarget').on('click', ()=>{
  var username =$(".username").val(); 
  $("#username").val(''); 
  var targetname = $("#targetName").val(); 
  $("#targetName").val('');
  var targetIP = $("#targetIP").val(); 
  $("#targetIP").val('');
  var targetDomain = $("#targetDomain").val(); 
  $("#targetDomain").val(''); 
  var password = $("#password").val(); 
  $("#password").val(''); 
  var targetdescription = $("#targetDescription").val(); 
  $("#targetDescription").val(''); 
  $.ajax({
    type: "POST", 
    url : "/addtarget", 
    data : {"targetname":targetname,"targetIP": targetIP, "targetDomain": targetDomain, "username": username, "password": password,"targetdescription":targetdescription}, 
    beforeSend: (request) =>{
      request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
    }
  })
  .done((resp)=>{
    if(resp['data'] == "Update success"){
      new Noty({
              type: 'success', 
              layout: 'topRight',
              theme: 'bootstrap-v4', 
              text: 'Thêm mục tiêu thành công', 
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
        text: 'Có lỗi xảy ra, hãy thử lại', 
        timeout: 1500, 
        progressBar: false,
      }).show();
    }
  })
}); 

//Xóa mục tiêu
$(".targetManagerDiv").on('click',"#targetdelete",  (e)=>{
  var row = $(e.currentTarget).closest('tr'); 
  var targetid = row.attr('id'); 
  swal({
    title: "Bạn có chắc chắn không?",
    text: "Một khi xóa, mục tiêu sẽ bị xóa khỏi hệ thống",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((result) => { 
    if (result) {
      $.ajax({
        type: "DELETE", 
        url : "/deletetarget", 
        data : {"targetid":targetid}, 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
      })
      .done((resp)=>{
        if(resp['message'] == 'success'){
          $("#targetmanagertable").DataTable().row(row).remove().draw();
          swal("Mục tiêu đã bị xóa!", {
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

// cung cap thong tin chi tiet ve mục tieu
$(".targetManagerDiv").on('click',"#targetDetail",  (e)=>{
  var  targetid = $(e.currentTarget).closest("tr").attr("id")
  $("#TargetDetailTable").html(''); 
  $.ajax({
    type: "POST", 
    url : "/gettarget", 
    data : {"id":targetid}, 
    beforeSend: (request) =>{
      request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
    }
  })
  .done((resp)=>{
    if(resp['message'] == 'success'){
      for (var [key, value] of Object.entries(resp['data'])) {
        var row = $("<tr>"); 
        if(key == '_id'){
          key = "ID Mục tiêu"; 
        }
        if(key == "authen"){
          key = "Xác thực"; 
        }
        if(key == "date"){
          key = "Ngày tạo"; 
        }
        if(key == "describe"){
          key = "Mô tả";
        }
        if(key == "domain"){
          key = "website"; 
          
        }
        if(key == "ip_address"){
          key = "Địa chỉ IP"; 
        }
        if(key == "name"){
          key = "Tên mục tiêu"; 
        }
        row.append($("<td style='width:50%;'>").html("<h5><strong>"+key+"</strong></h5>"));
        if(key == "Xác thực"){
           
          row.append($("<td>").jsonPresenter({
            json: value
          })); 
        }else if(key == "website"){
          if (!value.match(/^[a-zA-Z]+:\/\//))
          {
              var result = 'http://' + value;
          }
          row.append($("<td>").html("<h6><a href='"+result+"'>"+value+"</a></h6>"));
        }
        else{
          row.append($("<td>").html("<h6>"+value+"</h6>"));
        }
        $("#TargetDetailTable").append(row); 
      }
      $("#TargetDetailModal").modal("show"); 

    }
  })
})

//gen ra bang quan ly muc tieu 
$("#targetmanagertab").on('click', ()=>{
  $.ajax({
    type: "GET", 
    url : "/getalltarget", 
    beforeSend: (request) =>{
      request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
    }
  })
  .done((resp)=>{
    if(resp['message'] == 'success'){
      $("#targetmanagertable").DataTable().clear().destroy();
      $("#targetmanagertable").DataTable({
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
            { data: "ip_address" },
            { data: "name" }, 
            {
              className: "dt-center editor-delete",
              defaultContent: '<button id="targetDetail" class="btn btn-primary">Chi tiết</button><button id="targetdelete" class="btn btn-danger ml-3" >Xóa</button>',
              orderable: false
            }
        ]
      })
    }
  })
  .fail(()=>{
  })
});

