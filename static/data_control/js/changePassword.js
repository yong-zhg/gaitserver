$(document).ready(function(){
	$("#cp").click(function(){
    	var oldPassword = $("#oldPassword").val();
    	var newPassword = $("#newPassword").val();
    	var confirmPassword = $("#confirmPassword").val();
    	var storuser = sessionStorage.getItem("user");
		userobj = fromJSON(storuser);
    	var token = Application.data.token;
    	var storlogin = sessionStorage.getItem("login");
		loginobj = fromJSON(storlogin);
		 if ( !oldPassword ) {
    	    alert('请输入原始密码');
    	    return;
    	}
    	if ( !newPassword ) {
    	    alert('请输入新密码');
    	    return;
    	}
    	if ( !confirmPassword ) {
    	    alert('请确认新密码');
    	    return;
    	}
    	if ( newPassword != confirmPassword ) {
    	    alert('两次输入密码不匹配，请重新确认');
    	    return;
    	}
    	console.log(loginobj.data.token);
    	console.log(oldPassword);
    	console.log(newPassword);
	
    	postJSON('/user/password/update', {
    	    token: loginobj.data.token,
    	    user: {
    	        name: userobj.name,
    	        old_password: oldPassword,
    	        new_password: newPassword
    	    }
    	}, function(result) {
    	    if ( !result || !result.successful ) {
    	        alert('修改密码失败，原密码可能错误，请重新确认');
    	    }
    	    else {
    	        alert('修改密码成功');
    	        window.location.href = "../../login/login.html";
    	    }
    });
	})
});
