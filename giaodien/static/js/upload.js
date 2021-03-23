$(document).ready(function (e) {
    $('#upload').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles').files.length;

        if(ins == 0) {
            $('#msg').html('<span style="color:red">Select at least one file</span>');
            return;
        }
        
        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles').files[x]);
        }

        var call = $.ajax({
            url: '/uploadfile', // point to server-side URL
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
            call.done((response) => {
                $('#msg').html('<span style="color:white">Upload Successfully</span>');
            })
            call.fail((response) => {
               console.log(response.message); // display error response
            });
    });
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
function isEmptyDict(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}