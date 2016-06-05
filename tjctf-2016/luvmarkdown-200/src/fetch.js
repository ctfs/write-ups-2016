var page = require('webpage').create();
var system = require('system');

// TODO: change these as appropriate
const HOST = 'http://localhost:3000/';
const FLAG_FILENAME = 'eae3ba4e0dbb5b9801504ac50b0bb2623e07ac785da428f87354012ce26d6f84';
const MARKDOWN_LIBRARY_SELECTOR = 'body > #filename-container #markdown-library';
const TAG = "fetch.js: ";

const RESOURCE_TIMEOUT = 600;  // phantomjs timeout for loading resources
const PAGE_WAIT_TIME = 300;  // setTimeout to wait for JS to execute

function getAddressFromFilename(filename) {
  return HOST + 'view/' + filename;
}

if (system.args.length !== 2) {
  console.error("Usage: " + system.args[0] + " <filename>");
  phantom.exit(1);
}

// set timeout for requests
page.settings.resourceTimeout = RESOURCE_TIMEOUT;
page.onResourceTimeout = function(req) {
  console.error(TAG + "Resource timed out with error: " +
    req.errorCode + ", " + req.errorString);
};
page.onAlert = function(msg) {
  console.log(TAG + "Alert with message: " + msg);
};
page.onError = function(msg, trace) {
  console.error(TAG + "JavaScript error: " + msg);
};

function openReportedPage(callback) {
  var address = getAddressFromFilename(system.args[1]);
  page.open(address, function(status) {
    if (status !== 'success') {
      console.error(TAG + "openReportedPage status = " + status + ", quitting");
      phantom.exit(1);
    }

    setTimeout(function() {
      page.evaluate(function(selector) {
        var el = document.querySelector(selector);
        el.value = 'marked';
        el.dispatchEvent(new Event('change'));
      }, MARKDOWN_LIBRARY_SELECTOR);

      //page.render('test.png');
      setTimeout(callback, PAGE_WAIT_TIME);
    }, PAGE_WAIT_TIME);
  });
}


function openFlagPage(callback) {
  var address = getAddressFromFilename(FLAG_FILENAME);
  page.open(address, function(status) {
    if (status !== 'success') {
      console.error(TAG + "openFlagPage status = " + status + ", quitting");
      phantom.exit(1);
    }
    setTimeout(callback, PAGE_WAIT_TIME);
  });
}


openReportedPage(function() {
  openFlagPage(function() {
    page.open('about:blank', function(status) {
      console.log(TAG + "success");
      phantom.exit(0);
    });
  });
});
