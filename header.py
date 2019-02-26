import shutil
from textwrap import TextWrapper

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
               .++++++'  '++++++.                
              .++++++      ++ 4 +.               
             ;+++++:        '+ 4 +.              
          ;+++++++,          ,+ / +++'           
         '++++++++:          :++ 9 +++'          
         '++' '+++'          '++++'+++'          
          ';   +'              '+'  ;'           
                                 '              
'''


def print_header(width=None):
    # Fill width of screen
    if not width:
        width = shutil.get_terminal_size(fallback=(100, 24))[0]

    logo = LOGO.replace('\n', '\n' + ' ' * int((width - 50) / 2))
    print(logo)

    print(('{:^' + str(width) + '}').format('FRC Team 449, The Blair Robot Project'))
    print(('{:^' + str(width) + '}').format('Bluetooth Scouting Server'))
    print('-' * width)
    print(('{:^' + str(width) + '}').format('Runs with Python3 on Linux'))
    print(('{:^' + str(width) + '}').format('Writen by Carter Wilson, 2019'))
    print('=' * width + '\n')

    print('Instructions for use:')
    tw = TextWrapper(width=width)
    print(tw.fill(
        'This server is intended for use with the Team 449 scouting app (and strategy app) for android.') + '\n' +
          tw.fill('On each scouting tablet, please launch the scouting app, select your device name from the ' +
                  'popup, and press connect. If there is no popup, press the Bluetooth icon in the top right ' +
                  'corner of the app.') + '\n' +
          tw.fill('When connected, you should receive a popup in the app informing you that a connection was ' +
                  'made, as well as output from this server with the MAC of the device.') + '\n' +
          tw.fill('To quit the server, press Ctrl-C, confirm that you want to quit, wait for the server to close, ' +
                  'and press Ctrl-C again.'))
    print('_' * width + '\n\n')
