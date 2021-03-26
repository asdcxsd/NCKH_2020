$(document).ready(function (e) {
    InitTools(); 
    renderAvailableTool(); 

});
function RenderTools(listTools){
    $("#Tools-display").html(''); 
    for(i = 0 ; i < listTools.length; i++){
        var tool = listTools[i]; 
        var row = $("<tr>");
        row.append($("<td>").text(String(i+1))); 
        row.append($("<td>").text(tool['name'])); 
        row.append($("<td>").text(tool['type'])); 
        if(tool['service']){
            row.append($("<td>").text(tool['service'])); 
        }else{
            row.append($("<td>").text('none'));
        }
        let tableData=$('<td>',{ style:'width:25%;'  });
        tableData.append(
          $('<button>', {type:"button" , class: 'btn btn-danger DeleteTools', "toolname": tool['name'], 'data-toggle':"modal", 'data-target':'#DeleteToolmodal'})
                        .text('Detele')
        )
        row.append(tableData); 
        $("#Tools-display").append(row); 
        $("#Tools-display").show(); 
    }
}
function InitTools(){
    $.ajax({
        type:"GET", 
        url: "/listtool", 
        beforeSend: (request) => {
          request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
        }
    })
    .done((resp) => {
        if(resp['message'] == "success"){
             listTools = resp['data']; 
             RenderTools(listTools); 
        }
    })
}
function renderAvailableTool(){
    $.ajax({
      type:"GET", 
      url: "/getavailabletool", 
      async: false,
      beforeSend: (request) => {
        request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
      },
      success: (resp) => {
        if(resp['message'] === 'success'){
          $("#AvailableTools").html(''); 
          listTools = resp['data']; 
          for(i = 0; i < listTools.length; i ++){
            var tool = listTools[i]; 
            var option = $("<option>");
            option.attr("toolname",tool); 
            option.text(tool); 
            $("#AvailableTools").append(option);
          }
        }
      }
    })
  }
$(document).on('click', "#ImportTool", (e) => {
    var toolname = $("#AvailableTools option:selected").attr("toolname");
    $.ajax({
        type:"POST", 
        url: "/uploadtool", 
        data: {"tool": toolname}, 
        beforeSend: (request) => {
          request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
        }
    })
    .done((resp) => {
        if(resp['message'] == "success"){
            $("#ToastImportToolSuccess").show(); 
            $("#ToastImportToolSuccess").toast('show');
            InitTools(); 
        }else{ 
            $("#ToastImportToolError").show(); 
            $("#ToastImportToolError").toast('show');
        }
    })

})
$(document).on('click', ".DeleteTools", (e)=>{
    var button = $(e.currentTarget); 
    var toolname = button.attr("toolname"); 
    $.ajax({
        type:"DELETE", 
        url: "/deletetool", 
        data: {"tool": toolname}, 
        beforeSend: (request) => {
          request.setRequestHeader('X-CSRFToken', $("#csrf_token").val()); 
        }
    })
    .done((resp) => {
        if(resp['message'] == 'success'){ 
            $("#ToastDeleteToolSuccess").show(); 
            $("#ToastDeleteToolSuccess").toast('show');
            InitTools(); 
        }else{
            $("#ToastDeleteToolError").show(); 
            $("#ToastDeleteToolError").toast('show');
        }
    })
})