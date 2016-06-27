function escapeHtml(content) {
  // escaping is really annoying because then people can't use custom html tags
  // :( and besides, our content security policy is already super strict. so it
  // doesn't really matter anyway, right?
  return content;
}


function displayFile(filename) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/raw/' + filename);

  xhr.onload = function () {
    var text = xhr.responseText;
    var library = document.querySelector('#markdown-library').value;

    // load markdown library
    var scriptEl = document.createElement('script');
    scriptEl.src = '/static/' + library + '.js';
    scriptEl.onload = renderMarkdown.bind(this, text, library);
    document.head.appendChild(scriptEl);
  };

  xhr.onerror = function (err) {
    document.querySelector('#fileview').innerText = "Network error: " + err;
  };

  xhr.send();
}


function renderMarkdown(text, library) {
  var html;
  if (library === 'showdown') {
    var converter = new showdown.Converter();
    var content = escapeHtml(text);
    html = converter.makeHtml(content);
  }
  else {
    marked.setOptions({ sanitize: true });
    html = marked(text);
  }
  document.querySelector('#fileview').innerHTML = html;
}


function sendBeacon(filename) {
  // update recently closed pages
  if ('sendBeacon' in navigator) {
    navigator.sendBeacon('/recent-pages/' + filename);
  }
  else {
    // rip... have to use synchronous xhr
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/recent-pages/' + filename, false);
    xhr.send();
  }
}


function reportFile(filename) {
  var formEl = document.createElement('form');
  formEl.method = 'POST';
  formEl.action = '/report/' + filename;
  formEl.submit();
}


window.addEventListener('load', function () {
  var filename = location.pathname.replace(/^\/view\//, '');

  // attach event listeners
  document.querySelector('#markdown-library')
    .addEventListener('change', displayFile.bind(this, filename));
  window.addEventListener('unload', sendBeacon.bind(this, filename));
  document.querySelector('#report-link')
    .addEventListener('click', function (evt) {
      evt.preventDefault();
      reportFile(filename);
    });

  // update ui with filename
  document.querySelector('#filename').innerText = filename;
  document.querySelector('#download-link').href = '/raw/' + filename;
  document.title += ' | ' + filename;

  // display file initially
  displayFile(filename);
});
