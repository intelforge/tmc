[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![stability-alpha](https://img.shields.io/badge/stability-alpha-f4d03f.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#alpha)

# tmc
Threat Mapping Catalogue

![](tmc/static/TMCv1.png "TMC Diagram")
​
## Requirements
- [python3](https://www.python.org/) (3.7+)
- Flask
- Sqlite
- **TRAM adaptation** : (https://github.com/fierytermite/tram-1) [forked from fixed version by [@cyb3rR4v3n](https://twitter.com/cyb3rR4v3n) 
- **Attack Navigator adaptation** : (https://github.com/fierytermite/attack-navigator)  

For the navigator, you'll need to clone the branch 'tmc' in order to make it work:

```
git clone --branch tmc https://github.com/fierytermite/attack-navigator
```

Note!! In order to the Navigator Adaptation to work properly you would have to work around CORS blocked by policy. You can get away easily by using Chrome browser extension [Allow CORS: Access-Control-Allow-Origin](https://chrome.google.com/webstore/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf?). Keep in mind that CORS blocks are implemented for security reasons, so allow them wisely. You can still use TRAM and all other functionality without it.  

## Installation

Clone this github repository and from its root folder install its requirements:
```
pip install -r requirements.txt
```

You can set the enviornment in which the app is running by setting the FLASK_ENV variable to ```development``` or ```production```:

```
export FLASK_ENV=<environment varible>
```

Then run the following commands:

```
export FLASK_APP=tmc
flask init-db
flask run
```

Once the server has started, access the application through localhost:5000. **You will need to register an user and log in in order to use the application.**

To load the database with the data from [ATT&CK](https://attack.mitre.org/) access the following path. Please be patiente, since this operation **really takes a while** (aprox 1h 30m, depending on your internet connection):

```
localhost:5000/first-time
```

Keep in mind that the next time you want to run the application, you **don't have to** initilizate the database, since doing it will erase any content loaded in it. Repeat the previous steps without that command:

```
export FLASK_ENV=<environment varible>
export FLASK_APP=tmc
flask run
```

# Making the APP public

If you prefer, you can change the port and make the app publicly available by running the following command:

```
flask run -p <number> -h 0.0.0.0
```

# Author

* Valentina Palacin [@fierytermite](https://twitter.com/fierytermite) 

# License: GPL-3.0

[GNU General Public License](https://www.gnu.org/licenses/gpl-3.0)

# TO-DOs

- [x] Add Industry List
- [x] Add mapping from TRAM
- [x] Link TMC with TRAM
- [x] Link TMC with Navigator
- [ ] Automatically download the mapping from Navigator as SVG
- [x] Export as CSV function
- [x] Edit database views
- [ ] Dockerize project 