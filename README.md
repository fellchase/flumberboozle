# flumberboozle
Suite of programs meant to aid in bug hunting and security assessments 

## Why this weird name?
Just because I heard it first [here])https://youtu.be/lIFE7h3m40U?t=661) so I thought this meaningless word would be fitting name of a repository I don't know what I'm going to do with.

## Contents
This repository contains scripts that I wrote or modified other pre-existing scripts, which are useful in Bug Bounty Hunting and Security Assessments of websites.

### Flumberbuckets
Flumberbuckets is a multi-threaded tool to automate S3 bucket hunting. I actually got my first bounty through this script so decided develop it further and to further open source it, essentially flumberbuckets takes in a word as argument creates huge list of possible bucket names then finds the buckets that exist & performs tests that you want on those buckets. It provides a good visual overview of buckets that were found and what misconfiguration they have.

### Portboozle
Portboozle is a script I wrote as a substitute for masscan as it wasn't working as intended on my machine it wasn't showing the ports that were open on the targets I was scanning while, nmap was showing it properly. I tried to change the config of masscan but it still showed unreliable results, so I decied to write my own script to fix my problems. I know this script is no match for masscan's speed but it's okay for me as it at least shows all ports that were open. If you're facing the same problem with masscan then you could be missing on some open ports try running masscan & nmap on `scanme.nmap.org` and compare the results.

## Support the Project
### Share your story with me! ☺
If you earned a bounty through use of this script do share the story with me I will be happy to hear that my script was of use to you. You can contact me over twitter @fellchase

### Wanna support monetarily 💰?
If you want to thank me monetarily or want to donate to this project you can do so on [paypal.me/fellchase](https://paypal.me/fellchase) I'll be happy to hear your bug bounty story if you got any bounty with this script.