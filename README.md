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
flask run
```

Once the server has started, access the application through localhost:5555.

To change the port and make the app publicly available, you can run the following command:

```
flask run -p <number> -h 0.0.0.0
```

## Deleting & Reloading the database

Reinitilizating the database will erase any content already loaded in it. 

```
export FLASK_APP=tmc
flask init-db
flask run
```
To reload the database with the data from [ATT&CK](https://attack.mitre.org/) access the following path:

```
localhost:5555/first-time
```
Please be patiente, since this operation really takes a while.

# Author

* Valentina Palacin [@fierytermite](https://twitter.com/fierytermite) 

# License: GPL-3.0

[GNU General Public License](https://www.gnu.org/licenses/gpl-3.0)

# TO-Do

- [ ] Add Industry List
- [ ] Add mapping from TRAM
- [ ] Link TMC with TRAM
- [ ] Link TMC with Navigator
- [ ] Download TMC mapping from Navigator as SVG
- [ ] Export as CSV function
- [ ] Edit database screens
- [ ] Dockerize project