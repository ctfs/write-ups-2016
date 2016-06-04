import java.lang.reflect.Method;
import java.security.Permission;

import java.util.*;

class CustomSecurityManager extends SecurityManager {
    ArrayList<String> allow;
    String insecureClassName;
    String[] allowedLibraries = new String[] {"com.google","twitter4j","com.securefiledownloader"};
    String[] allowedSecurityPermissions = new String[] {"getProperty.networkaddress.cache.negative.ttl", "getProperty.networkaddress.cache.ttl"};
    public CustomSecurityManager(String className, String[] allowed) {
        insecureClassName = className;
        allow = new ArrayList<String>(Arrays.asList(allowed));
        // allow standard jre libraries
        allow.add(System.getProperty("java.home"));
    }

    public boolean checkSecurityPermission(String str) {
        for (String i : allowedSecurityPermissions) {
            if (str.equals(i))
                return true;
        }
        return false;
    }

    public boolean checkAllow(String str) {
        for (String i : allow) {
            if (str.startsWith(i))
                return true;
        }
        return false;
    }

    public boolean isLibrary() {
        StackTraceElement[] stack = Thread.currentThread().getStackTrace();
        for (StackTraceElement s : stack) {
            // reached end
            if ((""+s).startsWith("Wrapper") || (""+s).startsWith(insecureClassName)) {
                return false;
            }
            // pass cases that obviously aren't libraries
            if ((""+s).startsWith("CustomSecurityManager") || (""+s).startsWith("java.") || (""+s).startsWith("sun.")) {
                continue;
            }
            for (String x : allowedLibraries) {
                if ((""+s).startsWith(x)) {
                    return true;
                }
            }
        }
        return false;
    }

    @Override
    public void checkPermission(Permission perm) {
        if (perm instanceof java.io.FilePermission) {
            if (!perm.getActions().equals("read")) {
                throw new SecurityException("You can only read files! " + perm);
            }
            // allow trusted libraries to access files
            if (!isLibrary()) {
                if (!checkAllow(perm.getName())) {
                    throw new SecurityException("File access denied! " + perm);
                }
            }
        }
        else if (perm instanceof java.net.SocketPermission || perm instanceof java.net.NetPermission || perm instanceof javax.net.ssl.SSLPermission) {
            // allow trusted libraries to access the internet
            if (!isLibrary()) {
                // need this to create URLs
                if (!perm.getName().equals("specifyStreamHandler")) {
                    throw new SecurityException("Socket access denied! " + perm);
                }
            }
        }
        else if (perm instanceof java.lang.RuntimePermission) {
            if (perm.getName().equals("setSecurityManager") || perm.getName().equals("createSecurityManager")) {
                throw new SecurityException("Nope! " + perm);
            }
            if (perm.getName().equals("createClassLoader") || perm.getName().equals("preferences")) {
                throw new SecurityException("Nah... " + perm);
            }
            if (perm.getName().equals("queuePrintJob")) {
                throw new SecurityException("Why... " + perm);
            }
        }
        else if (perm instanceof java.security.SecurityPermission) {
            if (!checkSecurityPermission(perm.getName())) {
                throw new SecurityException("Permission denied! " + perm);
            }
        }
        else if (perm instanceof java.security.UnresolvedPermission) {
            throw new SecurityException("Permission denied! " + perm);
        }
        else if (perm instanceof java.sql.SQLPermission || perm instanceof java.util.logging.LoggingPermission || perm instanceof java.awt.AWTPermission) {
            // just in case...
            throw new SecurityException("Permission denied! " + perm);
        }
        // i think thats everything
    }
}

public class Wrapper {
    public static void main(String[] args) {
        // args[0] is the name of the class to run
        // args[1] is a colon separated list of directories your program can access
        System.setSecurityManager(new CustomSecurityManager(args[0], args[1].split(":")));
        try {
            Class<?> unsafeClass = ClassLoader.getSystemClassLoader().loadClass(args[0]);
            Method m = unsafeClass.getMethod("main", String[].class);
            m.invoke(null, new Object[] {new String[] {}});
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

