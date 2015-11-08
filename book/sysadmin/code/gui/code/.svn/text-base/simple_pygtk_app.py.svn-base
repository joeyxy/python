#!/usr/bin/env python

import pygtk
import gtk
import time

class SimpleButtonApp(object):
    """This is a simple PyGTK app that has one window and one button.
    When the button is clicked, it updates the button's label with the current time.
    """

    def __init__(self):
        #the main window of the application
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        #this is how you "register" an event handler.  Basically, this 
        #tells the gtk main loop to call self.quit() when the window "emits"
        #the "destroy" signal.
        self.window.connect("destroy", self.quit)

        #a button labeled "Click Me"
        self.button = gtk.Button("Click Me")

        #another registration of an event handler.  This time, when the
        #button "emits" the "clicked" signal, the 'update_button_label'
        #method will get called.
        self.button.connect("clicked", self.update_button_label, None)

        #The window is a container.  The "add" method puts the button
        #inside the window.
        self.window.add(self.button)

        #This call makes the button visible, but it won't become visible
        #until its container becomes visible as well.
        self.button.show()

        #Makes the container visible
        self.window.show()

    def update_button_label(self, widget, data=None):
        """set the button label to the current time

        This is the handler method for the 'clicked' event of the button
        """
        self.button.set_label(time.asctime())

    def quit(self, widget, data=None):
        """stop the main gtk event loop

        When you close the main window, it will go away, but if you don't
        tell the gtk main event loop to stop running, the application will
        continue to run even though it will look like nothing is really 
        happening.
        """
        gtk.main_quit()


    def main(self):
        """start the gtk main event loop"""
        gtk.main()

if __name__ == "__main__":
    s = SimpleButtonApp()
    s.main()

