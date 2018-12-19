# Open Inventory

### Version: 
1.0

### Designation:
Open-source

### License: 
GNU General Public License v3.0

### Description:
Open Inventory is a simple, open-source solution to inventory management, written in Python. It was developed as my Senior Design Project at the American University of Nigeria (AUN), for the Fall 2018 semester.

### Languages:
* Python (user interface, logic, business rules)
* SQLite (database)

### Modules:
* ```tkinter``` (GUI)
* ```Pmw``` (GUI)
* ```webbrowser``` (link to GitHub)
* ```re``` (regular expressions)
* ```sqlite3``` (database connectivity)
* ```pandas``` (data science)
* ```matplotlib``` (data science)

### Lines of Code:
* 2800+

### Platform:
* **Hardware:** PC
* **Operating System:** Windows

### For Developers:

#### Running from source:
The root file for the application is ```open-inventory.py```. With Python (at least 3.5) installed on your system, run it in Windows Command Prompt from where the file is saved, using ```python open-inventory.py```.

#### Dependencies:
All the modules listed above come with the Python installation by default, except ```Pmw```, ```pandas``` and ```matplotlib```. These must be installed using ```pip```.

#### Packaging:
I packaged the source code into an executable using Python's ```auto-py-to-exe``` module, which can be installed using ```pip```. Due to some mysterious bug, the ```icons``` source folder from the project, the ```data.sqlite``` source file from the project, and the ```<path to Pyhton's source files on your local disk>\Lib\site-packages\Pmw``` folder (least that's the path to it on my computer) each have to be specified as additional files during packaging for the application to work. It's basically a hack that I figured out and didn't question much because it worked. The ```icons``` folder should be placed in root folder for the executable, in a folder named "icons". The ```data.sqlite``` file is the database itself, and should be placed directly in the root folder for the executable. The ```Pmw``` folder should be placed in root folder for the executable, in a folder named "Pmw". Look up ```auto-py-to-exe``` for more info about usage.  
