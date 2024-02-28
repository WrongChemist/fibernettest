## Fibernet job application demo site automated test
Below are all the instructions, explanations, details, and caveats for the automated test demonstration.  

## WARNING
Due to time constraints, a slow work terminal, and CloudFlare present on the test website, running the script may produce HIGHLY INCONSISTENT results, such as slowdoown or lockouts.  
Using a protection system on a public-facing website is non-negotiable, but bypassing it consistently would take time that isn't available.  
Reference videos are included, demonstrating the functionality on my native machine, one for each browser.  

### Requirements:
To run the test script, you will need the following:  
1. Python 3.12+ (https://www.python.org/downloads/)  
2. pytest module  
3. Selenium module  
(All requirements can be downloaded from provided links, using the requirements.txt file (cmd -> "pip install -r requirements.txt" , once Python is installed), and are already included among the provided files (simply use the provided venv))  

The file repository should be placed in your computer's C:\tmp folder and run from there.

### Running:
To run the automated test, first make sure the repository is corretly placed in the C:\tmp folder.  
Then, open the main.py file using any Python script editor (such as PyCharm or similar), and use the green "Play" / "Run" buttons.  
Alternatively, open the cmd window to the project folder, and enter "python main.py"  

### Configuration file:
A configuration file is included - fbrntConfig.ini  
Driver and exe paths should be changed if the project folder is moved from C:\tmp, or if the user's Firefox installation isn't at the default location.  
Browsers can be set to "chrome" or "firefox"  
The names, email, and password of the new user can be changed in the "User" section.  
Version, OS, and OS_Version are currently unused.  
All other parameters are unused, or should remain unchanged (such as the test site address).  

### What is included:
A set of basic tests, using the pytest framework, testing basic site functionality (buttons, links, menus) and appearance (text, images).  
Basic security tests are also included (XSS, anti-bot).   

### To be implemented:
1. Multi-column dropdown handling.
2. Testing for navigation using the side-menu in the store's item browser was ommited due to time constraint (would have worked similarly to testing the store navigation from the header drodpowns - counter how many are present, go through each and make sure they lead to the correct page, and make sure the displayed numbers of items match).   
3. Implementation for the Allure test result visualizer (again, due to needing a day or two that was not available).  
4. Refined test parameters and reporting, depending on requirements and what faults are found (currently, the tests can only "fail" in general, without specifying causes).  
5. Automated updating of browser drivers, per installed browser version. This would eliminate the need for manual updates.  

### Known issues with the site itself:
1. Using the "Search" function while the Search field isn't empty will lead to an "Internal error" page.  
2. Carousel items doono't link to the correct page.  
3. The second carousel item doesn't have a link at all, and clicking it does nothing.  
4. Item shop categories show incorrect numbers.  
5. New users aren't actually registered, and it is impossible to login to the site.  
6. Items can't be added to the shopping cart ("Added" notification appears, but the cart stays empty).  
7. Individual item pages show inconsistent information, tabs, and fields.  

### Challenges and limitations:
1. CloudFlare, an anti-bot protection system, cannot currently be bypassed - an "iframe" component is used, which Selenium has a hard time dealing with. Other methods, such as flag-switching or cookie-spoofing have also failed. This thus requires avoiding the protection, instead of challenging it, which means longer wait times between actions.  
2. Firefox driver configuration was a hassle, but it works.  
