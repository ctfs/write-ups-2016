<?php if (!isset($_SESSION['login'])) die("<script>window.location.href='?p=pages/login';</script>");
?><div id="contents">
		<div class="section">
			<h1>MyPage</h1>
			<p> Reset your Password
			</p>
			<form action="" method="post" class="message" onsubmit="return modify(this);">
				<input type="hidden" name="uidx" value="<?=$_SESSION['login'][0]?>"/>
				<input type="text" minlength="4" readonly name="userid" value="<?=$_SESSION['login'][1]?>" onFocus="this.select();" onMouseOut="javascript:return false;"/>
				<input type="text" minlength="6" name="userps" value="original password" onFocus="this.select();" onMouseOut="javascript:return false;"/>
				<input type="text" minlength="6" name="change" value="new password" onFocus="this.select();" onMouseOut="javascript:return false;"/>
				<input type="submit" value=change />
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
	function modify(f){
		if (f.userid.value.length < 4) {alert("id leng err"); return false;}
		if (f.userps.value.length < 6) {alert("ps leng err"); return false;}
		data = JSON.stringify(arrange($(f).serializeArray()));
		$.post("./mod/modify.php",data,function(d){
			if (d == "success") alert("okay"); else alert("wrong");
			window.location.href="?p=pages/mypage";
		});
		return false;
	}
</script>
