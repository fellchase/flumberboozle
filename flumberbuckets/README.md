# flumberbuckets
![flumberbuckets](https://user-images.githubusercontent.com/11918572/70925058-9bb4a080-2050-11ea-915d-532d2e09505b.jpg)

Flumberbuckets is a part of suite of scripts that I'll be open-sourcing on GitHub in flumberboozle repository, scripts in this repository are supposed to aid bug hunters in hunting, automating workflows, etc.

## What is flumberbuckets?
Flumberbuckets is is yet another S3 bucket enumeration tool which you can choose to use while hunting on bug bounty programs or during security assessment. I designed this tool to serve my purposes and now I am open-sourcing it, there are several different tools that exist for people with different tastes. The aim of this tools was to present S3 bucket enumeration results in better format which is visually more appealing than scrolling through output of a bash script that just runs  aws s3 ls in a loop.

## How does it work?
Flumberbuckets is a really simple script which combines the best of existing S3 bucket enumeration tools to make S3 bucket enumeration simpler and faster. It achieves this by using DNS resolution for sorting out non existent buckets and runs 10 tests on each bucket, several buckets are checked simultaneously to save time.

## But why?
- I actually got my first bounty by finding misconfigured S3 bucket so I decided to write a tool for doing it on larger scale, this script is outcome of that effort.
- Tools I used previously weren't so good at presenting results of enumeration visually, it was a pain to scroll through output of those
- Tools I used previously had smaller word-lists and checked for less functions, I suspect that I missed a few easy bounties because of that.
- Tools I used previously were painfully slow they were bash scripts, they weren't multi-threaded they would sort out nonexistent buckets with HTTP requests, flumberbuckets was an attempt to fix all the problems I encountered while using other scripts.

## Is it really worth switching?

![Flumberbuckets in action](https://user-images.githubusercontent.com/11918572/70925128-bbe45f80-2050-11ea-99aa-ba85fac325b6.gif)

- You may want to switch over for any of the following reasons
- Sorting out nonexistent buckets with DNS(massdns) resolution rather than HTTP
- Multi-threaded enumeration of existent buckets to find misconfiguration
- Cleaner visual output which you can copy and store for later 
- Several vulnerability tests available like LIST, ACL , POLICY , CORS , REPLICATION , WEBSITE , LOCATION , LOGGING , UPLOAD , DELETE. 
- You can decide what tests you want to run on a buckets run all if you want run only 1 if you're in hurry 
- I also included DELETE test It's the most overlooked by S3 bucket automation tools
- Much more functionality and options that even I'm exhausted writing about it just check the "Detailed Usage" section
- Just try it, maybe you'll get your first bounty 


Note: The performance of flumberbuckets is subject to your connection bandwidth speed and hardware

## Installation & Usage
Refer article published on my blog 
[Releasing Flumberbuckets: S3 Bucket Enumeration Tool for Bug Hunters](https://fellchase.blogspot.com/2019/12/releasing-flumberbuckets-s3-bucket-enumeration-tool.html)

## Credits
Flumberbuckets is inspired from following scripts, it combines all the good things in the following tools.
- mass3
- s3enum
- S3Scanner

## Support the Project
### Share your story with me! ☺
If you earned a bounty through use of this script do share the story with me I will be happy to hear that my script was of use to you. You can contact me over twitter @fellchase

### Wanna support monetarily 💰?
If you want to thank me monetarily or want to donate to this project you can do so on [paypal.me/fellchase](https://paypal.me/fellchase) I'll be happy to hear your bug bounty story if you got any bounty with this script.
