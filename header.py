from shutil import get_terminal_size
from textwrap import TextWrapper

import printing

LOGO = '''
                     ,:++:,                      
                   :++++++++:                    
            _     :++++  ++++:     _              
          ,++++:  '++++  ++++' ,:++++;           
         :++  '+:  :++++++++:  +++  ++'          
  ,++,    + THE +'   ':++:'    :+++++:     ,,:,,    
:++++++++++++++++++++++++++++++++++++++++++++-++, 
    +++++ BLAIR ++++ ROBOT +++ PROJECT ++++:   ++'
'+,++++++++++++++++++++++++++++++++++++++++++-++'
 '++++'        '++++++    ++++++'          '':'' 
                '++++++  ++++++'                 
                 '++++++++++++'                  
                  '++++++++++'                    
                   '++++++++'                     
                   :++++++++:                    
                  .++++++++++.                   
                 ++++++''++++++                 
               .++++++'  '++ 4 +.                
              .++++++      ++ 4 +.               
             ;+++++:        '+ / +.              
          ;+++++++,          ,+ 9 +++,           
         :++++++++:          :++++++++'          
         '++' '+++'          '++++'+++'          
          ';   +'              '+'  ;'           
                                 '              
'''


def print_header(width=None):
    # Fill width of screen
    if not width:
        width = get_terminal_size(fallback=(100, 24))[0]

    logo = LOGO.replace('\n', '\n' + ' ' * int((width - 50) / 2))
    printing.printf(logo, style=printing.LOGO)

    printing.printf(('{:^' + str(width) + '}').format('FRC Team 449: The Blair Robot Project'), style=printing.HEADER)
    printing.printf('=' * width, style=printing.HEADER)
    printing.printf(('{:^' + str(width) + '}').format('Bluetooth Scouting Server'), style=printing.TITLE)
    printing.printf()
    printing.printf(('{:^' + str(width) + '}').format('Runs with Python3 on Linux'), style=printing.INSTRUCTIONS)
    printing.printf(('{:^' + str(width) + '}').format('Writen by Carter Wilson, 2019'), style=printing.INSTRUCTIONS)
    printing.printf('-' * width + '\n', style=printing.INSTRUCTIONS)

    printing.printf('Instructions for use:', style=printing.INSTRUCTIONS)
    tw = TextWrapper(width=width)
    printing.printf(tw.fill(
        'This server is intended for use with the Team 449 scouting app (and strategy app) for android.') + '\n' +
        tw.fill('On each scouting tablet, please launch the scouting app, select your device name from the '
                'popup, and press connect. If there is no popup, press the Bluetooth icon in the top right '
                'corner of the app.') + '\n' +
        tw.fill('When connected, you should receive a popup in the app informing you that a connection was '
                'made, as well as output from this server with the name of the device.') + '\n' +
        tw.fill('To retrieve the data file for data analysis, plug in a USB flash drive, wait for output ' 
                'saying that it was mounted, the data was copied, and it was unmounted, then remove it.') + '\n' +
        tw.fill('If the drive does not get detected/updated, it may be because there is no new data since you last '
                'updated it. If you would still like to update it (if, for example, you switched flash drives), '
                'just type d, data, u, or update into the server.') + '\n' +
        tw.fill('To retrieve data for strategy, type "s" and hit enter, then enter the team numbers.') + '\n' +
        tw.fill('To quit the server, type "q" or "quit" and press enter, confirm that you want to ' 
                'quit, and wait for the server to close.'), style=printing.INSTRUCTIONS)
    printing.printf()
    printing.printf('-' * width + '\n\n', style=printing.UNDERLINE)
