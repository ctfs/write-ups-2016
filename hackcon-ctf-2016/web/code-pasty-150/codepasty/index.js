var express = require('express');
var mongodb = require('mongodb');
var session = require('express-session');
var url = 'mongodb://localhost:27017/hackcon2';
var MongoClient = mongodb.MongoClient;

// Use connect method to connect to the Server
MongoClient.connect(url, function (err, db) {
  if (err) {
    console.log('Unable to connect to the mongoDB server. Error:', err);
  } else {
    //HURRAY!! We are connected. :)
    console.log('Connection established to', url);

    var collection = db.collection('common');
	var user1 = {username: 'admin', password: 'complexisthekey', name: 'Administrator'};
	collection.insert(user1,  function (err, result) {
      if (err) {
        console.log(err);
      } else {
        console.log('Inserted %d documents into the "users" collection. The documents inserted with "_id" are:', result.length, result);
      }
  	});
  }
});

var app = express();

app.use(session({secret: 'HackConIsCrazyGood'}));
app.set('views', __dirname);
app.set('view engine', 'jade');

app.use(require('body-parser').urlencoded({extended: true}));

app.get('/paste/:id', function(req, res) {
	MongoClient.connect(url, function (err, db) {
	  if (err) {
	    console.log('Unable to connect to the mongoDB server. Error:', err);
	  } else {
			var collection = db.collection('common');
			if (!req.params['id'] || req.params['id'].length != 24) return req.redirect('/');
			if (!mongodb.ObjectID(req.params['id'])) return req.redirect('/');
			var cursor = collection.find(mongodb.ObjectID(req.params['id']));

			console.log('ID ' + req.params['id']);
			cursor.nextObject(function(err, pasty) {
					console.log("pasty obj: ");
					console.log(pasty);
					// Do a find and get the cursor count
					cursor.count(function(err, count) {
						console.log(count);
		      		})

					if (!pasty) {
						return res.redirect('/');

					}
					return res.render('show', {pasty: pasty});
			});
		}
	});
});

app.get('/paste', function(req, res) {
	sess = req.session;
	if(!sess.user)
		res.redirect('/login');
	res.render('paste', {});
});

app.post('/paste', function(req, res) {
	sess = req.session;
	if (!sess.user)
		res.redirect('/login');
	
	if (!req.body.pasty) res.redirect('/paste');
	MongoClient.connect(url, function (err, db) {
	  if (err) {
	    console.log('Unable to connect to the mongoDB server. Error:', err);
	  } else {
		var collection = db.collection('common');
		var past = {username: sess.user, content: req.body.pasty};
		collection.insert(past, function (err, result) {
			if (err) {
				console.log(err);
			}
			else {
				console.log(result);
				res.redirect('/paste/' + result[0]['_id']);
			}
		});
	    }
    });
});


app.get('/', function(req, res) {
	MongoClient.connect(url, function (err, db) {
	  if (err) {
	    console.log('Unable to connect to the mongoDB server. Error:', err);
	  } else {
		var collection = db.collection('common');
		collection.find().sort({_id:-1}).limit(100).toArray(function(error, results) {
	    	console.log(results); 
	        if (!error) res.render('index', {pasties: results});
	   	});
      }
    });
});



app.get('/register', function(req, res) {
	sess = req.session;
	if(sess.user)
		return res.redirect('/');
	return res.render('register', {});
});


app.post('/register', function(req, res) {
	sess = req.session;
	console.log(req.body.user);
	console.log(req.body.pass);
	MongoClient.connect(url, function (err, db) {
	  if (err) {
	    console.log('Unable to connect to the mongoDB server. Error:', err);
	  } else {
	    console.log('Connection established to', url);

	    var collection = db.collection('common');
	    var check = collection.find({'username': req.body.user});
	    check.count(function(e, count) {
	    	if (count > 0) return res.redirect('/register');
	    });
		var user1 = {username: req.body.user, password: req.body.pass};
		collection.insert(user1,  function (err, result) {
	      if (err) {
	        console.log(err);
	      }
	  	});
	  }
	});

	return 	res.redirect('/login');

});


app.get('/login', function(req, res) {
	sess = req.session;
	if(sess.user)
		res.redirect('/paste');
	res.render('login', {});
});

app.post('/login', function(req, res) {
	sess = req.session;
	console.log(req.body.user);
	console.log(req.body.pass);

	// Use connect method to connect to the Server
	MongoClient.connect(url, function (err, db) {
	  if (err) {
	    console.log('Unable to connect to the mongoDB server. Error:', err);
	  } else {
	    //HURRAY!! We are connected. :)
	    console.log('Connection established to', url);

	    var collection = db.collection('common');
	    console.log("Collection!");
	    console.log("Finding");
	    console.log(req.body.user);
	    console.log(req.body.pass);
    	var cursor = collection.find({username: req.body.user, password: req.body.pass});
		cursor.nextObject(function(err, user) {
			console.log("user obj: ");
			console.log(user);
			// Do a find and get the cursor count
			cursor.count(function(err, count) {
				console.log(count);
      		})

			if (!user) {
				return res.render('login', {message: 'Invalid Login'});

			}

			sess.user = user.username;
			if (user.username == 'admin') {
				return res.render('login', {message: "Flag is HACKCON{WHY_MULTIPLE_COLLECTIONS}"});
			}
			return res.render('login', {message: 'Welcome back ' + user.username});
		});
	  }
	});
});

var server = app.listen(49090, function () {
	console.log('listening on port %d', server.address().port);
});
