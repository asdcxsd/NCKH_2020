
var listResult=[]
$(document).ready(function () {
    //Nếu khởi tạo dữ liệu trong này thì web trông load bị chậm
    
});
InitialSinglePocData();
function InitialSinglePocData(){
    var poc_path=$('#poc-path').val();
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
                $("#pocLabel").text(data['poc-path']);
                displayPocInfo(data['info']);
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
                //Xu ly 3-mode-attack
                let attackModesDiv=$('#attack-mode-button');
                attackModesDiv.html('');
                let modes=data['modes'];
                if(modes.includes("verify")){
                    attackModesDiv.append($('<button>', {type:"button",style:'width:30%;', class:"btn btn-info ml-2", id:"verify"  })
                    .text('Verify')
                    .click((e) => {
                        verifyButtonClicked();
                    })
                    );
                }

                if(modes.includes("attack")){
                    attackModesDiv.append($('<button>', {type:"button",style:'width:30%;', class:"btn btn-warning ml-2", id:"attack"  })
                    .text('Attack')
                    .click((e) => {
                        attackButtonClicked();
                    })
                    );

                }
                if(modes.includes("shell")){
                    $('#divPayloadOptions').show(); 
                    attackModesDiv.append($('<button>', {type:"button",style:'width:30%;', class:"btn btn-success ml-2", id:"shell"  })
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
                        // /data-toggle="tooltip" data-placement="top" title="Tooltip on top"
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
};
$('#chkBoxFileTarget').change(function() {
    var isTargetFile = $('#chkBoxFileTarget').is(":checked");   
    if(isTargetFile==true){    
        $('#target-value').hide();
        $('#multiFiles').show();
    }
    else{
        $('#target-value').show();
        $('#multiFiles').hide();
    }

});
function displayPocInfo(data){
    $('#poc-info-display').html('');
    if (isEmptyDict(data)){
        $('#poc-info-display').text("No Description");
        return;
    }
    for (let key in data){
        $('#poc-info-display').append($("<tr>")
            .append($("<td>").text(key))
            .append($("<td>").text(data[key]))
            );
    }
 
}
// Xu ly Attack-mode-click
function verifyButtonClicked() { 
    $([document.documentElement, document.body]).animate({
        scrollTop: $("#result").offset().top
    }, 2000);
    var isTargetFile = $('#chkBoxFileTarget').is(":checked");   
    var data = getAllInputData();
    let targets=[]
    if(isTargetFile==true){    
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles').files.length;
        if(ins == 0) {
            alert("Please choose file");
            return;
        }       
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles').files[x]);
        }
        
        $.ajax({
            url: '/target-file', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            beforeSend: (request) => {
                request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
            },
        })
            .done((response) => {
                targets= response['targets'];
                let flag=false;
                for ( let i in targets) {
                    data['target-value']=targets[i];
                    let result=executeVerifyMode(data);
                    if(flag==false){
                        flag=result;
                    }
                }
                if (flag==false) {
                    $('#result-export').show();  
                }
                else{
                    $('#result-export').hide();
                    resultDiv.html("No result");
                }

                
            })
            .fail(() => {

            });
    }
    else{
        executeVerifyMode(data);
    }
    return;

    
};
function executeVerifyMode(data){
    let ret=false;
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
            ret=ShowResult(result);
        })
        .fail(() => {
           
        });
        return ret;
}
function attackButtonClicked() { 
    var isTargetFile = $('#chkBoxFileTarget').is(":checked");   
    if (isTargetFile==true){
        alert("Target file only supports Verify mode");
        return;
    }
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
            ret=ShowResult(result);
            
        })
        .fail(() => {
           
        });
  };
function shellButtonClicked() { 
    var isTargetFile = $('#chkBoxFileTarget').is(":checked");   
    if (isTargetFile==true){
        alert("Target file only supports Verify mode");
        return;
    }
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
            ret=ShowResult(result);
            
        })
        .fail(() => {
           
        });
};
function ShowResult(result){
    let ret=false;
    let resultDiv=$('#result');
    if (!isEmptyDict(result)) {
        ret=true;
        listResult.push(result);
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
function getAllInputData(){
    var data={}
    $("#divExploit input:not([type=hidden])").each(function(e){	
        
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

function isEmptyDict(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}
$('#btnHtmlExport').click(()=>{
 
    $.ajax({
        type: 'POST',
        url: '/html-export',
        data: JSON.stringify({ data: listResult }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        beforeSend: (request) => {
            request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
        },
    })
        .done((resp) => {
   
            
        })
        .fail(() => {
           
        });

});