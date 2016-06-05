# ~ luvmarkdown ~

## Distribution
Unfortunately, the setup of this problem is rather fragile.

The web server uses Node.js, and the Node dependencies can be installed from
`web/package.json`.

The server also requires PhantomJS to be installed. *In particular, `app.js`
expects to be able to run `phantomjs` from a shell.* This may pose problems,
especially on Windows. On my Windows machine, I've done this by creating a
symlink `web/phantomjs.exe` that points to a real copy of PhantomJS.

Next, `setup.js` needs to be run to initialize the problem. This script will
copy the files in `initial_files` into `web/uploads`; in particular, the
description file and the flag file.

Note that `fetch.js` is also dependent on the current host, which as of now
is set to `http://localhost:3000`. This will obviously change.

## Other notes
Note that because this setup relies on hashes, it is sensitive to even the
smallest changes in either of the `initial_files`:

  * If `flag.txt` is changed, the corresponding hash in `fetch.js` must also
    be changed.
  * If `description.txt` is changed, the corresponding hash in `problem.yml`
    must also be changed.

## Improvements
Currently, files are stored in `web/uploads`, and the session data from
`express-session` is stored in memory. This is quite suboptimal. Eventually,
those should both be stored in a database, if/when possible.
