
var scannedPlatform=[];
var scannedVulnerability=[];
var tblScanCurrentPage=1;
var tblScanRecoredPerPage=10;
var tblScanKeyword='';
var tblScanCurrentReverse=true;
var tblScanCurrentSort='';
var Tools = []; 
var targetid = ''; 
var latestPOCDayCheck = ''; 
var reconProcess = []; 
var pocProcess = []; 
$( document ).ready(function() {
  TableScanManagement(tblScanCurrentPage,tblScanRecoredPerPage,tblScanKeyword);
  // ReloadDataTable();
  InitialPagination();
  //$("#Toast").hide();
  //thuc 
  
});

 

//phan xu li cho add target 

function InitTarget(){
  $('#target-display').html(''); 
  $.ajax({
    type:"GET", 
    url: "/getalltarget", 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
    } 
  })
  .done((resp) =>{
    if(resp["message"] == "success"){
      var listtarget = resp["data"]
      for(i=0; i < listtarget.length; i++){
        var displayTarget = listtarget[i]; 
        let tableRow = $('<tr>');
        tableRow.attr('class', displayTarget['_id']);
        tableRow.append($('<td>').text(String(i+1)));
        tableRow.append($('<td>').text(displayTarget['url']));
        tableRow.append($('<td>').text(displayTarget['name']));
        let tableData=$('<td>',{ style:'width:25%;'  });
        tableData.append(
          $('<button>', {type:"button" , class: 'btn btn-danger d',targetID:displayTarget['_id'], "url": displayTarget['url'], 'data-toggle':"modal", 'data-target':'#DeleteTargetmodal'})
                        .text('Detele')
        )
        tableRow.append(tableData);
        $('#target-display').append(tableRow);
      }
    }

  })
  .fail(() => {

  })
}
$("#btnAddTarget").on('click', ()=> {
  var url = $("#AddTargetInput").val(); 
  var name  = $("#AddTargetDescription").val(); 
  $.ajax({
    type:"POST", 
    url: "/addtarget", 
    data: {"url": url, "name": name}, 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) => {
    if(resp['data'] === "Update success"){
      $("#ToastAddTargetSuccess").show(); 
      $("#ToastAddTargetSuccess").toast('show'); 
      InitTarget();
    }
  })
  .fail(() => {
    $("#ToastAddTargetError").show(); 
    $("#ToastAddTargetError").toast('show'); 
  })
}); 
$("#btnDeleteTarget").on('click', (e) =>{
  var button = $(e.currentTarget); 
  var target_id = button.attr('targetid'); 
  $.ajax({
    type:"DELETE", 
    url: "/deletetarget", 
    data: {"targetid": target_id},
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    } 
  })
  .done((resp) => {
    if(resp['message'] === 'success') { 
      $("#ToastDeleteTargetSuccess").show(); 
      $("#ToastDeleteTargetSuccess").toast('show');
      $("#DeleteTargetmodal").modal('hide');
      InitTarget(); 


    }
  })
  .fail(() => {
    $("#ToastDeleteTargetError").show(); 
    $("#ToastDeleteTargetError").toast('show');

  })



}); 
function renderTargetDashboard(){
  $.ajax({
    type:"GET", 
    url: "/getalltarget", 
    async: false,
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    },
    success: (resp) => {
      if(resp['message'] === 'success'){
        $(".target").html(''); 
        listTarget = resp['data']; 
        for(i = 0; i < listTarget.length; i ++){
          var target = listTarget[i]; 
          var option = $("<option>");
          option.attr("id", target['_id']); 
          option.text(target['url']); 
          $(".target").append(option);
        }
      }
    }
  })
}
function renderExtensionDashboard(mode){
  $.ajax({
    type:"POST", 
    url: "/getExtension",
    data: {'mode':mode}, 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
    } 
  })
  .done((resp) => {
    if(resp['message'] === 'success'){
      listExtension = resp['data'];
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
      for(i = 0; i < listExtension.length; i ++){
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
  console.log($(this)); 
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
      $(".dropdown-text-tools").html('Select tools');
      $(".select-text").html(' Select');
  }
}); 
$(document).on("change", "input[type='checkbox']", function () {
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
  $(".dropdown-text-tools").html("Select tools");
}else { 
  $(".dropdown-text-tools").html('(' + total + ') Selected');
}
$('input[name="options[]"]:checked').each(function(){
  Tools.push($(this).val()); 
});
});
$("#DeleteTargetmodal").on('show.bs.modal', function(event){
  var button = $(event.relatedTarget);
  var modal = $(this); 
  $(this).find('#POCName').text("You want to delete the target: " + button.attr("url") + "?");
  $(this).find('#btnDeleteTarget').attr("targetID", button.attr('targetID')); 

})
//xonng phan xu li cho target 
//xu li phan dashboard 
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
$(document).on('click','#btnReconHistory',(e)=>{
  var button = $(e.currentTarget); 
  var recon_id = button.attr('reconid'); 
  $.ajax({
    type:"GET", 
    url: "/senddatatorecon", 
    data: {"id": recon_id},
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) => {
    if(resp['message'] === 'success'){
      $("#navCheckPOC").fadeOut(500).fadeIn(500);
      data = resp['data'][0];
      targeturl = getTargetURL(data['target_id']); 
      if($("#ReconBody tr:first").text() == "No data available in table" && $("#ReconBody").children().length == 1){
        $("#ReconBody tr:first").html('');
      }
      var i=0; 
      let tableRow = $('<tr >');
      tableRow.attr('data-tonggle', 'collapse'); 
      tableRow.attr('class', 'accordion-tonggle'); 
      tableRow.attr("id", data['target_id']); 
      tableRow.append($('<td>').text(String(i+1)));
      tableRow.append($('<td>').text(targeturl));
      tableRow.append($('<td>').text(data['date_start']));
      tableRow.append($('<td>').text(data['date_end']));
      let tableData=$('<td>',{ style:'width:500px;'  });
      tableData.append(
      $('<button>', {type:"button" , class: 'btn btn-info Recon-Detail','reconid':data['_id']})
                  .text('Detail')
      )
      $button= $('<button>', {type:"button" , class: 'btn ml-2 mr-2 btn-success ExploitCVE',"reconid":data['_id']}).text('CVE')
      tableData.append($button)
      tableData.append(
      $('<button>', {type:"button" , class: 'btn btn-danger',id:"DeleteRecon","reconid":data['_id'],
            'data-toggle':'modal', 'data-target': "#DeleteReconModal"
      })
      .text('Detele')
      )  
      tableRow.append(tableData);
      $('#ReconBody').append(tableRow);
      $('#Recon_Result').show();
      
    }else{
      if($("#ReconBody").children().length == 0){
        let tableRow = $('<tr >');
        let tableData=$('<td>');
        tableData.attr("colspan","5"); 
        tableData.text("No data available in table"); 
        tableRow.append(tableData);
        $('#ReconBody').append(tableRow);
        $('#Recon_Result').show();
      }
    }
  })


}); 
function renderReconHistory(){
  $.ajax({
    type: 'GET',
    url: '/reconhistory',
    beforeSend: (request) => {
        request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
    },
    })
    .done((resp) => {
      if(resp["message"] === 'success') { 
        listReconHistory = resp['data']; 
        TableDashboardManagement(tblDashboardCurrentPage,tblDashboardRecoredPerPage,tblDashboardKeyword,tblDashboardCurrentSort);
      }

    }); 


}
function getTargetURL(target_id){
  var targeturl; 
  $.ajax({
    type:"POST", 
    url: "/gettargeturl", 
    data: {"id": target_id},//targetid
    async: false, 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    },
    success: (resp) => {
      if(resp['message'] === 'success'){
        targeturl = resp['data']['url']; 
      }else{
        targeturl = ''; 
      }
    }
  })
  return targeturl;
}

