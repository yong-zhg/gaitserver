$(document).ready(function(){
	var storlogin = sessionStorage.getItem("login");
	loginobj = fromJSON(storlogin);
    console.log(loginobj);
	postJSON('/user/info', 
	{
        token: loginobj.data.token
    }, 
    function(result) {
        if ( !result || !result.successful ) {
            alert('请求用户信息失败');
            return;
        }
        else{
        	sessionStorage.setItem('user',toJSON(result.user));
        	updatehtml()
        }
    });
    updatehtml = function() {
    	var storuser = sessionStorage.getItem("user");
		userobj = fromJSON(storuser);
		console.log(userobj);
		var name = $("#input-name").val(userobj.name);
		var real_name = $("#input-real-name").val(userobj.real_name);
		var height = $("#input-height").val(userobj.height);
		var weight = $("#input-weight").val(userobj.weight);
		var sex = $("#input-sex").val(userobj.sex);
		var birthday = $("#input-birthday").val(userobj.birthday);
		var email = $("#input-email").val(userobj.email);
    };
    $("#changeinfo").click(function(){
    	var storuser = sessionStorage.getItem("user");
		userobj = fromJSON(storuser);
        userobj.name = $("#input-name").val();
        userobj.real_name = $("#input-real-name").val();
        userobj.height = $("#input-height").val();
        userobj.weight = $("#input-weight").val();
        userobj.sex = $("#input-sex").val();
        userobj.birthday = $("#input-birthday").val();
        userobj.email = $("#input-email").val();
    	postJSON('/user/info/update', 
    	{
    	    token: loginobj.data.token,
    	    user: userobj
    	}, function(result) {
    	    if ( !result || !result.successful ) {
    	        alert('请求用户信息失败');
    	    }
    	    else {
    	        alert('修改用户信息成功');
                sessionStorage.setItem('user', toJSON(userobj));
    	    }
    	});
})

});