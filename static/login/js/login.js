function processLoginResult (result) {
     if ( !result || !result.successful ) {
                console.log(result);
                alert('Error!');
                return;
            }
    else{
        window.location.href = "../data_control/pages/index.html";
        sessionStorage.setItem('login', toJSON(result));
    }
}

function doLogin(username, password, rememberMe) {
	var postdata = {
		user: {
                name: username,
                password: password
            }
	}
    $.ajax({
        type:"POST",
        url:"/user/login",
        data:JSON.stringify(postdata),
        dataType:"json",
        success:function(result){
            processLoginResult(result);
        }
    });
}

$(".login").click(function(){
    var username = $("#username").val();
    var password = $("#password").val();
    var rememberMe = $("#remember").is(':checked');
    doLogin(username, password, rememberMe);
})