InitDashboard();
function InitDashboard(){
  
  //renderExtensionDashboard(); 
  renderReconHistory(); 
}

//xong phan xu li cho dashboard




//thuc hien xu li phan recon
// $(document).on('click', '#ReconBody tr', (e) => {
//    var recon_data = $(e.currentTarget); 
//    console.log(recon_data); 
//    var recon_id = recon_data.attr("id"); 
//    alert(recon_id); 
// }); 
// xu li viec chon mode
$(".mode").on('change', function(){
  $(".mode").val($(this).val());
  var mode = $(".mode option:selected").val(); 
  renderExtensionDashboard(mode); 
});

$(".target").on('change', function(){
  $(".target").val($(this).val());
  var targetid = $(".target option:selected").attr('id'); 
  var reportByTargetId = GetReportByTarget(targetid); 
  console.log(reportByTargetId); 
  if(reportByTargetId === '' && $('#ReportBody').children().length == 0){
    let tableRow = $('<tr >');
    let tableData=$('<td>');
    tableData.attr("colspan","3"); 
    tableData.text("No report available for target"); 
    tableRow.append(tableData);
    $('#ReportBody').append(tableRow);
    $('#Report').show();
  }else{
    if($("#ReportBody").children().length == 1 && $("#ReportBody tr:first").text() != "No report available for target"){
      $("ReportBody").html(''); 
    }
    for(i=0; i < reportByTargetId.length; i++){
      var displayReport = reportByTargetId[i]; 
      let tableRow = $('<tr >');
      tableRow.attr("id", displayReport['_id']); 
      tableRow.append($('<td>').html('<input type="checkbox"/>'));
      tableRow.append($('<td>').text(displayReport['name']));
      tableRow.append($('<td>').text(displayReport['date']));
      $('#ReportBody').append(tableRow);
      $('#Report').show();
    }
  }

}); 


$(".btnDeleteRecon").on('click',(e) => {
  var button = $(e.currentTarget); 
  var recon_id = button.attr('reconid'); 
  $.ajax({
    type:"POST", 
    url: "/deleterecon", 
    data: {"id": recon_id},
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) =>{
    if(resp['message'] === 'success'){
      $("#DeleteReconModal").modal('hide'); 
      $("#ToastDeleteReconSuccess").show(); 
      $("#ToastDeleteReconSuccess").toast('show');
      RenderReconResult(); 
    }
    else{
      $("#DeleteReconModal").hide(); 
      $("#ToastDeleteReconError").show(); 
      $("#ToastDeleteReconError").toast('show');
    }

  })

})

