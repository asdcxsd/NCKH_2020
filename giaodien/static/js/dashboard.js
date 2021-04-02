


var listReconHistory=[];
var tblDashboardCurrentPage=1;
var tblDashboardRecoredPerPage=10;
var tblDashboardKeyword='';
var tblDashboardCurrentReverse=true;
var tblDashboardCurrentSort='';

function showTableDashboardRecords(data){
    $("#cboxTableDashboardRecords").text(data);
    tblDashboardRecoredPerPage=parseInt(data);
    tblDashboardCurrentPage=1;
    TableDashboardManagement(tblDashboardCurrentPage,tblDashboardRecoredPerPage,tblDashboardKeyword,tblDashboardCurrentSort);
}

$("#txtSearchDashboard").on("change paste keyup", function() {
    tblDashboardKeyword=$("#txtSearchDashboard").val();
    tblDashboardCurrentPage=1;
    TableDashboardManagement(tblDashboardCurrentPage,tblDashboardRecoredPerPage,tblDashboardKeyword,tblDashboardCurrentSort);
});
function TableDashboardSort(sortBy){
    tblDashboardCurrentReverse=!tblDashboardCurrentReverse;
    tblDashboardCurrentSort=sortBy;
    TableDashboardManagement(tblDashboardCurrentPage,tblDashboardRecoredPerPage,tblDashboardKeyword,tblDashboardCurrentSort,tblDashboardCurrentReverse);
  }
function TableDashboardManagement(page,pageSize,txtSearch='',sortBy='',reverse=false){
    
    let displayTableData=[];
    for (let j=0;j<listReconHistory.length;j++){
        for (let key in listReconHistory[j]){
            if (key=='status'){
                continue;
            }
          if (listReconHistory[j][key]!=null && listReconHistory[j][key].toLowerCase().includes(txtSearch.toLowerCase())){
            displayTableData.push(listReconHistory[j]);
            break;
          }
        }
    }
    if (sortBy!=''){

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
    $('#table-recon-history-result').html('');
    for (i; i< displayTableData.length;i++) {
      pageSize-=1;
      if(pageSize==0) {break;}
      let displayReconHistory = displayTableData[i];
      var reconURL = getTargetURL(displayReconHistory['target_id']);
      let tableRow = $('<tr>');
      tableRow.attr("id", displayReconHistory['_id']); 
      tableRow.append($('<td>').text(String(i+1)));
      tableRow.append($('<td>').text(reconURL));
      tableRow.append($('<td>').text(displayReconHistory['date_start']));
      tableRow.append($('<td>').text(displayReconHistory['date_end']));
      let tableData=$('<td>',{ style:'width:500px;'  });
      tableData.append(
      $('<button>', {type:"button" ,id: "btnReconHistory", class: 'btn btn-info','reconid':displayReconHistory['_id']})
                    .text('Send to Exploit')
      )
      tableRow.append(tableData);
      $('#table-recon-history-result').append(tableRow);
      
    }
    TableDashboardPagination(displayTableData.length);
  }
  function TableDashboardPagination(arrayLength){

    if(arrayLength>0 && tblDashboardRecoredPerPage < arrayLength){
      if(tblDashboardCurrentPage==1){
            $("#table-dashboard-prev-page").attr("class","page-item disabled");
            $("#table-dashboard-next-page").attr("class","page-item");
          }
     else if(tblDashboardCurrentPage*tblDashboardRecoredPerPage>= arrayLength){
        $("#table-dashboard-next-page").attr("class","page-item disabled");   
        $("#table-dashboard-prev-page").attr("class","page-item");
      }
      else{
        $("#table-dashboard-next-page").attr("class","page-item");   
        $("#table-dashboard-prev-page").attr("class","page-item");
      }
    }
    else{
      $("#table-dashboard-next-page").attr("class","page-item disabled");   
      $("#table-dashboard-prev-page").attr("class","page-item disabled");
    }
    // Show 1-10 in 50 records
  
    let startPage=tblDashboardCurrentPage*tblDashboardRecoredPerPage-tblDashboardRecoredPerPage+1
    let stopPage=tblDashboardCurrentPage*tblDashboardRecoredPerPage;
  
    if(arrayLength<=0){
      $("#table-dashboard-page-info").text("No records");
    }
    else{
      if(startPage<1){
        startPage=1;
      }
      if(stopPage>arrayLength){
        stopPage=arrayLength;
      }
      let pageInfo="Show "+ String(startPage)+' - '+String(stopPage)+' in total '+String(arrayLength)+' records'
      $("#table-dashboard-page-info").text(pageInfo);
    }
    
  }
  function TableDashboardNextPage(){
    tblDashboardCurrentPage+=1;
    TableDashboardManagement(tblDashboardCurrentPage,tblDashboardRecoredPerPage,tblDashboardKeyword,tblDashboardCurrentSort);
  };
  function TableDashboardPrevPage(){
    tblDashboardCurrentPage-=1;
    TableDashboardManagement(tblDashboardCurrentPage,tblDashboardRecoredPerPage,tblDashboardKeyword,tblDashboardCurrentSort);
  };

  function convertStatus(status){
    let tag=$('<span>',{class:'btn btn-info',style:"font-size: small;"}).text("Undefined");
    if (status==-1){
        tag.attr('class',"btn btn-danger").text("Failed");
    }
    else if (status==0){
        tag.attr('class',"btn btn-warning").text("Running");
    }
    else if (status==1){
        tag.attr('class',"btn btn-success").text("Success");
    }
    return tag;
  }