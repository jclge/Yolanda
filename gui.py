import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)
i = 1
while i != 500:
     img = Gtk.Image.new_from_file('test/test'+str(i)+'.png')
     win.add(img)
     win.show_all()
     Gtk.main()
     i+=1