$("#DeleteReconModal").on('show.bs.modal', function(event){
  var button = $(event.relatedTarget); 
  var reconid = button.attr('reconid'); 
  $(this).find('.btnDeleteRecon').attr('reconid',reconid); 
});
function GetReportByTarget(targetid){ 
  var result; 
  $.ajax({
    type:"POST", 
    url: "/getreportbytarget", 
    data: {"id": targetid},//targetid
    async: false, 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    },
    success: (resp) => {
      if(resp['message'] === 'success'){
        result = resp['data']; 
      }
    }
  })
  return result;

}
function InitScanActivity(){
  if($("#Recon_Activity_Body").children().length == 0){
    var row = $("<tr>");
    var data = $("<td>");  
    data.attr("colspan",'5'); 
    data.text("No scan activity available now");
    row.append(data); 

    $("#Recon_Activity_Body").append(row); 
  }

}
function InitReconStartPage(){
  var mode = $(".mode").val(); 
  InitScanActivity(); 
  renderTargetDashboard();  
  renderExtensionDashboard(mode); 
  var targetid = $(".target option:selected").attr('id'); 
  var reportByTargetId = GetReportByTarget(targetid); 
  if(reportByTargetId.length == 0 && $('#ReportBody').children().length == 0){
    let tableRow = $('<tr >');
    let tableData=$('<td>');
    tableData.attr("colspan","3"); 
    tableData.text("No report available for target"); 
    tableRow.append(tableData);
    $('#ReportBody').append(tableRow);
    $('#Report').show();
  }else{
    if($("#ReportBody").children().length == 1 && $("#ReportBody tr:first").text() != "No report available for target"){
      $("ReportBody").html(''); 
    }
    for(i=0; i < reportByTargetId.length; i++){
      var displayReport = reportByTargetId[i]; 
      let tableRow = $('<tr >');
      tableRow.attr("id", displayReport['_id']); 
      tableRow.append($('<td>').html('<input type="checkbox"/>'));
      tableRow.append($('<td>').text(displayReport['NameFile']));
      tableRow.append($('<td>').text(displayReport['DateUpload']));
      $('#ReportBody').append(tableRow);
      $('#Report').show();
    }
  }


}
function InitReconResult(){ 
  if($("#ReconBody").children().length == 0){
    let tableRow = $('<tr >');
    let tableData=$('<td>');
    tableData.attr("colspan","5"); 
    tableData.text("No data available in table"); 
    tableRow.append(tableData);
    $('#ReconBody').append(tableRow);
    $('#Recon_Result').show();
  }
}
function ReconDetail(x){
  $(this).closest('tbody').toggleClass('open'); 
  
}
function RenderReconResult(){
  var targetid = $(".target option:selected").attr("id");
  var targeturl = getTargetURL(targetid);  
  $.ajax({
    type:"POST", 
    url: "/getreconresult", 
    data: {"id": targetid},//targetid
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) => {
    if(resp['message'] === 'success'){
      var reconHistory = resp["data"]; 
      //$('#TargetRecon').text(targeturl); 
     
      if($("#ReconBody").children().length == 0){
        let tableRow = $('<tr >');
        let tableData=$('<td>');
        tableData.attr("colspan","5"); 
        tableData.text("No data available in table"); 
        tableRow.append(tableData);
        $('#ReconBody').append(tableRow);
        $('#Recon_Result').show();
      }else{
        if($("#ReconBody tr:first").text() == "No data available in table" && $("#ReconBody").children().text() != "No data available in table"){
          $("#ReconBody tr:first").html('');
        }
        for(i=0; i < reconHistory.length; i++){
          var displayRecon = reconHistory[i]; 
          let tableRow = $('<tr >');
          tableRow.attr("id", targetid); 
          tableRow.attr('data-tonggle', 'collapse'); 
          tableRow.attr('class', 'accordion-tonggle'); 
          tableRow.append($('<td>').text(String(i+1)));
          tableRow.append($('<td>').text(targeturl));
          tableRow.append($('<td>').text(displayRecon['date_start']));
          tableRow.append($('<td>').text(displayRecon['date_end']));
          let tableData=$('<td>',{ style:'width:500px;'  });
          tableData.append(
            $('<button>', {type:"button" , class: 'btn btn-info Recon-Detail','reconid':displayRecon['_id']})
                          .text('Detail')
          )
          $button= $('<button>', {type:"button" , class: 'btn ml-2 mr-2 btn-success ExploitCVE',"reconid":displayRecon['_id']}).text('CVE')
          tableData.append($button)
          tableData.append(
            $('<button>', {type:"button" , class: 'btn btn-danger',id:"DeleteRecon","reconid":displayRecon['_id'],
                           'data-toggle':'modal', 'data-target': "#DeleteReconModal"
                     })
                          .text('Detele')
          )
          tableRow.append(tableData);
          $('#ReconBody').append(tableRow);
          $('#Recon_Result').show();
        
        } 
      }
      
    }

  })
  .fail(() => {

  })

}
$(document).on('click','#Send_exploit',(e)=>{
  var button = $(e.currentTarget); 
  var recon_id = button.attr('reconid'); 
  $.ajax({
    type:"GET", 
    url: "/senddatatorecon", 
    data: {"id": recon_id},
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) => {
    if(resp['message'] === 'success'){
      $("#navCheckPOC").fadeOut(500).fadeIn(500);
      data = resp['data'][0];
      targeturl = getTargetURL(data['target_id']); 
      if($("#ReconBody tr:first").text() == "No data available in table" && $("#ReconBody").children().length == 1){
        $("#ReconBody tr:first").html('');
      }
      var i=0; 
      let tableRow = $('<tr >');
      tableRow.attr('data-tonggle', 'collapse'); 
      tableRow.attr('class', 'accordion-tonggle'); 
      tableRow.attr("id", data['target_id']); 
      tableRow.append($('<td>').text(String(i+1)));
      tableRow.append($('<td>').text(targeturl));
      tableRow.append($('<td>').text(data['date_start']));
      tableRow.append($('<td>').text(data['date_end']));
      let tableData=$('<td>',{ style:'width:500px;'  });
      $button= $('<button>', {type:"button" , class: 'btn ml-2 mr-2 btn-success ExploitCVE',"reconid":data['_id']}).text('CVE')
      tableData.append($button)
      tableData.append(
      $('<button>', {type:"button" , class: 'btn btn-danger',id:"DeleteRecon","reconid":data['_id'],
            'data-toggle':'modal', 'data-target': "#DeleteReconModal"
      })
      .text('Detele')
      )  
      tableRow.append(tableData);
      $('#ReconBody').append(tableRow);
      $('#Recon_Result').show();
      
    }else{
      if($("#ReconBody").children().length == 0){
        let tableRow = $('<tr >');
        let tableData=$('<td>');
        tableData.attr("colspan","5"); 
        tableData.text("No data available in table"); 
        tableRow.append(tableData);
        $('#ReconBody').append(tableRow);
        $('#Recon_Result').show();
      }
    }
  })


}); 
function CheckReconStatus(){
  var flag = 0; 
  $.ajax({
    type:"get", 
    url: "/reconstatus", 
    async: false,
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    },
    success: (resp) => {
      if(resp['message'] == 'success'){
      
        var listActivity  = resp['data']; 
        if($("#Recon_Activity_Body").children().length == 1 && $("#Recon_Activity_Body tr:first").text() == "No scan activity available now"){
          $("#Recon_Activity_Body").html(''); 
        }
        if(listActivity.length){
          for(i = 0; i < listActivity.length; i++){
            var activity = listActivity[i]; 
            var activityID = activity['_id']; 
            if($("#"+activityID).length){
              if(activity['status'] == 'success'){
                console.log($("#"+activityID + " td.status").val()); 
                $("#"+activityID + " td.status").text("success"); 
                $("#"+activityID + " td.btnViewResult").find(".Recon-Scan-Detail").attr("recon_id", activity['recon_id']); 
                $("#"+activityID + " td.btnSendToExploit").find(".Send_Data_exploit").attr("recon_id", activity['recon_id']);
              }else{
                flag = 1;
                continue; 
              }
              
            }else{
              var targeturl = getTargetURL(activity['target_id'])
              if(targeturl == ''){
                continue; 
              }
              var row = $("<tr>");
              row.attr("id", activityID); 
              row.append($("<td>").text(targeturl)); 
              row.append($("<td>").text(activity['date']));
              row.append($("<td>").attr('class','status').text(activity['status'])); 
              let tableData=$('<td>');
              tableData.attr('class', 'btnViewResult');
              let tableData1 = $("<td>"); 
              tableData1.attr('class', 'btnSendToExploit'); 
              if(activity['status'] == 'running'){
                flag = 1; 
              }
              tableData.append(
                $('<button >', {type:"button" , class: 'btn btn-info Recon-Scan-Detail','recon_id':activity['recon_id']})
                              .text('Detail')
              )
              row.append(tableData); 
              tableData1.append(
                $('<button >', {type:"button" , class: 'btn btn-info Send_Data_exploit','recon_id':activity['recon_id']})
                              .text('Send to Exploit')
              )
              row.append(tableData1)
              
              $("#Recon_Activity_Body").append(row); 
            } 
          }
        }
      }
    }
  })
  if (flag == 0 ){
    id = window.setInterval(() => {}, 0);
    while (id) {
      window.clearInterval(id);
      id--;
    }
  }
}
function CheckLastRecon(targetid){
  var result; 
  $.ajax({
    type:"POST", 
    url: "/checklastrecon", 
    data: {"id":targetid}, 
    async: false,
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    },
    success: (resp) => {
      result = resp
    }
  })
  return result; 
}
$(".btnContinueRecon").on('click', function(e){
  
  $("#ReconWarning").modal("hide");
  var targetid = $(".target option:selected").attr("id"); 
  var mode = $(".mode").val(); 
  $.ajax({
    type:"POST", 
    url: "/reconnaisance", 
    data: {"id": targetid, "tools": Tools, 'mode':mode},
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) => {
    if(resp['message'] === 'success'){
      $("#ToastStartReconSuccess").show(); 
      $("#ToastStartReconSuccess").toast('show');
      let id = window.setInterval(CheckReconStatus, 4000);
    }
  })
  .fail(() => {

  })
})
$("#btnAttack").on('click',function(e) {
  //$("."+targetid).html('In Progress'); 
  var targetid = $(".target option:selected").attr("id"); 
  var checkLastRecon = CheckLastRecon(targetid);
  
  if(checkLastRecon["message"] == "fail" && checkLastRecon["last_recon"] == 1){
    $("#ReconWarningDetail").text("The Last recon is " + checkLastRecon['data'] + " ago. Do you want to recheck?"); 
    $("#ReconWarning").modal("show");

  }else{
    var mode = $(".mode").val(); 
    $.ajax({
      type:"POST", 
      url: "/reconnaisance", 
      data: {"id": targetid, "tools": Tools, 'mode':mode},
      beforeSend: (request) => {
        request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
      }
    })
    .done((resp) => {
      if(resp['message'] === 'success'){
        $("#ToastStartReconSuccess").show(); 
        $("#ToastStartReconSuccess").toast('show');
        let id = window.setInterval(CheckReconStatus, 4000);
      }
    })
    .fail(() => {

    })
  }
});
$(document).on('click', '#ReconBody tr td:not(:last-child)', function(e){
  var tablerow = $(this).closest('tr'); 
  var targetid = tablerow.attr('id'); 
  var collapseRow = $("<tr>"); 
  collapseRow.attr("class", "hiddenRow"); 
  var collapseData = $("<td>"); 
  collapseData.attr("colspan",'5'); 
  var result; 
  $.ajax({
    type:"POST", 
    url: "/getpoccheckresult", 
    data: {"targetid": targetid},//targetid
    async: false,
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    },
    success: (resp) => {
      if(resp['message'] == 'success'){
        result = resp['data']; 
      }
    }
  })
  var collapseDataBody = $("<tbody>"); 

  if(result.length == 0 ){
    var  data = $("<td>"); 
    data.attr("colspan", '5');
    data.text("no CVE check result available"); 
    collapseRow.append(data); 
    tablerow.after(collapseRow); 
    $(".hiddenRow").hide(); 
    tablerow.next('tr').show();
  }else{
    for(i = 0; i < result.length; i++){
      var POCresult = result[i]; 
      let tableRow = $('<tr>');
      //tableRow.append($('<td>').text(String(i+1)));
      tableRow.append($('<td>').text(POCresult['entrypoint']));
      tableRow.append($('<td>').text(POCresult['app_name']));
      tableRow.append($('<td>').text(POCresult['date_check']));
      let tableData=$('<td>',{ style:'width:25%;'  });
      tableData.append(
      $('<button>', {type:"button" , class: 'btn btn-danger',id:"POCShell","pocid":POCresult['_id'],
            'data-toggle':'modal', 'data-target': "#ReverseShellModal"
      })
      .text('Runshell')
      )
      tableRow.append(tableData);
      collapseDataBody.append(tableRow); 
    }
    var collapseDataTable = $("<table>")
    collapseDataTable.append(collapseDataBody); 
    var div = $("<div>"); 
    div.attr("class", "col-md-12"); 
    div.append(collapseDataTable); 
    collapseData.append(div); 
    collapseRow.append(collapseData); 
    tablerow.after(collapseRow); 
    $(".hiddenRow").hide(); 
    tablerow.next('tr').show(); 
  }

}); 
$(document).on('click','.Recon-Scan-Detail', function(e){
  var button =  $(e.currentTarget); 
  var reconid = button.attr("recon_id"); 
  if(reconid == "No"){
    alert("wait for result"); 
  }else{
    window.open("/renderrecondetail?reconid="+reconid);
  }
})
$(document).on('click', ".Send_Data_exploit", function(e){
  var button =  $(e.currentTarget); 
  var reconid = button.attr("recon_id"); 
  if(reconid == "No"){
    alert("wait for result"); 
  }else{
    $.ajax({
      type:"GET", 
      url: "/senddatatorecon", 
      data: {"id": reconid},
      beforeSend: (request) => {
        request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
      }
    })
    .done((resp) => {
      if(resp['message'] === 'success'){
        $("#navCheckPOC").fadeOut(500).fadeIn(500);
        data = resp['data'][0];
        targeturl = getTargetURL(data['target_id']); 
        if($("#ReconBody tr:first").text() == "No data available in table" && $("#ReconBody").children().length == 1){
          $("#ReconBody tr:first").html('');
        }
        var i=0; 
        let tableRow = $('<tr >');
        tableRow.attr('data-tonggle', 'collapse'); 
        tableRow.attr('class', 'accordion-tonggle'); 
        tableRow.attr("id", data['target_id']); 
        tableRow.append($('<td>').text(String(i+1)));
        tableRow.append($('<td>').text(targeturl));
        tableRow.append($('<td>').text(data['date_start']));
        tableRow.append($('<td>').text(data['date_end']));
        let tableData=$('<td>',{ style:'width:500px;'  });
        $button= $('<button>', {type:"button" , class: 'btn ml-2 mr-2 btn-success ExploitCVE',"reconid":data['_id']}).text('CVE')
        tableData.append($button)
        tableData.append(
        $('<button>', {type:"button" , class: 'btn btn-danger',id:"DeleteRecon","reconid":data['_id'],
              'data-toggle':'modal', 'data-target': "#DeleteReconModal"
        })
        .text('Detele')
        )  
        tableRow.append(tableData);
        $('#ReconBody').append(tableRow);
        $('#Recon_Result').show();
        
      }else{
        if($("#ReconBody").children().length == 0){
          let tableRow = $('<tr >');
          let tableData=$('<td>');
          tableData.attr("colspan","5"); 
          tableData.text("No data available in table"); 
          tableRow.append(tableData);
          $('#ReconBody').append(tableRow);
          $('#Recon_Result').show();
        }
      }
    })
  }
})
$(document).on('click','.ExploitCVE', function(e){
  var tablerow = $(this).closest("tr"); 
  var targetid = tablerow.attr('id'); 
  $.ajax({
    type:"POST", 
    url: "/getpoccheckresult", 
    data: {"targetid": targetid},
    async: false,
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    },
    success: (resp) => {
      if(resp['message'] === 'success'){
        for(i = 0; i < resp['data'].length; i++){
          if(latestPOCDayCheck == ''){
            latestPOCDayCheck = resp['data'][i]['date_check']; 

          }else{
            if(latestPOCDayCheck < resp['data'][i]['date_check']){
              latestPOCDayCheck = resp['data'][i]['date_check'];
            }
          }

        }
        alert(latestPOCDayCheck); 
      }
    }
  })
  var button = $(e.currentTarget); 
  reconid = button.attr('reconid'); 
  $.ajax({
    type:"POST", 
    url: "/runpocscan", 
    data: {"targetid": reconid},
    async: false,
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    },
    success: (resp) => {
      if(resp['message'] === 'success'){
        $("#ToastStartPOCCheckSuccess").show(); 
        $("#ToastStartPOCCheckSuccess").toast('show'); 
        window.setInterval(CheckPOCScanStatus, 2000);
      }else{
        $("#ToastStartPOCCheckError").show(); 
        $("#ToastStartPOCCheckError").toast('show'); 
      }
    }
  })
});

