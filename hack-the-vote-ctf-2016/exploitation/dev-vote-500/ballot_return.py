#!/usr/bin/python
import os
import ctypes
from ctypes.util import find_library
from subprocess import call
import sqlite3 as lite
import pickle
import sys
import pwd
import time

username=''
new_ballot = False

# Helpers
def dprint(s):
    sys.stdout.flush()
    for c in s:
        time.sleep(1)
        sys.stdout.write(c)
        sys.stdout.flush()

def setresuid(ruid,euid,suid):
    libc = ctypes.CDLL('/lib/libc.so.6')
    libc.setresuid(ruid,euid,suid)

def debug():
    global username
    # Drop privileges
    pwnam = pwd.getpwnam(username)
    setresuid(pwnam.pw_uid, pwnam.pw_uid, pwnam.pw_uid)

    call(['/bin/sh', '-i', '/ballot_return/dbg.sh'])

# Data storage
class Ballot(object):
    def __init__(self):
        self.President = ''
        self.VicePresident = ''
        self.State = ''
        self.Senator_1 = ''
        self.Senator_2 = ''
        self.FavoriteIceCreamFlavor = ''

# Database interaction
def load_ballot():
    global new_ballot,username
    # Connect to database
    con = lite.connect('ballots.db')

    # Fetch serialized ballot for username
    cur = con.cursor()
    cur.execute('SELECT ballot FROM ballots WHERE username=?', (username,))
    
    # De-serialize ballot
    data = cur.fetchone()
    con.close()
    if data is None:
        new_ballot = True
        return Ballot()
    else:
        new_ballot = False
        return pickle.loads(str(data[0]))

def save_ballot(ballot):
    global new_ballot
    # Connect to database
    con = lite.connect('ballots.db')

    # Serialize ballot
    data = pickle.dumps(ballot)

    # Update ballot for username
    cur = con.cursor()
    if new_ballot:
        cur.execute("INSERT INTO ballots VALUES (NULL,?,?)",(username,data))
    else:
        cur.execute("UPDATE ballots SET ballot=? WHERE username=?",(data,username))
    con.commit()
    con.close()

# User interaction
def ballot_vote(ballot):
    for x in ballot.__dict__:
        if '_' == x[0]:
            continue
        ans = raw_input('{}? ({}): '.format(x, ballot.__dict__[x]))
        if ans:
            ballot.__dict__[x] = ans
    return ballot

def ballot_interact():
    global username
    # Load existing ballot for user
    sys.stdout.write("               Loading ballot for {}".format(username))
    dprint('...')
    print('done!')
    ballot = load_ballot()

    # Allow user to update ballot
    ballot = ballot_vote(ballot)

    # Save ballot to database
    save_ballot(ballot)

def main():
    global username
    # Get full privs for ballot updates
    username = os.getlogin()
    os.setresuid(os.geteuid(), os.geteuid(), os.getuid())

    # Print welcome header
    print("************************************************************")
    print("** Welcome to the District County online e-ballot return! **")
    print("************************************************************")
    print("**                                                        **")
    print("**                            *********                   **")
    print("**            --    *****     *** E ***                   **")
    print("**              --  * E *     ** BOX **                   **")
    print("**           --     *****     ***   ***                   **")
    print("**                            *********                   **")
    print("**                                                        **")
    print("************************************************************")
    
    try:
        ballot_interact()
    except EOFError:
        debug()

if __name__ == "__main__":
    main()
