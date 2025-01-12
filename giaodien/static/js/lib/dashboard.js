'use strict';
$(document).ready(function(){
    get_dashboard_info();
    get_process_info();
    get_poc_info()
});
function get_dashboard_info(){
    $.ajax({
        type: "GET", 
        url : "/getdashboard", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
      })
    .done((resp) => {
        if(resp['message'] == 'success'){
            var data = resp['data'];
            $(".target").text(data['target']); 
            $(".vulnerability").text(data['vulnerability']); 
            $(".account").text(data['account']); 
            $(".process").text(data['process']); 
        }
    })
}

function get_process_info(){
    $.ajax({
        type: "GET", 
        url : "/getprocessdashboard", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
      })
    .done((resp) => {
        if(resp['message'] == 'success'){
            new Chart(document.getElementById("myAreaChart"), {
                type: 'line',
                data: {
                labels: ["1/2021","2/2021","3/2021","4/2021","5/2021","6/2021","7/2021","8/2021","9/2021","10/2021","11/2021","12/2021"],
                datasets: [{ 
                    data: resp["data"],
                    label: "Tiến trình đã chạy theo tháng",
                    borderColor: "#3e95cd",
                    fill: false
                    }
                ]
                },  
            });
        }
    })
}

function get_poc_info(){
    $.ajax({
        type: "GET", 
        url : "/getpocinfo", 
        beforeSend: (request) =>{
          request.setRequestHeader("X-CSRFToken", $('#csrf_token').val()); 
        }
      })
    .done((resp) => {
        if(resp['message'] == 'success'){
            
            new Chart(document.getElementById("PocChart"), {
                type: 'pie',
                data: {
                  labels: resp['labels'],
                  datasets: [{
                    label: "Population (millions)",
                    backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", "#6495ED", "#808000"],
                    data: resp['data']
                  }]
                },
                options: {
                  title: {
                    display: true,
                    text: 'Tổng hợp mã khai thác có trong hệ thống'
                  }
                }
            });
            
        }
    })
}