<style>
	div#about b {font-size:120%;}
</style>
	<div id="contents">
		<div id="about">
			<h1>List of Registered Account</h1>
		</div>
	</div>
<script>
	function listing(){
		$.get("./mod/list.php",function(d){
			draw_table(d);
		});
	}
	function draw_table(d){
		$.each(d, function(i,d){
			$('div#about').append("<p>uid : <b>"+d[0]+"</b> / userid : <b>"+d[1]+"</b></p><hr />");
		})
	}
	$(function(){listing();})
</script>
