socat -T10 tcp-l:8000,reuseaddr,fork exec:./scripty,pty,setsid,setpgid,ctty
