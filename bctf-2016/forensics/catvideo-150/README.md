#bctf 2016 cat video writeup

###*Category:* Forensics *Points:* 150

###How we used ffmpeg and java to do a simple video forensics analysis.

We started out looking at a very scrambled video of something that might be the outline of a cat, and something that looked like two rows of text the first few seconds.

We guessed that the lines of text was the flag, and dumped the video into individual frames with ffmpeg:

> ffmpeg -i catvideo-497570b7e2811eb52dd75bac9839f19d7bca5ef4.mp4 -vf fps=30  pics_in/%04d.bmp

Once we had that it was easy to experiment with a couple of different filters, and by going over the 100 first frames, and record the pixel positions of all pixels where the lowest bit was flipped from one frame to the next.

Since the first seconds was a fade-in of the text in the video we were lucky and this technique gave us a clear picture of the title text of what turned out to be a normal cat video: https://www.youtube.com/watch?v=N-CSBFdDZsw

Back to the drawing board it was, and the next thing that was tried was to play with filters in gimp, Kent on our team found out that the flag became visible if you used the differance method on two of the images where one was later in the movie.

For completeness sake we implemented it in code also, we took the first image and xor'ed all images in the stream with that one, and then wrote them back to disk (implemented here: https://git.tazj.in/hackeriet/bctf-2016/src/master/catvideo/src/main/java/no/hackeriet/App.java ).

Once that was done we could reassemble it into a video with ffmpeg:

> ffmpeg -y -f image2 -i pics_out/%04d.png -r 10 -vcodec libx264 -vb 4096k -acodec null event.mp4

written by Alexander Kjäll



## Other write-ups and resources
* <http://veganzombies.org/writeups/2016/03/21/BCtf-catvideo.html>
* <https://github.com/WesternCyber/CTF-WriteUp/blob/master/2016/BCTF/Forensics150.md>
* <http://fadec0d3.blogspot.com/2016/03/bctf-2016-catvideo-150.html>
* <https://github.com/DMArens/CTF-Writeups/tree/master/2016/BCTF/Forensics150>
* <http://err0r-451.ru/2016-bctf-forensic-catvideo-150-pts/>
* [Invulnerable (Russian)](http://countersite.org/articles/steganography/68-bctf-2016-stego-catvideo.html)
