from shutil import get_terminal_size
from textwrap import TextWrapper

from interface import printing

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
    printing.printf('-' * width + '\n', style=printing.INSTRUCTIONS)

    # printing.printf('Instructions for use:', style=printing.INSTRUCTIONS)
    # tw = TextWrapper(width=width)
    # printing.printf(tw.fill('Commands:') + '\n' +
                    # tw.fill('q: quit') + '\n' +
                    # tw.fill('d: request drive update (should be automatic)') + '\n' +
                    # tw.fill('st: send team list to all connected devices') + '\n' +
                    # tw.fill('ss: send match schedule to all connected devices'), style=printing.INSTRUCTIONS)
    # printing.printf()
    # printing.printf('-' * width + '\n\n', style=printing.UNDERLINE)
