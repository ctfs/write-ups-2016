var crypto = require('crypto');
var fs = require('fs');
var path = require('path');

// constants
const HMAC_KEY = 'luvmarkdown';

const UPLOAD_DIR = path.join(__dirname, '/src/uploads');
const INITIAL_FILES_DIR = path.join(__dirname, '/initial_files');


// ensure that uploads directory exists
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR);
}


// helper functions for files
function generateFilename(contents) {
  return crypto.createHmac('sha256', HMAC_KEY)
    .update(contents, 'utf8')
    .digest('hex');
}


// move files in initial_files into uploads
var files = fs.readdirSync(INITIAL_FILES_DIR);

files.forEach(function (oldFilename) {
  // load file contents
  var oldFilepath = path.join(INITIAL_FILES_DIR, oldFilename);
  var contents = fs.readFileSync(oldFilepath, {encoding: 'utf8'});
  contents = contents.replace(/\r\n/g, '\n');  // normalize newlines

  // find destination path
  var filename = generateFilename(contents);
  var filepath = path.join(UPLOAD_DIR, filename);

  fs.writeFileSync(filepath, contents, {encoding: 'utf8'});
});
