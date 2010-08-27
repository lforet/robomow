# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record
import gtk

from foo.helpers import get_builder

import gettext
from gettext import gettext as _
gettext.textdomain('foo')

class PreferencesFooDialog(gtk.Dialog):
    __gtype_name__ = "PreferencesFooDialog"
    preferences = {}

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated PreferencesFooDialog object.
        """
        builder = get_builder('PreferencesFooDialog')
        new_object = builder.get_object("preferences_foo_dialog")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initalizing should be called after parsing the ui definition
        and creating a PreferencesFooDialog object with it in order to
        finish initializing the start of the new PerferencesFooDialog
        instance.
        
        Put your initialization code in here and leave __init__ undefined.
        """

        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

        # Set up couchdb and the preference info.
        self._db_name = "foo"
        self._database = CouchDatabase(self._db_name, create=True)
        self._preferences = None
        self._key = None

        # Set the record type and then initalize the preferences.
        self._record_type = (
            "http://wiki.ubuntu.com/Quickly/RecordTypes/Foo/"
            "Preferences")
        self._preferences = self.get_preferences()
        # TODO: code for other initialization actions should be added here

    def get_preferences(self):
        """Return a dict of preferences for foo.

        Creates a couchdb record if necessary.
        """
        if self._preferences == None:
            # The dialog is initializing.
            self._load_preferences()

        # If there were no saved preference, this.
        return self._preferences

    def _load_preferences(self):
        # TODO: add preferences to the self._preferences dict default
        # preferences that will be overwritten if some are saved
        self._preferences = {"record_type": self._record_type}

        results = self._database.get_records(
            record_type=self._record_type, create_view=True)

        if len(results.rows) == 0:
            # No preferences have ever been saved, save them before returning.
            self._key = self._database.put_record(Record(self._preferences))
        else:
            self._preferences = results.rows[0].value
            del self._preferences['_rev']
            self._key = results.rows[0].value["_id"]

    def _save_preferences(self):
        self._database.update_fields(self._key, self._preferences)

    def ok(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns gtk.RESONSE_OK from run().
        """

        # Make any updates to self._preferences here. e.g.
        #self._preferences["preference1"] = "value2"
        self._save_preferences()

    def cancel(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """
        # Restore any changes to self._preferences here.
        pass

if __name__ == "__main__":
    dialog = PreferencesFooDialog()
    dialog.show()
    gtk.main()
