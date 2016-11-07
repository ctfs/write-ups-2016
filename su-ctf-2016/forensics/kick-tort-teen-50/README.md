# Sharif University CTF 2016 : Kick Tort Teen

**Category:** Forensics
**Points:** 50
**Solves:** 120
**Description:**

> Anagram, anyone?
>
> Download [data.xls](./data.xls)


## Write-up

by [Jashan Bhoora](https://github.com/jashanbhoora)

Upon opening the Excel file we are given, we are presented with a 23x14747 spreadsheet of integers.
I notice the Excel warning that Macros have been disabled, so I open the Macro Editor (Alt + F11) and find the following macro.

```VBA
Function FileExists(ByVal FileToTest As String) As Boolean
   FileExists = (Dir(FileToTest) <> "")
End Function
Sub DeleteFile(ByVal FileToDelete As String)
   If FileExists(FileToDelete) Then 'See above
      SetAttr FileToDelete, vbNormal
      Kill FileToDelete
   End If
End Sub
Sub DoIt()
    Dim filename As String
    filename = Environ("USERPROFILE") & "\fileXYZ.data"
    DeleteFile (filename)

    Open filename For Binary Lock Read Write As #2
    For i = 1 To 14747
        For j = 1 To 23
            Put #2, , CByte((Cells(i, j).Value - 78) / 3)
        Next
    Next

    Put #2, , CByte(98)
    Put #2, , CByte(13)
    Put #2, , CByte(0)
    Put #2, , CByte(73)
    Put #2, , CByte(19)
    Put #2, , CByte(0)
    Put #2, , CByte(94)
    Put #2, , CByte(188)
    Put #2, , CByte(0)
    Put #2, , CByte(0)
    Put #2, , CByte(0)

    Close #2
End Sub
```

I haven't done any VBA, but I figure it's writing a file to the Windows environment variable `%USERPROFILE%`.
I enable and run the macro, and upon checking `%USERPROFILE%` I find `fileXYZ.data`

Analysing under Ubuntu:

```
file fileXYZ.data
fileXYZ.data: ELF 64-bit LSB  executable, x86-64, version 1 (GNU/Linux), statically linked, stripped

chmod +x fileXYZ.data
./fileXYZ.data
SharifCTF{5bd74def27ce149fe1b63f2aa92331ab}
```
And there's the flag!

<b>Flag: SharifCTF{5bd74def27ce149fe1b63f2aa92331ab}</b>

## Other write-ups and resources

* <https://github.com/ctfs/write-ups-2016/tree/master/su-ctf-2016/forensics/kick-tort-teen-50>
* [0x90r00t](https://0x90r00t.com/2016/02/07/sharif-university-ctf-2016-forensic-50-kick-tort-teen-write-up/)
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-02-05-sharif/for_50_tort#eng-version)
* <https://github.com/QuokkaLight/write-ups/blob/master/sharif-university-ctf-2016/forensics/Kick_Tort_Teen.md>
* <https://github.com/smokeleeteveryday/CTF_WRITEUPS/tree/master/2016/SHARIFCTF/forensics/kick_tort_teen>
