# OpenCTF : neophyte_reversing

**Category:** Tasks
**Points:** 
**Solves:** 
**Description:**

> {'solve_count': 14, 'description': u'I hear metallic skittering in the walls\n....CLICK CLICK CLICK.....\ndo you understand what they say?\n172.31.0.10/neophyte_reversing_ccabcc8f0b9900638a75017f2d6dc029', 'total_scored': 2800, 'challenge_name': u'neophyte_reversing', 'point_value': 200, 'open': 1}

> file: [neophyte_reversing_ccabcc8f0b9900638a75017f2d6dc029](neophyte_reversing_ccabcc8f0b9900638a75017f2d6dc029)

## Write-up

The app provided asks for a 41 character long pass-phrase (flag). Complains about its length and outputs "no" if the password is wrong.  
Opening it in disassembler, it is easy to see a function 0804860E that initializes 41 entries used for validation in a function 080484AD.

Knowing that we made a gdb script that outputs the flag at the end.

    root@kali:/mnt/hgfs/f# gdb -q --args neophyte_reversing_ccabcc8f0b9900638a75017f2d6dc029 12345678901234567890123456789012345678901
    Reading symbols from neophyte_reversing_ccabcc8f0b9900638a75017f2d6dc029...(no debugging symbols found)...done.
    (gdb) b *0x080485FC
    Breakpoint 1 at 0x80485fc
    (gdb) b *0x08049306
    Breakpoint 2 at 0x8049306
    (gdb) r
    Starting program: /mnt/hgfs/f/open/neophyte_reversing_ccabcc8f0b9900638a75017f2d6dc029 12345678901234567890123456789012345678901

    Breakpoint 1, 0x080485fc in ?? ()
    (gdb) set $ZF = 1
    (gdb) set $count = 0
    (gdb) while ($count <= 41)
     >    set $eflags |= (1 << $ZF)
     >    set {char}(0x0804B119 + $count) = $dl
     >    set $count = $count + 1
     >    if ($count >= 41)
      >        loop_break
      >    end
     >    c
     >end

    (gdb) x/s 0x0804B119
    0x804b119:	"OpenC\304F{IhopeYOUdidThisInADebuggerScript}"

Flag: `OpenCTF{IhopeYOUdidThisInADebuggerScript}`

## Other write-ups and resources

* none yet
