# NCL 2016 Preseason : Email-Header-Analysis-65

__Category__: OSINT

__Points__: 65

## Write-up

For this Challenge we are provided with the following questions...

<a href="https://jhalon.github.io/images/ncl3.png"><img src="https://jhalon.github.io/images/ncl3.png"></a>

We are also provided with the following email header to answer the questions.

```
Delivered-To: alpha1@hacknet.cityinthe.cloud
Received: by 177.75.184.96 with SMTP id c1234trf3719itc;
        Wed, 9 Sep 2015 11:29:09 -0700 (PDT)
Return-Path: <gh0st@hacknet.cityinthe.cloud>
Received: from mail.hacknet.cityinthe.cloud (mail.hacknet.cityinthe.cloud. [75.184.96.93])
        by mx.cityinthe.cloud with ESMTP id o66si4673783qhb.117.2015.09.09.11.29.08
        for <alpha1@hacknet.cityinthe.cloud>;
        Wed, 09 Sep 2015 11:29:08 -0700 (PDT)
Received: by mail.hacknet.cityinthe.cloud (75.184.96.93) with ESMTP id t89IT8Le023674
	for <alpha1@hacknet.cityinthe.cloud>; Wed, 9 Sep 2015 14:29:08 -0400 (EDT)
From: <gh0st@hacknet.cityinthe.cloud>
Message-Id: <201509091829.t89IT8cb018346@mail.cityinthe.cloud>
Date: Wed, 09 Sep 2015 14:29:08 -0400
To: alpha1@hacknet.cityinthe.cloud
Subject: passphrase
User-Agent: Heirloom mailx 12.4 7/29/08
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

The flood of revolution.
```

--

__What is the recipient’s email address?__

The answer is located in Line 1 of the header - `Delivered-To: alpha1@hacknet.cityinthe.cloud`.

__Answer: alpha1@hacknet.cityinthe.cloud__

--

__What is the sender’s email address?__

The Return Path in Line 4 provides us this answer - `Return-Path: gh0st@hacknet.cityinthe.cloud`.

__Answer: gh0st@hacknet.cityinthe.cloud__

--

__What IP address retrieves the email?__

Line 5 provides us this answer:

`Received: from mail.hacknet.cityinthe.cloud (mail.hacknet.cityinthe.cloud. [75.184.96.93])`

__Answer: 75.184.96.93__

--

__What is the content type of the message?__

Line 18 provides us this answer - `Content-Type: text/plain; charset=us-ascii`

__Answer: text/plain__

--

__What version of MIME is being used?__

Just look for MIME in Line 17 - `MIME-Version: 1.0`.

__Answer: 1.0__

--

__What day of the week was the message received?__

Look for the date after Recieved in Line 3 - `Wed, 9 Sep 2015 11:29:09 -0700 (PDT)`.

__Answer: Wednesday__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-intro-osint/
