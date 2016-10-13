# ABCTF 2016 : meteor-smash-100

**Category:** Web
**Points:** 100
**Solves:** 48
**Description:**

Dig around in [this](http://107.170.122.6:8082/) blog and I'm sure you can find a flag.

[HINT] Someone told me my admin checks are insecure.


## Write-up

The site offer the user to register an account and after logging in to post comments which are shown on the page. In order to get the flag user has to be admin (look HINT), therefore I assumed that the comments are not the vulnerable part and started researching.

In Meteor every user can access his profile by typing `Meteor.user().profile` into the browsers' console. Given the hint, can we somehow become admins?

Looking for `meteor user.profile admin exploit` shows us the [3rd link](https://dweldon.silvrback.com/common-mistakes) which describes a common vulnerability in Meteor apps - when `user().profile` can be edited through browsers console. By opening it and executing `Meteor.users.update(Meteor.userId(), {$set: {'profile.admin': true}});` we set us (user with our id) to be admin and by refreshing the website we get the flag.

`ABCTF{r3lly_s3cure_Auth0riz4t1on}`

## Other write-ups and resources

* none yet
