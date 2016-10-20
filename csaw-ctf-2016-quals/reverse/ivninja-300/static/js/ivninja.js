$(document).ready(function() {
	$.uploadPreview({
	input_field: "#image-upload",
	preview_box: "#image-preview",
	label_field: "#image-label"
	});

	$('#analyze').click(function() {
		var data = new FormData();
		var files = $("#image-upload").get(0).files;
		if (files.length != 1) {
			errorLog("Please pick an image to analyze.");
			return false;
		}
		data.append("image",files[0]);
		data.append("level",$("#slider").val());
		$.ajax({
			dataType: "json",
			type: "POST",
			url: "/analyze",
			contentType: false,
			processData: false,
			data: data,
			error: function (xhr, status, error) {
				if (error == "Too Many Requests") {
					errorLog("The server is rate-limited at 6 requests per five minutes. You should only need one attempt to succeed. <a href='/ivninja.zip'>Downlaod</a> the binary and analyze it to find out what you need to do to get the flag.");
				}
			}
		}).done(function(json) {
			if (json.ok) {
				$("#pname").html(json.name);
				$("#plevel").html(json.level);
				$("#pcp").html(json.cp);
				$("#php").html(json.hp);
				$("#pcpp").html(json.cp_percent);
				$("#pstars").html("⭐".repeat(json.stars));
				$("#prating").html(json.rating_desc);
				$("#pbivmin").html(json.battle_iv_min);
				$("#pbivmax").html(json.battle_iv_max);
				$("#phpivmin").html(json.hp_iv_min);
				$("#phpivmax").html(json.hp_iv_max);
				$('#results').show();
			} else {
				errorLog(json.error);	
			}
			console.log(json);
		});
	});

	$(':file').change(function(){
		$('#results').hide();
		var file = this.files[0];
		if (file.size > Math.pow(2,20)*2) 
		{
			errorLog("Image is too large. Please use files less than 2MB.");
			return false;
		}
	});

	$("#slider").slider({});

});


function errorLog(message) {
	$('#errorMessage').html(message);
	$('#errorModal').modal();
}
