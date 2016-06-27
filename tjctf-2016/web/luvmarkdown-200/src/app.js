const express = require('express');
const bodyParser = require('body-parser');
const csp = require('helmet-csp');
const session = require('express-session');

const child_process = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');


// constants
const HMAC_KEY = 'luvmarkdown';
const SESSION_SECRET = '<removed>';
const RECENT_PAGES_SIZE = 15;
const MAX_TEXT_LEN = 4096;
const PROCESS_FORCE_TIMEOUT = 3500;  // timeout to kill phantomjs process

const UPLOAD_DIR = path.join(__dirname, '/uploads');
const STATIC_DIR = path.join(__dirname, '/static');
const TEMPLATES_DIR = path.join(__dirname, '/templates');
const FETCH_SCRIPT = path.join(__dirname, '/fetch.js');


// ensure that uploads directory exists
if (!fs.existsSync(UPLOAD_DIR)) {
  console.warn("Warning: upload directory doesn't exist. Make sure to run setup.js.");
}


// helper functions for files
function generateFilename(contents) {
  return crypto.createHmac('sha256', HMAC_KEY)
    .update(contents, 'utf8')
    .digest('hex');
}

function validateFilename(filename) {
  return (/^[0-9a-f]{64}$/).test(filename);
}

function handleFileExists(filename, successCallback, errorCallback) {
  if (!validateFilename(filename)) {
    errorCallback('invalid filename!');
    return;
  }
  var filepath = path.join(UPLOAD_DIR, filename);
  fs.access(filepath, fs.R_OK, function (err) {
    if (err) {
      errorCallback('file not found!');
      return;
    }
    successCallback();
  });
}


// begin express app
var app = express();

app.use(csp({
  scriptSrc: ["'self'"],
  styleSrc: ["'self'"]
}));

app.use(session({
  secret: SESSION_SECRET,
  resave: false,
  saveUninitialized: false
}));

app.use(bodyParser.json());

app.use('/static', express.static(STATIC_DIR));


// serve static html pages
app.get('/', function (req, res) {
  res.sendFile('index.html', { root: TEMPLATES_DIR });
});

app.get('/view/:filename', function (req, res) {
  res.sendFile('view.html', { root: TEMPLATES_DIR });
});


// create a new paste (returns json)
app.post('/', function (req, res) {
  if (!req.body || typeof req.body.text !== 'string') {
    return res.status(400).json({
      error: 'request body empty'
    });
  }

  var contents = req.body.text;
  if (contents.length > MAX_TEXT_LEN) {
    return res.status(400).json({
      error: 'text too long'
    });
  }

  contents = contents.replace(/\r\n/g, '\n');  // normalize newlines
  var filename = generateFilename(contents);
  var filepath = path.join(UPLOAD_DIR, filename);

  fs.writeFile(filepath, contents, function (err) {
    if (err) {
      return res.status(500).json({
        error: 'error saving file'
      });
    }
    return res.status(200).json({
      success: true,
      filename: filename
    });
  });
});


// get raw paste (returns markdown)
app.get('/raw/:filename', function (req, res) {
  var filename = req.params.filename;
  handleFileExists(filename, function () {
    res.sendFile(filename, {
      root: UPLOAD_DIR,
      headers: {
        'Content-Type': 'text/markdown'
      }
    }, function (err) {
      if (err) {
        return res.status(500).send('error sending file');
      }
    });
  }, function (err) {
    return res.status(404).send(err);
  });
});


// get recent pages (returns json)
app.get('/recent-pages', function (req, res) {
  var recent_pages = req.session.recent_pages || [];
  res.status(200).json({
    recent_pages: recent_pages
  });
});


// update recent pages (returns json)
app.post('/recent-pages/:filename', function (req, res) {
  var filename = req.params.filename;
  handleFileExists(filename, function () {
    var recent_pages = [ filename ];
    if (req.session.recent_pages) {
      recent_pages = recent_pages.concat(
        req.session.recent_pages.slice(0, RECENT_PAGES_SIZE - 1));
    }
    req.session.recent_pages = recent_pages;
    res.status(200).json({ success: true });
  }, function (err) {
    res.status(404).json({ error: err });
  });
});


// report paste (returns html)
app.post('/report/:filename', function (req, res) {
  var filename = req.params.filename;
  handleFileExists(filename, function () {
    // start process
    var child = child_process.execFile(
      'phantomjs',
      [ FETCH_SCRIPT, filename ],
      { timeout: PROCESS_FORCE_TIMEOUT },
      function (err, stdout, stderr) {
        if (err) {
          console.error('app.js: process error: ' + String(err).trim());
          console.error('>> printing stdout\n' + stdout.trim() + '\n>> end');
          res.status(500).send('Internal Server Error');
        } else {
          res.sendFile('reported.html', { root: TEMPLATES_DIR });
        }
      }
    );

    console.log('app.js: spawned process for filename', filename);

    child.on('exit', function (code, signal) {
      console.log('app.js: process exited with code ' + code + ', signal ' + signal);
    });

  }, function (err) {
    res.status(404).send(err);
  });
});


var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);
});
