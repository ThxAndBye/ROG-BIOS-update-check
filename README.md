# ROG BIOS update check
Checks if a new BIOS version is availabe for your [ROG mainboard](https://rog.asus.com/motherboards-group/).  
Just execute `main.py`, no input needed.

Example output:
```
C:\Users\Thx And Bye\Desktop>main.py
Your Board: ROG-STRIX-X470-I-GAMING, installed BIOS: 4603
Retrieving Board ID ... 10028
Retrieving newest BIOS version ... 4603

No new BIOS release found!
```

When an update is available:
```
Your Board: ROG-STRIX-X470-I-GAMING, installed BIOS: 4502
Retrieving Board ID ... 10028
Retrieving newest BIOS version ... 4603

BIOS Update Available! Version 4603 Stable release from: 22 Sep 2021
1. Update AMD AM4 AGESA V2 PI 1.2.0.3 Patch C
2.Improve system performance
Download: https://dlcdnets.asus.com/pub/ASUS/mb/BIOS/ROG-STRIX-X470-I-GAMING-ASUS-4603.ZIP
```

## Dependencies
[WMI](https://pypi.org/project/WMI/) to check installed BIOS version and mainboard model automatically.  
`pip install wmi`  
[Beautiful Soup](https://pypi.org/project/beautifulsoup4/) to parse the HTML to retrieve the Product ID  
`pip install beautifulsoup4`  

## TODO
Doesn't work with TUF and ASUS boards yet as they encode the Product ID differently to the HTML of ROG boards.
