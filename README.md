Python CSRFGenerator
====================
- 1.) Installation
- 2.) Usage
- 3.) Functionality
- 4.) ToDo
- 5.) License

##1. Installation

[Pyhton 2.7](http://www.python.org/download/releases/2.7/) is required to run this software.

You only need to clone this GitHub repository:

```
git clone https://github.com/internetwache/Python-CSRFGenerator.git CSRFGenerator
```

Yay you're done :)

##2. Usage

```
% ./csrfgen.py -h        
[*] Started CSRFGen
[*] Usage: ././csrfgen.py [PoC]
[-] PoC: File to write the CSRF PoC - Default: csrf.html
```

First, export your HTTP-Request (e.g. "rightclick -> Copy to file" in Burp Proxy) into the "csrf.txt" file or use the echo command:

```
echo '[LONG HTTP-REQUEST]' > csrf.txt
```

After that, you can generate your CSRF Poc:

```
./csrfgen.py newcsrf.html
```

You can specify the output file using the first parameter. This parameter is optional and by default the PoC will be written into "csrf.html".

##3. Functionality

This tool can be used to create CSRF PoCs for the following HTTP-Request types:

- Simple GET Requests
- Simple POST Requests

##4. ToDo

The following functionality should be implemented in the future:

- POST Requests with JSON-Body
- Multipart POST Requests

##5. License

This script is licensed under [MIT](http://choosealicense.com/licenses/mit/). 
Please feel free to extend or improve the code/functionality of this script :)

Happy Hacking!
