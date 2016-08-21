var express = require('express');
var mongodb = require('mongodb');
var url = 'mongodb://localhost:27017/hackcon';
var MongoClient = mongodb.MongoClient;

// Use connect method to connect to the Server
MongoClient.connect(url, function (err, db) {
  if (err) {
    console.log('Unable to connect to the mongoDB server. Error:', err);
  } else {
    //HURRAY!! We are connected. :)
    console.log('Connection established to', url);

    var collection = db.collection('users');
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

app.set('views', __dirname);
app.set('view engine', 'jade');

app.use(require('body-parser').json());
app.use(require('body-parser').urlencoded());

app.get('/', function(req, res) {
	res.render('index', {});
});

app.post('/', function(req, res) {
	console.log(req.body.user);
	console.log(req.body.pass);

	// Use connect method to connect to the Server
	MongoClient.connect(url, function (err, db) {
	  if (err) {
	    console.log('Unable to connect to the mongoDB server. Error:', err);
	  } else {
	    //HURRAY!! We are connected. :)
	    console.log('Connection established to', url);

	    var collection = db.collection('users');
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
				return res.render('index', {message: 'Invalid Login'});

			}
			if (user.username == 'admin') {

				return res.render('index', {message: "Flag is HACKCON{MONGODB_BUTHOLE_LEAKING}"});
			}
			return res.render('index', {message: 'Welcome back ' + user.user});
		});
	  }
	});
});

var server = app.listen(49090, function () {
	console.log('listening on port %d', server.address().port);
});
