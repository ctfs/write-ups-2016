// wow, maybe i should use a library...

function displaySuccess(filename) {
  document.querySelector('#success-container').style.display = 'block';
  document.querySelector('#error-container').style.display = 'none';
  document.querySelector('#success-link').href = '/view/' + filename;
}

function displayError(message) {
  document.querySelector('#success-container').style.display = 'none';
  document.querySelector('#error-container').style.display = 'block';
  document.querySelector('#error-message').innerText = String(message);
}

function uploadFile() {
  var submitButton = document.querySelector('#markdown-submit');
  submitButton.disabled = true;

  var contents = document.querySelector('#markdown-input').value;
  var obj = { text: contents };

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.responseType = 'json';
  xhr.send(JSON.stringify(obj));

  xhr.onload = function () {
    var obj = xhr.response;
    if (obj.success) {
      displaySuccess(obj.filename);
    } else {
      displayError(obj.error);
    }
    submitButton.disabled = false;
  };
  xhr.onerror = function (err) {
    displayError(err);
    submitButton.disabled = false;
  };
}


var SHORT_TIMEOUT = 15000;
var LONG_TIMEOUT = 120000;

var timerId;
var timeoutDuration = SHORT_TIMEOUT;

function updateTimeout() {
  if (timerId) {
    clearTimeout(timerId);
  }
  timerId = setTimeout(function () {
    console.log('timeout');
    loadRecentPages();
  }, timeoutDuration);
}

function loadRecentPages() {
  console.log('* loadRecentPages');
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/recent-pages');
  xhr.onload = function () {
    var obj = JSON.parse(xhr.responseText)
    var pages = obj.recent_pages;

    var container = document.querySelector('#recent-pages-container');
    var ul = document.createElement('ul');

    pages.forEach(function (filename) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '/view/' + filename;
      a.target = '_blank';
      a.textContent = filename;
      li.appendChild(a);
      ul.appendChild(li);
    });

    container.innerHTML = '';
    container.appendChild(ul);
  };

  xhr.send();
  updateTimeout();
}

document.addEventListener('DOMContentLoaded', function () {
  // gosh, show the form
  var form = document.querySelector('#markdown-form');
  form.style.display = 'block';
  form.addEventListener('submit', function (evt) {
    evt.preventDefault();
    uploadFile();
  });

  // update list of recent pages
  loadRecentPages();
});

window.addEventListener('focus', function () {
  console.log('focus');
  loadRecentPages();
});

document.addEventListener('visibilitychange', function () {
  console.log('visibilitychange hidden=' + document.hidden);
  if (document.hidden) {
    timeoutDuration = LONG_TIMEOUT;
  } else {
    timeoutDuration = SHORT_TIMEOUT;
  }
  updateTimeout();
});
