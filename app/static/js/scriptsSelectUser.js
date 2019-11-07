$( document ).ready(function() {
    console.log( "ready! selectuser" );

    var theUrl = "./userlist"
    $.ajax({
        url: theUrl,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            console.log(res);
            var arrLen = res.length;
            var userArray = []
            for(i = 0; i < arrLen; i++){
            	//console.log(res[i].FirstName + " " + res[i].LastName);
            	var user = {
            		"FirstName": res[i].FirstName,
            		"LastName": res[i].LastName
            	}
            	userArray.push(user);
            	$("#selectUser").append(`<option value="${user.FirstName}">${user.FirstName} ${user.LastName}</option>`)
            }
            
        }
    });

    document.getElementById("getUserInfo").addEventListener("click", function(event){
  		event.preventDefault()

  		var userVal = $("#selectUser").val()
  		var nextUrl = "./userdata/" + userVal

  		$.ajax({
        url: nextUrl,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            console.log(res);
            
         
        }
    });

	});

});







