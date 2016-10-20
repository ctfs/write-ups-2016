var express = require('express');
var morgan = require('morgan');
var path = require('path');
var multer = require('multer');
var ratelimit = require('express-rate-limit');
var crypto = require('crypto');
var exec = require('child_process').exec;

function randomHex(len) { return crypto.randomBytes(Math.ceil(len/2)).toString('hex').slice(0,len); }

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, randomHex(10) + '-' + Date.now() + '.png');
  }
})

var upload = multer({ storage : storage });
//app.enable('trust proxy'); // only if you're behind a reverse proxy 

var app = express();
app.use(morgan('combined'));

var limiter = new ratelimit({
  windowMs: 5*60*1000, // 5 minutes 
  max: 6, // 6 requests
  delayMs: 0 // disable delaying - full speed until the max limit is reached 
});

app.get('/',function(req, res) {
	res.sendFile(path.join(__dirname, './static', 'index.html'));
});

app.post('/analyze', limiter, upload.single('image'), function(req, res) {
	var level = parseInt(req.body.level);
	if (level < 1 || level > 40) {
		res.send('{"ok": false, "error": "Invalid trainer level"}');
		return;
	}
	var cmd = "./ivninja " + level + " " + req.file.path
	exec(cmd, function(error, stdout, stderr) {
		res.send(stdout);	
	});
});

app.use(express.static('static'));

app.set('port', process.env.PORT || 8000);

var server = app.listen(app.get('port'), function() {
    console.log("Server started.");
});