$(document).on('click', '.Recon-Detail', function(e){
  var button  = $(e.currentTarget); 
  var reconid = button.attr("reconid"); 
  window.open("/renderrecondetail?reconid="+reconid); 
});

//thuc hien xong phan recon 




// thuc hien phan check POC //////////////////////////

function CheckPOCScanStatus(){
  $.ajax({
    type:"GET", 
    url: "/getpoccheckstatus", 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) =>{
    if(resp['message'] === 'fail'){
      id = window.setInterval(() => {}, 0);
      while (id) {
        window.clearInterval(id);
        id--;
      }
      
    }

  })
}


// thuc hien xong check POC /////////////////////////////////

// thuc hien phan reverse shell////////////////////////////
// phan xu li modal shell 
$("#InputCommand").on('keyup', function(e){
  if(e.key =="Enter" || e.keyCode ==13){
    var command = $("#InputCommand").val(); 
    if (command == "clear"){
      $("#DisplayShell").val("$>"); 
      $("#InputCommand").val('');
    }else{
      $("#DisplayShell").val($("#DisplayShell").val() +command + "\n");
      var textarea = document.getElementById('DisplayShell');
      textarea.scrollTop = textarea.scrollHeight;
      $("#InputCommand").val('');
      $.ajax({
        type:"POST", 
        url:"/sendshelldata", 
        data:{"port":4448,"cmd":command}, 
        beforeSend: (request) => {
        request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
      }
      })
      .done((resp)=>{
        if(resp === 'Send success'){
          GetShellData(); 
        }

      })
      .fail(() =>{

      })

    }
  }
})

