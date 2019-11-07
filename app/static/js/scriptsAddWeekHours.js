$( document ).ready(function() {
    console.log( "ready! addWeekHours" );

    //get the users and add to dropdown options
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

    //after selecting user - the rate will auto fill in
    $("#selectUser").on("change", function(){
    	var theSelectedUser = $("#selectUser").val();
 		var userUrl = "/userdata/" + theSelectedUser
		$.ajax({
        	url: userUrl,
        	type: 'GET',
        	dataType: 'json', // added data type
        	success: function(res) {
            	console.log(res);
            	var pasteUserRate = res[0].Rate;
            	var pastePersonId = res[0].PersonId;
            	console.log(pasteUserRate);
            	$("#empRate").val(pasteUserRate);
            	$("#personId").val(pastePersonId)
        		}
    		});
    		
    	});

   }) //end of jquery ready function

	