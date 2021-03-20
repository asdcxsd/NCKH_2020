'use strict';
var listPocs=[];
var currentPage=1;
var recoredPerPage=10;
var keyword='';
var currentReverse=true;
var currentSort='';

let isFetchingPocs = false;
$(document).ready(function () {
    fetchPocs();
    
});

function fetchPocs() {
    if (isFetchingPocs) {
        return;
    }

    $.ajax({
        type: 'GET',
        url: '/fetch-pocs',
        beforeSend: (request) => {
            request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
        },
    })
        .done((resp) => {
            $('#pocs-count').text(resp['pocs'].length);

            $('#pocs-display').text('');
            listPocs=resp['pocs'];
            TableManagement(currentPage,recoredPerPage,keyword,currentSort);

            isFetchingPocs = false;
        })
        .fail(() => {
            isFetchingPocs = false;
        });
}
function TableManagement(page,pageSize,txtSearch='',sortBy='',reverse=false){

    let displayTableData=[];
    for (let j=0;j<listPocs.length;j++){
        for (let key in listPocs[j]){
          if (listPocs[j][key]!=null && listPocs[j][key].includes(txtSearch)){
            displayTableData.push(listPocs[j]);
            break;
          }
        }
    }
    if (sortBy!=''){
      //Sort the data of table
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
    let i=(page-1)*pageSize; //index of start record recaculated
    $('#pocs-display').html('');
    for (i; i< displayTableData.length;i++) {
      pageSize-=1;
      if(pageSize==0) {break;}
      let poc = displayTableData[i];
      let tableRow = $('<tr>');

      tableRow.append(
          $('<td>', { 'data-poc-id': poc['id'], class: 'clickable' })
              .text(poc['id'].slice(0, 8))
              .click((e) => {
                 // exploreBot(e.currentTarget.getAttribute('data-poc-id'));
              })
      );
      //tableRow.append($('<td>').text(poc['id']));
      tableRow.append($('<td>').text(poc['appname']));
      tableRow.append($('<td>').text(poc['appversion']));
      tableRow.append($('<td>').text(poc['name']));
      let tableData=$('<td>',{ style:'width:25%;'  });
      tableData.append(
        $('<button>', {type:"button" , class: 'btn btn-info','poc-path': poc['path'],
        'data-toggle':"modal", 'data-target':"#DetailModal", 'data-poc-path':poc['path'],'data-poc-name':poc['name']
                })
                      .text('Detail')
      )
      tableData.append(
        $('<button>', {type:"button" , class: 'btn btn-danger',id:"DeletePOC","data-poc-name":poc['name'],
                       'data-toggle':'modal', 'data-target': "#DeleteModal"
                 })
                      .text('Detele')
      )
      tableRow.append(tableData);
      $('#pocs-display').append(tableRow);
    }
  
    ManagePaginationDisplay(displayTableData.length);



}
$("#DetailModal").on('show.bs.modal', function(event){
  var button = $(event.relatedTarget);
  var modal = $(this); 
  $(this).find(".modal-title").text('POC: '+ button.attr("data-poc-name"));
  $.ajax({
    type: 'POST',
    url: '/get-poc-info',
    data: { 'poc-path': button.attr("poc-path") },
    beforeSend: (request) => {
        request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
    }
    })
    .done((resp) => {
      if(resp["status"] === 0){
        let data = resp["data"]["info"]; 
        $.each(data, function(k, v) {
          //display the key and value pair
          let row = $("<row>"); 
          let div = $("<div>",{class:"col-12 col-md-9 pl-2 mt-3 pr-0"});
          let p = $("<p>", {style:"white-space: pre-line"}).text(k + ": " + v);
          div.append(p); 
          row.append(div); 
          $("#POC-Info").append(row);
      });
      }
    })

})
$("#DeleteModal").on('show.bs.modal', function(event){
  var button = $(event.relatedTarget);
  var modal = $(this); 
  $(this).find('#POCName').text("You want to delete the POC " + button.attr("data-poc-name") + "?");

})
$("#DetailModal").on('show.bs.modal', function(event){
  $("#POC-Info").html('');
})


function nextPage(){
    currentPage+=1;
    TableManagement(currentPage,recoredPerPage,keyword,currentSort);
  };
  function prevPage(){
    currentPage-=1;
    TableManagement(currentPage,recoredPerPage,keyword,currentSort);
  };
  function ManagePaginationDisplay(arrayLength){
     
    if(arrayLength>0 && recoredPerPage < arrayLength){
      if(currentPage==1){
            $("#prevPage").attr("class","page-item disabled");
            $("#nextPage").attr("class","page-item");
          }
    else if(currentPage*recoredPerPage>= arrayLength){
        $("#nextPage").attr("class","page-item disabled");   
        $("#prevPage").attr("class","page-item");
      }
      else{
        $("#nextPage").attr("class","page-item");   
        $("#prevPage").attr("class","page-item");
      }
    }
    else{
      $("#nextPage").attr("class","page-item disabled");   
      $("#prevPage").attr("class","page-item disabled");
    }
    // Show 1-10 in 50 records
  
    let startPage=currentPage*recoredPerPage-recoredPerPage+1
    let stopPage=currentPage*recoredPerPage;
  
    if(arrayLength<=0){
      $("#pageInfo").text("No records");
    }
    else{
      if(startPage<1){
        startPage=1;
      }
      if(stopPage>arrayLength){
        stopPage=arrayLength;
      }
      let pageInfo="Show "+ String(startPage)+' - '+String(stopPage)+' in total '+String(arrayLength)+' records'
      $("#pageInfo").text(pageInfo);
    }
    
  }
// Xu ly Modal
$('#pocModal').on('show.bs.modal', function (event) {
    var resultDiv=$('#result'); 
    resultDiv.html('')
    var button = $(event.relatedTarget) // Button that triggered the modal
    var poc_path = button.data('poc-path') // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('.modal-title').text(' POC: ' + button.data('poc-name'))
    $.ajax({
        type: 'POST',
        url: '/get-poc-info',
        data: { 'poc-path': poc_path },
        beforeSend: (request) => {
            request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
        },
    })
        .done((resp) => {

            if (resp['status'] === 0) {
                let data = resp['data'];
                $('#poc-info-display').text(data['info']);
                //Xử lý divModuleOptions
                if (isEmptyDict(data['options'])){
                  $('#divModuleOptions').hide();  
              }
              else
              {
                  $('#divModuleOptions').show();  
                  let moduleOptions=$('#module-options');
                  moduleOptions.html('');
                  for (let k in data['options']) {
                      let key = data['options'][k][0];
                      let defaultValue=data['options'][k][1];
                      moduleOptions.append(
                          $('<div>', { class: 'form-group' })
                              .append($('<label>', { class: 'col-form-label',for:key+'-name','data-toggle':"tooltip",'data-placement':"top",'title':data['options'][k][3] }).text(key))
                              .append($('<input>', { class: 'form-control',id:key+'-value',type:'text',value:defaultValue }))
                      );
                  }
              }
               
                let attackModesDiv=$('#attack-mode-button');
                attackModesDiv.html('');
                let modes=data['modes'];
                if(modes.includes("verify")){
                    attackModesDiv.append($('<button>', {type:"button", class:"btn btn-info", id:"verify"  })
                    .text('Verify')
                    .click((e) => {
                        verifyButtonClicked();
                    })
                    );
                }

              
                if(modes.includes("attack")){
                  attackModesDiv.append($('<button>', {type:"button", class:"btn btn-warning", id:"attack"  })
                  .text('Attack')
                  .click((e) => {
                      attackButtonClicked();
                  })
                  );
              }
                if(modes.includes("shell")){
                  $('#divPayloadOptions').show(); 

                    attackModesDiv.append($('<button>', {type:"button", class:"btn btn-success", id:"shell"  })
                    .text('Shell')
                    .click((e) => {
                        shellButtonClicked();
                    })
                    );

                     //prepare lhost and lprot 
                    //Set bottom beacuse it need to generate lport,lhost input tag first as well as ShellMode is open
                    let isServerOnline=data['isServerOnline'];
                    if (isServerOnline.length>0){
                        $("#lhost-value").val(isServerOnline[0]);
                        $("#lhost-value").prop('disabled', true);
                        $("#lport-value").val(isServerOnline[1]);
                        $("#lport-value").prop('disabled', true);
                        $("#lhost-value").attr({
                          "data-toggle" : "tooltip",
                          "data-placement" : "top",
                          title:"Server is active. Please stop server so that you can customize Lhost"
                        });
                        $("#lport-value").attr({
                          "data-toggle" : "tooltip",
                          "data-placement" : "top",
                          title:"Server is active. Please stop server so that you can customize Lhost"
                        });
                    }
                }
                attackModesDiv.append($('<input>', {type:"hidden", class:"form-control",id:'hidden-input' }).text('hidden tag'));
                
                
            }
            else{

            }
        })
        .fail(() => {
            
        });


  })
  // Xu ly Attack-mode-click
function verifyButtonClicked() { 
    var data = getAllInputData()
    $.ajax({
        type: 'POST',
        url: '/verify-mode',
        data: data,
        beforeSend: (request) => {
            request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
        },
    })
        .done((resp) => {
            let result=resp['data'];
            
            ShowResult(result);
            
        })
        .fail(() => {
           
        });
};
function attackButtonClicked() { 
  var data = getAllInputData()
  $.ajax({
      type: 'POST',
      url: '/attack-mode',
      data: data,
      beforeSend: (request) => {
          request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
      },
  })
      .done((resp) => {
          let result=resp['data'];
          
          ShowResult(result);
          
      })
      .fail(() => {
         
      });
};
function shellButtonClicked() { 
    let lhost=$('#lhost-value').val();
    let lport=$('#lport-value').val();
    if (lhost =='' || lport ==""){
      alert("Shell mode requires Lhost and Lport");
      return;
    }
    var data = getAllInputData()
    $.ajax({
        type: 'POST',
        url: '/shell-mode',
        data: data,
        beforeSend: (request) => {
            request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
        },
    })
        .done((resp) => {
            let result=resp['data'];
            ShowResult(result);
            
        })
        .fail(() => {
           
        });
};
function getAllInputData(){
    var data={}
    $("#pocModal input:not([type=hidden])").each(function(e){	
        
        let id = this.id;
        if(this.value!=''){
            data[id]=this.value;
        }      
        // show id 
        // console.log("#"+id);
        // // show input value 
        // console.log(this.value);
        // disable input if you want
        //$("#"+id).prop('disabled', true);
      });
    return data;
}

function showNumRecords(data){
    $("#dropdownMenuButton").text(data);
    recoredPerPage=parseInt(data);
    currentPage=1;
    TableManagement(currentPage,recoredPerPage,keyword,currentSort);
  }
  $("#txtSearchScanPlatform").on("change paste keyup", function() {
    keyword=$("#txtSearchScanPlatform").val();
    TableManagement(currentPage,recoredPerPage,keyword,currentSort);
  });
function isEmptyDict(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}
function ShowResult(result){
  let ret=false;
  let resultDiv=$('#result');
  if (!isEmptyDict(result)) {
      ret=true;
  }

  let dt = new Date().toLocaleString();
  // let time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
  let titleResult='Target '+result['target']+' '+result['mode']+' at '+dt;

  //Result print from here
  for (let k in result){
      if (k=='report'){
          continue;
      }
      let row =$('<div>', { class:"col-md-12 px-2"})
      .append($('<h5>', { class:"btn btn-outline-success mr-4"}).text(k))
      .append($('<h5>', { class:"btn btn-outline-info"}).text(result[k]));
      resultDiv.prepend(row);
  }
  resultDiv.prepend($('<div>', { class:"col-md-12 pl-2 pr-0",style:'display:block;text-align:center;' })
  .append($('<h5>').text(titleResult)));
  return ret;
}