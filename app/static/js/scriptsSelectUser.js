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
  		var nextUrl = "./showuserhours/" + userVal

  		$.ajax({
        url: nextUrl,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            $("#hoursTable tbody td").remove();
            console.log(res);
            for(i=0; i < res.length; i++){
            var getObj = res[i];
            var fDate = getObj.FromDate;
            var frDate = fDate.slice(4,16);
            var tDate = getObj.ToDate;
            var toDate = tDate.slice(4,16);
            var pId = getObj.PersonID;
            var lName = getObj.LastName; 
            var fName = getObj.FirstName;
            var rate = getObj.Rate;
            var totHours = getObj.TotHours;
            var regHours = getObj.RegHours;
            var otHours = getObj.OtHours;
            var regPay = getObj.RegPay;
            var otPay = getObj.OtPay;
            var totPay = getObj.TotPay;
            
            $("#hoursTable tbody").append(`<tr><td>${frDate}</td><td>${toDate}</td><td>${pId}</td><td>${lName}</td><td>${fName}</td><td>$${rate}</td><td>${totHours}</td><td>${regHours}</td><td>${otHours}</td><td>$${regPay}</td><td>$${otPay}</td><td>$${totPay}</td></tr>`)

        }
    }
    });

	});

});







