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

Usage
--------------
This example program has been tested on Windows 10 with Python 3.6 and RedHat CentOS 7.2 with Python 3.6.  Once the program and all dependencies are installed, it can be tested using Microsofts Bot Framework Emulator:

            Directions:
            1. Open the first Terminal Window and start the bot. For example:
                python3.6 echo-LUIS-bot.py
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
                e. Examine the LUIS returned text

License
=======
The standard MIT license applies, inherited from the two underlying Microsoft projects.  

Developer Code of Conduct
=======
From the Microsoft LUIS SDK:
"Developers using Cognitive Services, including this client library & sample, are required to follow the “[Developer Code of Conduct for Microsoft Cognitive Services](http://go.microsoft.com/fwlink/?LinkId=698895)”."

