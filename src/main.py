import os
import sys
import gi
import pygit2

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib


class Application(Gtk.Application):
    __APP_ID__ = 'com.hack_computer.BuilderToolbox'

    __DBUSIface__ = ('''
    <node>
      <interface name="com.hack_computer.Toolbox">
        <method name="Init">
          <arg type="s" direction="in" name="appId"/>
          <arg type="s" direction="out" name="toolboxId"/>
        </method>
        <method name="Flip">
          <arg type="s" direction="in" name="appId"/>
        </method>
        <method name="FlipBack">
          <arg type="s" direction="in" name="appId"/>
        </method>
      </interface>
    </node>
    ''')

    _builder_action_group = None
    _apps = {}
    _gnome_apps = {
        'org.gnome.Weather': 'gnome-weather',
        'org.gnome.Calendar': 'gnome-calendar',
        'org.gnome.Boxes': 'gnome-boxes',
        'org.gnome.Games': 'gnome-games',
        'org.gnome.Maps': 'gnome-maps',
        'org.gnome.Music': 'gnome-music',
        'org.gnome.Nautilus': 'gnome-nautilus',
        'org.gnome.Photos': 'gnome-photos',
        'org.gnome.SoundRecorder': 'gnome-sound-recorder',
    }

    def __init__(self):
        super().__init__(application_id=self.__APP_ID__,
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        builder_id = 'org.gnome.Builder'
        builder_path = '/org/gnome/Builder'
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self._builder_action_group = Gio.DBusActionGroup.get(bus, builder_id, builder_path)
        self._builder_action_group.list_actions()

    def do_activate(self):
        pass

    def do_dbus_register(self, connection, path):
        introspection_data = Gio.DBusNodeInfo.new_for_xml(self.__DBUSIface__)
        connection.register_object(path,
                                   introspection_data.interfaces[0],
                                   self.handle_method_call,
                                   None)
        return Gtk.Application.do_dbus_register(self, connection, path)

    def handle_method_call(self, connection, sender, object_path,
                           interface_name, method_name, parameters,
                           invocation):
        args = parameters.unpack()
        if not hasattr(self, method_name):
            invocation.return_dbus_error("org.gtk.GDBus.Failed",
                                         "This method is not implemented")
            return

        invocation.return_value(getattr(self, method_name)(*args))

    # DBUS methods
    def Init(self, app_id):
        '''
        Get the source code of the application in ~/Projects/{app_name}

        This tries to clone the repository and if it exists a pull is done.
        '''

        # TODO: Provide this code in the app to make this work without connection
        # and faster

        app_name = self._gnome_apps.get(app_id, None)
        url = f'https://gitlab.gnome.org/GNOME/{app_name}.git'
        path = os.path.expanduser(os.path.join('~', 'Projects', app_name))
        self._apps[app_id] = path

        if os.path.exists(path):
            # TODO: Do a git pull
            pass
        else:
            pygit2.clone_repository(url, path)

        return GLib.Variant('(s)', ('org.gnome.Builder', ))

    def Flip(self, app_id):
        '''
        Launches the gnome-builder loading the corresponding source code path
        '''
        self._builder_action_group.activate_action(
            'load-project', GLib.Variant('s', self._apps[app_id]))

    def FlipBack(self, app_id):
        # TODO: build and replace the app window?
        pass


def main(version):
    app = Application()
    return app.run(sys.argv)
