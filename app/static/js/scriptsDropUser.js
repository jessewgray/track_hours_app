$( document ).ready(function() {
    console.log( "ready! select user to drop" );

    //on page load - adds options to the drop down
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

        //on change of the dropdown - auto updates the user id
        $("#selectUser").on("change", function(){
            var theSelectedUser = $("#selectUser").val();
             var userUrl = "/userdata/" + theSelectedUser
            $.ajax({
                url: userUrl,
                type: 'GET',
                dataType: 'json', // added data type
                success: function(res) {
                    console.log(res);
                    var pastePersonId = res[0].PersonId;
                    var fName = res[0].FirstName;
                    var lName = res[0].LastName;
                    $("#userId").val(pastePersonId);
                    $("#fName").val(fName);
                    $("#lName").val(lName);
                    
                    }
                });
                
            });

});