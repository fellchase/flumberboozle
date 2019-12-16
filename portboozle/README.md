# Portboozle
Portboozle is a script I wrote as a substitute for masscan as it wasn't working as intended on my machine it wasn't showing the ports that were open on the targets I was scanning while, nmap was showing it properly. I tried to change the config of masscan but it still showed unreliable results, so I decied to write my own script to fix my problems. I know this script is no match for masscan's speed but it's okay for me as it at least shows all ports that were open. If you're facing the same problem with masscan then you could be missing on some open ports try running masscan & nmap on `scanme.nmap.org` and compare the results.

## Features
- Save scan progress in JSON format
- Resume scans on startup by launching this script at startup with cron or something 
- Auto save on shutdown
- Multi-threaded 
- Output greppable to some extent
- Fits into the massdns workflow for bug bounty hunting
- Useful when masscan doesn't work properly

## Installation
Python 3 only requires no dependencies just clone the git repo and change directory then run portboozle.py 

## Usage
```$ python portboozle.py -h```
```
Usage: cat massdns_output | portboozle.py -p <portlist>

Options:
  -h, --help            show this help message and exit
  -p PORTS, --ports=PORTS
                        Specify target port[s] seperated by comma or just do
                        1-65535 or medium or large or huge or massive
  -t THREADS, --threads=THREADS
                        Specify number of threads default is 100
  -o OUTPUT, --output=OUTPUT
                        Output JSON location
  -s TIMEOUT, --timeout=TIMEOUT
                        Socket timeout for port scanning default is 0.7
  -d DUMP, --dump=DUMP  Path to .portboozle.dump
```

```$ cat massdns_output_examplecom | ./portboozle.py -p large -o ~/Desktop/example_scan.json```
Now try pressing CTRL+C it'll save the state somewhere this way you can resume your scan when you again relaunch the script, you can also run the script at startup and it'll do it's job diligently and your portscans will start and stop automatically when you use computer. Auto save function only works if you are going to save output as JSON that is when you use `-o`

Output saved in JSON format, is categoried into IP and then into hostnames used and ports open on that IP
```
    "1.1.1.1": {
        "hosts": [
            "subdomain.example.com"
        ],
        "ports": [
            443,
            80
        ]
    }

```


Following command will just output result to terminal won't autosave on shutdown or quit or won't save the results in JSON format

```$ cat massdns_output_examplecom | python portboozle.py -p large```

Output on terminal
```
93.184.216.34 | 80 | www.example.com
93.184.216.34 | 443 | www.example.com
```

massdns_output_examplecom should look like this
```
0000028.example.com. a 235.49.239.47
0000028.example.com. a 87.140.150.81
000245000.example.com. a 235.49.239.47
000245000.example.com. a 87.140.150.81
001-kz.example.com. a 235.49.239.47
```

## Support the Project
### Share your story with me! ☺
If you earned a bounty through use of this script do share the story with me I'd be happy to hear that my script was of use to you. You can contact me over twitter @fellchase

### Wanna support monetarily 💰?
If you want to thank me monetarily or want to donate to this project you can do so on [paypal.me/fellchase](https://paypal.me/fellchase) I'll be happy to hear your bug bounty story if you got any bounty with this script.