# ROG BIOS update check
Checks if a new BIOS version is availabe for your [ROG mainboard](https://rog.asus.com/motherboards-group/).  
Just execute `main.py`, no input needed.

## Dependencies
[WMI](https://pypi.org/project/WMI/) to check installed BIOS version and mainboard model automatically.  
`pip install wmi`  
[Beautiful Soup](https://pypi.org/project/beautifulsoup4/) to parse the HTML to retrieve the Product ID  
`pip install beautifulsoup4`  

## TODO
Doesn't work with TUF and ASUS boards yet as they encode the Product ID differently to the HTML of ROG boards.
