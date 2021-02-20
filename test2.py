import queue
import threading
import time

# This program has been tested on all flavors of PySimpleGUI and it works with no problems at all
# To try something other than tkinter version, just comment out the first import and uncomment the one you want
import PySimpleGUI as sg
# import PySimpleGUIQt as sg
# import PySimpleGUIWx as sg
# import PySimpleGUIWeb as sg

# isRunning = True


def long_operation_thread(seconds, gui_queue):
    """
    A worker thread that communicates with the GUI through a queue
    This thread can block for as long as it wants and the GUI will not be affected
    :param seconds: (int) How long to sleep, the ultimate blocking call
    :param gui_queue: (queue.Queue) Queue to communicate back to GUI that task is completed
    :return:
    """
    while isRunning:
        print('Starting thread sleep for {} seconds'.format(seconds))
        time.sleep(seconds)                  # sleep for a while
        gui_queue.put('** Runnning **')  # put a message into queue for GUI
    gui_queue.put('** Done **')  # put a message into queue for GUI
    time.sleep(1)


######   ##     ## ####
##    ##  ##     ##  ##
##        ##     ##  ##
##   #### ##     ##  ##
##    ##  ##     ##  ##
##    ##  ##     ##  ##
######    #######  ####

def the_gui():
    """
    Starts and executes the GUI
    Reads data from a Queue and displays the data to the window
    Returns when the user exits / closes the window
    """

    gui_queue = queue.Queue()  # queue used to communicate between the gui and the threads

    layout = [[sg.Text('Long task to perform example')],
              [sg.Output(size=(70, 12))],
              [sg.Text('Number of seconds your task will take'), sg.Input(
                  key='_SECONDS_', size=(5, 1)), sg.Button('Do Long Task', bind_return_key=True)],
              [sg.Button('Click Me'), sg.Button('Exit')], ]

    window = sg.Window('Multithreaded Window').Layout(layout)
    # --------------------- EVENT LOOP ---------------------
    while True:
        # wait for up to 100 ms for a GUI event
        event, values = window.Read(timeout=100)
        if event is None or event == 'Exit':
            break
        elif event.startswith('Do'):
            try:
                seconds = int(values['_SECONDS_'])
                print('Starting thread to do long work....sending value of {} seconds'.format(
                    seconds))
                threading.Thread(target=long_operation_thread, args=[
                    seconds, gui_queue], daemon=True).start()
            except Exception as e:
                print('Error starting work thread. Did you input a valid # of seconds? You entered: %s' %
                      values['_SECONDS_'])
        elif event == 'Click Me':
            global isRunning
            isRunning = not isRunning
            print('Your GUI is alive and well')
        # --------------- Check for incoming messages from threads  ---------------
        try:
            message = gui_queue.get_nowait()
        # except Exception as e:
        #     print("error")
        except queue.Empty:             # get_nowait() will get exception when Queue is empty
            message = None              # break from the loop if no more messages are queued up

        # if message received from queue, display the message in the Window
        if message:
            print('Got a message back from the thread: ', message)

    # if user exits the window, then close the window and exit the GUI func
    window.Close()


##     ##    ###    #### ##    ##
###   ###   ## ##    ##  ###   ##
#### ####  ##   ##   ##  ####  ##
## ### ## ##     ##  ##  ## ## ##
##     ## #########  ##  ##  ####
##     ## ##     ##  ##  ##   ###
##     ## ##     ## #### ##    ##

if __name__ == '__main__':
    isRunning = True
    the_gui()
    print('Exiting Program')