function GetShellData() {
  $.ajax({
    type:"GET", 
    url:"/getshelldata", 
    data:{"port":4448, "length":'4096'}, 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) =>{
    console.log(resp); 
    $("#DisplayShell").val($("#DisplayShell").val() + resp +">");
    var textarea = document.getElementById('DisplayShell');
    textarea.scrollTop = textarea.scrollHeight;
  })
  .fail(() =>{

  })
}
function CheckShellStatus(){
  $.ajax({
    type:"GET", 
    url: "/shellstatus", 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) =>{
    if(resp['message'] === 'fail'){
      id = window.setInterval(() => {}, 0);
      while (id) {
        window.clearInterval(id);
        id--;
      }
      GetShellData(); 
    }

  })
}
$("#ReverseShellModal").on('show.bs.modal', function(event){
  var $text = $('#DisplayShell'); 
  $text.scrollTop($text[0].scrollHeight);
  var button = $(event.relatedTarget); 
  var modal = $(this); 
  $(this).find("#InputCommand").val(''); 
  $(this).find("#DisplayShell").val(''); 
  var pocid = button.attr("pocid");
  $.ajax({
    type:"POST", 
    url:"/runshell", 
    data:{'pocid':pocid,"port":4448,"host":'75.119.131.210'}, 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done((resp) => {
    if(resp['message'] === "fail"){     
      $("#ToastErrorStartServer").show(); 
      $("#ToastErrorStartServer").toast('show');
    }else{
      window.setInterval(CheckShellStatus, 2000);
      
    }
  })
  .fail((error) =>{
   
  })


});

$("#ReverseShellModal").on('hidden.bs.modal', function(event){
  $.ajax({
    type: "POST", 
    url: "/closeport",
    data:{"port": 4448}, 
    beforeSend: (request) => {
      request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
    }
  })
  .done(()=>{

  })
  .fail(()=>{

  })

});
//


//end of dropdown button
function TableScanNextPage(){
  tblScanCurrentPage+=1;
  TableScanManagement(tblScanCurrentPage,tblScanRecoredPerPage,tblScanKeyword,tblScanCurrentSort,tblScanCurrentReverse);
};
function TableScanPrevPage(){
  tblScanCurrentPage-=1;
  TableScanManagement(tblScanCurrentPage,tblScanRecoredPerPage,tblScanKeyword,tblScanCurrentSort,tblScanCurrentReverse);
};
function TableScanPagination(arrayLength){

  if(arrayLength>0 && tblScanRecoredPerPage < arrayLength){
    if(tblScanCurrentPage==1){
          $("#table-scan-prev-page").attr("class","page-item disabled");
          $("#table-scan-next-page").attr("class","page-item");
        }
   else if(tblScanCurrentPage*tblScanRecoredPerPage>= arrayLength){
      $("#table-scan-next-page").attr("class","page-item disabled");   
      $("#table-scan-prev-page").attr("class","page-item");
    }
    else{
      $("#table-scan-next-page").attr("class","page-item");   
      $("#table-scan-prev-page").attr("class","page-item");
    }
  }
  else{
    $("#table-scan-next-page").attr("class","page-item disabled");   
    $("#table-scan-prev-page").attr("class","page-item disabled");
  }
  // Show 1-10 in 50 records

  let startPage=tblScanCurrentPage*tblScanRecoredPerPage-tblScanRecoredPerPage+1
  let stopPage=tblScanCurrentPage*tblScanRecoredPerPage;

  if(arrayLength<=0){
    $("#table-scan-page-info").text("No records");
  }
  else{
    if(startPage<1){
      startPage=1;
    }
    if(stopPage>arrayLength){
      stopPage=arrayLength;
    }
    let pageInfo="Show "+ String(startPage)+' - '+String(stopPage)+' in total '+String(arrayLength)+' records'
    $("#table-scan-page-info").text(pageInfo);
  }
  
}
function TableScanManagement(page,pageSize,txtSearch='',sortBy='',reverse=false){
  //
  //scannedPlatform =[]
  // let totalRecords= ;
  
  let displayTableData=[];
  for (let j=0;j<scannedPlatform.length;j++){
      for (let key in scannedPlatform[j]){
        let value=scannedPlatform[j][key];
        if(key!='supported-poc'){
          value=value.toLowerCase();
        }
        if (value!=null && value.includes(txtSearch.toLowerCase())){
          displayTableData.push(scannedPlatform[j]);
          break;
        }
      }
  }
  if (sortBy!=''){
    //Sort the data of table
    if(sortBy=='sp'){
      if(reverse==false){
          displayTableData.sort(function(a, b){
            return a['supported-poc'].length - b['supported-poc'].length;
          });
      }
      else{
        displayTableData.sort(function(a,b){
          return b['supported-poc'].length - a['supported-poc'].length;
        });
      }

     
    }
    else{
      if(reverse==false){
          displayTableData.sort(function(a, b){
            var x = a[sortBy].toLowerCase();
            var y = b[sortBy].toLowerCase();
            if (x < y) {return -1;}
            if (x > y) {return 1;}
            return 0;
         });
      }
      else{
        displayTableData.sort(function(a, b){
          var x = b[sortBy].toLowerCase();
          var y = a[sortBy].toLowerCase();
          if (x < y) {return -1;}
          if (x > y) {return 1;}
          return 0;
         });
      }
    }
   
  
  }
  let i=(page-1)*pageSize; //index of start record recaculated
  $('#table-scan-result').html('');
  for (i; i< displayTableData.length;i++) {
    pageSize-=1;
    if(pageSize==0) {break;}
    let newHost = displayTableData[i];
    let tableRow = $('<tr>');
            
    tableRow.append($('<td>', { style:'width:25%;' })
            .append($('<a>',{href:newHost['host'],target:"_blank",style:"color: white;"})
            .text(newHost['host']))
    );
    //tableRow.append($('<td>').text(poc['id']));
    tableRow.append($('<td>',{ style:'width:25%;'  }).text(newHost['title']));
    tableRow.append($('<td>',{ style:'width:25%;'  }).text(newHost['version']));
    let pocSupport='';
    let tableData=$('<td>',{ style:'width:25%; overflow: scroll;'  });
    for (let j = 0; j < newHost['supported-poc'].length; j++)  {
      tableData.append($('<a>',{href:'/poc?path='+newHost['supported-poc'][j],target:"_blank",class:'btn btn-outline-success'})
      .text(newHost['supported-poc'][j].replace("pocs\\","")+' '));
    }
    tableRow.append(tableData);

   
    $('#table-scan-result').append(tableRow);
  }

  TableScanPagination(displayTableData.length);
}
function showTableScanRecords(data){
  $("#cboxTableScanRecords").text(data);
  tblScanRecoredPerPage=parseInt(data);
  tblScanCurrentPage=1;
  TableScanManagement(tblScanCurrentPage,tblScanRecoredPerPage,tblScanKeyword,tblScanCurrentSort,tblScanCurrentReverse);
}
function ManagePieChart(pieChartIdName,title, dataPoints){
  // dataPoints=
  // [
  //   { label: "Email Marketing", y: 31 },
  //   { label: "Referrals", y: 7 },
  //   { label: "Twitter", y: 7 },
  //   { label: "Facebook", y: 6 },
  // ]
  var  chart =  new  CanvasJS.Chart(pieChartIdName,
    {
      title: {
        text: title
      },
      data: [{
          type: "pie",
          startAngle: 45,
          showInLegend: "true",
          legendText: "{label}",
          indexLabel: "{label} ({y})",
          yValueFormatString:"#,##0.#"%"",
          dataPoints: dataPoints
      }]

  });
chart.render();

}

$("#navDashboard").click(()=>{
  //Can use hide(), fadeOut(), slideUp()
  $("#divDashboard").show();
  $("#divReconnaisanse").hide();
  $("#divCheckPOC").hide();
  $("#divTarget").hide(); 
  $("#navDashboard").attr('class','btn btn-info form-control');
  $("#navReconnaisance").attr('class','btn btn-outline-info form-control');
  $("#navCheckPOC").attr('class', 'btn btn-outline-info form-control');
  $("#navTarget").attr('class', 'btn btn-outline-info form-control');
  InitDashboard();
}); 
$("#navReconnaisance").click(()=>{
  //Can use hide(), fadeOut(), slideUp() 
  $("#divDashboard").hide();
  $("#divReconnaisanse").show();
  $("#divCheckPOC").hide(); 
  $("#divTarget").hide(); 

  $("#navDashboard").attr('class','btn btn-outline-info form-control');
  $("#navReconnaisance").attr('class','btn btn-info form-control');
  $("#navCheckPOC").attr('class', 'btn btn-outline-info form-control');
  $("#navTarget").attr('class', 'btn btn-outline-info form-control');
  InitReconStartPage()
}); 

$("#navCheckPOC").click(()=>{
  //Can use hide(), fadeOut(), slideUp() 
  $("#divDashboard").hide();
  $("#divReconnaisanse").hide();
  $("#divCheckPOC").show(); 
  $("#divTarget").hide(); 
  $("#navTarget").attr('class', 'btn btn-outline-info form-control');
  $("#navDashboard").attr('class','btn btn-outline-info form-control');
  $("#navReconnaisance").attr('class','btn btn-outline-info form-control');
  $("#navCheckPOC").attr('class', 'btn btn-info form-control'); 
  InitReconResult()
}); 

$("#navTarget").click(()=>{
  //Can use hide(), fadeOut(), slideUp() 
  $("#divDashboard").hide();
  $("#divReconnaisanse").hide();
  $("#divCheckPOC").hide(); 
  $("#divTarget").show(); 
  $("#navTarget").attr('class', 'btn btn-info form-control');
  $("#navDashboard").attr('class','btn btn-outline-info form-control');
  $("#navReconnaisance").attr('class','btn btn-outline-info form-control');
  $("#navCheckPOC").attr('class', 'btn btn-outline-info form-control');
  InitTarget();
}); 

var options = {
	title: {
		text: "Total PoC Platforms: 9"
  },
  animationEnabled: true,
	data: [{
      type: "pie",
			startAngle: 45,
			showInLegend: "true",
			legendText: "{label}",
			indexLabel: "{label} ({y})",
			yValueFormatString:"#,##0.#",
			dataPoints: [
				{ label: "Liferay", y: 3 },
				{ label: "Sharepoint", y: 3 },
				{ label: "Wordpress", y: 3},

			]
	}]
};
$("#dashboard-piechart").CanvasJSChart(options);


var dataPointsGenerated=[
    { label: "Unsupported", y: 100 },
    { label: "Supported Exploit Sites", y: 0 }
  ];
var optionsPieScanPlatform = {
    title: {
      text: "Total sites:"+0
    },
    data: [{
        type: "pie",
        startAngle: 45,
        showInLegend: "true",
        legendText: "{label}",
        indexLabel: "{label} ({y})",
        yValueFormatString:"#,##0.#"%"",
        dataPoints: dataPointsGenerated
    }]
};
$("#pieChartScanPlatform").CanvasJSChart(optionsPieScanPlatform);

function TableScanSort(sortBy){
  tblScanCurrentReverse=!tblScanCurrentReverse;
  tblScanCurrentSort=sortBy;
  TableScanManagement(tblScanCurrentPage,tblScanRecoredPerPage,tblScanKeyword,tblScanCurrentSort,tblScanCurrentReverse);
}
function InitialPagination(){
  if (scannedPlatform.length<=tblScanRecoredPerPage){
    $("#table-scan-prev-page").attr("class","page-item disabled");
    $("#table-scan-next-page").attr("class","page-item disabled");
  }
 
}


