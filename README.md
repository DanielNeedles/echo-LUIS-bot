echo-LUIS-bot
==============
This code example uses Microsoft BOT Framework to interact with the user on the frontend and Microsofts Language Understanding (LUIS) on the backend to echo to the user LUIS's understanding of the meaning to their natural language input.  

Microsoft LUIS
--------------
For more information see the README.md in https://github.com/Microsoft/Cognitive-LUIS-Python as well as https://www.luis.ai/home

Microsoft BotBuilder Framework
--------------
For more information see the README.md in https://github.com/Microsoft/botbuilder-python as well as https://dev.botframework.com

Installation
--------------
This example program has been tested on Windows 10 with Python 3.6 and RedHat CentOS 7.2 with Python 3.6.

WINDOWS
  Install the Python modules listed in requirements.txt and then simply copy echo-LUIS-bot to the desired destination. 

LINUX (CENTOS 7.2) Vagrant on VirtualBox
  A Vagrant file is provided under echo-LUIS-bot directory.  Place this file and the echo-LUIS-bot.py file in a directory and execute "vagrant up".  

Usage
--------------
This example program has been tested on Windows 10 with Python 3.6 and RedHat CentOS 7.2 with Python 3.6.  Once the program and all dependencies are installed, it can be tested using Microsofts Bot Framework Emulator:

            Directions:
            1. Open the first Terminal Window and start the bot. For example:
                Linux CentOS: python3.6 echo-LUIS-bot.py
                Windows 10: py echo-LUIS-bot.py
            2. Open a second Terminal window and run the Emulator.  For example:
                cd /vagrant/BotFramework-Emulator
                sudo npm run start
            4. Converse with the bot using the Emulator.  For example:
                a. Enter the endpoint as:
                  http://localhost:9000/api/message and click connect
                b. Enter the default APP ID (HINT: cut and paste from the prompt)
                c. Enter the default APP KEY (HINT: cut and paste from the prompt)
                d. Enter text for LUIS to render.  For example the text:
                  Start a run
                e. Examine the LUIS returned text.  From the example above:
                   LUIS says: --------------------------------------------- LUIS Response:
                   Query: Start a run
                   Top Scoring Intent: Fitness.Activity
                   Entities:
                   'start': (Type: Fitness.Activity, Score: 0.840186954)
                   
                   'run': (Type: Fitness.ActivityType, Score: 0.956281543)

License
=======
The standard MIT license applies, inherited from the two underlying Microsoft projects.  

Developer Code of Conduct
=======
From the Microsoft LUIS SDK:
"Developers using Cognitive Services, including this client library & sample, are required to follow the “[Developer Code of Conduct for Microsoft Cognitive Services](http://go.microsoft.com/fwlink/?LinkId=698895)”."

