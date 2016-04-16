	<div id="contents">
		<div class="section">
			<h1>Login</h1>
			<p> Login page :D
			</p>
			<form action="" method="post" class="message" onsubmit="return login(this);">
				<input type="hidden" name="uidx" value=""/>
				<input type="text" minlength="4" name="userid" value="userid" onFocus="this.select();" onMouseOut="javascript:return false;"/>
				<input type="text" minlength="6" name="userps" value="userps" onFocus="this.select();" onMouseOut="javascript:return false;"/>
				<input type="submit" value=Login />
			</form>
		</div>
		<div class="section contact">
			<p>
				For Inquiries Please Call: <span>877-433-8137</span>
			</p>
			<p>
				Or you can visit us at: <span>ZeroType<br> 250 Business ParK Angel Green, Sunville 109935</span>
			</p>
		</div>
	</div>
<script>
	function get_hash(d){
		var data = "";
		return data;
	}
	function arrange(data){
		var list = [];
		$.each(data, function(i,d){list.push(d.value);})
		return list;
	}
	function login(f){
		if (f.userid.value.length < 4) {alert("id leng err"); return false;}
		if (f.userps.value.length < 6) {alert("ps leng err"); return false;}
		data = JSON.stringify(arrange($(f).serializeArray()));
		$.post("./mod/login.php",data,function(d){
			if (d != "success") alert("login failed..");
			window.location.href="?p=pages/home";
		});
		return false;
	}
</script>
