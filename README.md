# Open-Inventory

### Version: 
1.0

### Designation:
Open-source

### License: 
GNU General Public License v3.0

### Description:
Open Inventory is a simple, open-source solution to inventory management, written in Python. It is, at the time of this writing, being developed as part of my Senior Design Project at the American University of Nigeria (AUN), for the Fall 2018 semester.

### Languages:
* Python (user interface, programming logic, business rules)
* SQLite (database)

### Modules, Extensions & Libraries:
* ```tkinter``` (GUI)
* ```Pmw``` (GUI)
* ```webbrowser``` (link to GitHub)
* ```re``` (regular expressions)
* ```sqlite3``` (database connectivity)
* ```pandas``` (data science)
* ```matplotlib``` (data science)

### Lines of Code:
* 2800+

### Platform Dependencies:
* **Hardware:** PC
* **Operating System:** Windows

### Future Implementations:
Circumstances permitting, Open Inventory will eventually be migrated to a Python-based web-development framework -- preferably Django -- which will allow for far more features and flexibility.

### For Developers:

#### Running from source:
The root file for the application is ```open-inventory.py```. With Python (at least 3.5) installed on your system, run it in Command Prompt/Terminal (code may need to be tweaked a bit for Linux) from wherever the file is saved, using 
```bash
  python open-inventory.py
  ```
#### Dependencies:
All the above modules come with the Python installation by default, except ```Pmw```, ```pandas``` and ```matplotlib```. These must be installed using ```pip```.

#### Packaging:
I packaged the source code into an executable using Python's ```auto-py-to-exe``` module, which can be downloaded using ```pip```. Due to some as yet unknown bug, the ```icons``` folder, the ```data.sqlite``` file, and the ```Pmw``` folder installed on the local disk with ```pip```, each have to be specified as additional files during packaging for the application to work. It's basically a hack that I figured out and didn't question much because it worked. The ```icons``` folder should be placed in root folder for the executable, in a folder named "icons". The ```data.sqlite``` file is the database itself, and should be placed directly in the root folder for the executable. The ```Pmw``` folder should be placed in root folder for the executable, in a folder named "Pmw". Look up ```auto-py-to-exe``` for more info about usage.  
