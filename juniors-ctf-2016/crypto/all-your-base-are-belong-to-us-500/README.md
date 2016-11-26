# Juniors CTF 2016 : all-your-base-are-belong-to-us-500

**Category:** Crypto
**Points:** 500
**Solves:**
**Description:**

> ![Description Image](all-your-base-are-belong-to-us-desc-0.jpg)
>
> \- Gruncle Stan, where are you going?
>
> \- Guys, I'm going to Las Vegas. Gonna con them into giving me all their money. Haha.
>
> \- Gruncle, Mabel has already been a head while you were away last time. May I take a lead now?
>
> \- As you wish, Dipper. I'll leve you my cash. As I arrive in LA, I'll send you an email with an account number.
>
> \- But Gruncle, how will I know that the message is from you?
>
> \- Ha, McGucket has invented electronic signature. I'll use it. You will have a verification key and I will have a signature key.
>
> \- Ok, Gruncle Stan. I'm going to do it right. Have fun in LA.
>
> A few hours later (Gideon is muttering to himself)
>
> ![Description Image](all-your-base-are-belong-to-us-desc-1.jpg)
>
> \- Eventually I've got a chance to take Stan's Mystery Shack.
>
> \- I'll steal the money while Dipper will be sending it to Stan.
>
> \- Genious. But how will we do this? Dipper is going to use the bank services.
>
> \- It means that we only have to figure out the way how the money ends up in my hands.
>
> \- I'll fake Stan's message and write in the number of my account. Haha.
>
> \- Yeah, that's genious. But Stan uses McGucket's e-signature. Dipper will instantly realize what is going on.
>
> \- McGucket is so dumb that he used CRC32 insead of regular hash. It'll be dead easy to hack it.
>
> \- But I don't know anything about hashes, keys and cryptography. What am I supposed to do?
>
> \- You can seek for help. It seems I know someone who will attempt to do this.
>
> On the next day Gideon captured the message from Stan with an account number. Change the message:
>
> ############ BEGIN SIGNED MESSAGE ############
>
> send me $ 10,000 to the account 9589234485239
>
> ############## BEGIN SIGNATURE ###############
>
> 0x64ce88bd59abad6c3f2247f9109bac5d2c1b7d6L
>
> 0x5a39c115fef0ff943740a0cbef07a762478520f6L
>
> ############# END SIGNED MESSAGE #############
>
> Write in Gideon's accout number there: 0102128506010 and dispatch it.
>
> You can send a message via [online messager](10.0.212.239:33636)

## Write-up

(TODO)

## Other write-ups and resources

* none yet
