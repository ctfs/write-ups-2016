# Cyber Security Challenge 2016: Even the best make mistakes  
 
**Category:** Reverse Engineering  
**Points:** 40  
**Challenge designer:** Didier Stevens  
**Description:**  
> We suspect [this document](challenge-source-files/Doc1.doc.zip) is trying to drop malware on our network, can you find the url of the malware? The password of the zip file is 'infected'. Remember to never run untrusted files on a non-disposable system!

## Write-up
For this challenge we need to use the tool oledump which is made by the creator of the challenge.
> oledump.py is a program to analyze OLE files (Compound File Binary Format). These files contain streams of data. oledump allows you to analyze these streams.  

Using the `plugin_linear.py` we can solve the challenge in a one liner.

```
$ python oledump.py -p plugin_linear Doc1.doc.zip                             ~/Downloads
  1:       114 '\x01CompObj'
  2:      4096 '\x05DocumentSummaryInformation'
  3:      4096 '\x05SummaryInformation'
  4:      7045 '1Table'
  5:       441 'Macros/PROJECT'
  6:        41 'Macros/PROJECTwm'
  7: M    2504 'Macros/VBA/ThisDocument'
               Plugin: Linear cryptanalysis
                 http://example.com/iejdinfe/oap98dczk.exe
  8:      2599 'Macros/VBA/_VBA_PROJECT'
  9:       522 'Macros/VBA/dir'
 10:      4096 'WordDocument'
```

### Solution
*"http://example.com/iejdinfe/oap98dczk.exe"*

