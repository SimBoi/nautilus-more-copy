import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, GLib, Nautilus, GObject
from typing import List


# copy text to the clipboard
class ClipboardApp(Gtk.Application):
    def __init__(self, str_to_copy: str):
        super().__init__(application_id="org.example.ClipboardApp")
        self.str_to_copy = str_to_copy

    def do_activate(self):
        display = Gdk.Display.get_default()
        clipboard = display.get_clipboard()
        provider = Gdk.ContentProvider.new_for_value(self.str_to_copy)
        clipboard.set_content(provider)
        GLib.timeout_add(300, self.quit)


class MoreCopyExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        return self.generate_menu(files)

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        return self.generate_menu([current_folder])

    def generate_menu(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        submenu = Nautilus.Menu()

        multiple_files = len(files) > 1
        is_directory = not multiple_files and files[0].is_directory()

        copy_path_item = Nautilus.MenuItem(
            name="MoreCopyExtension::CopyPath",
            label="Copy Directory Path" if is_directory else "Copy File Paths" if multiple_files else "Copy File Path",
            tip="",
            icon="",
        )
        copy_path_item.connect(
            "activate",
            lambda menu_item, files=files: self.copy_path(files),
        )

        copy_name_item = Nautilus.MenuItem(
            name="MoreCopyExtension::CopyName",
            label="Copy Directory Name" if is_directory else "Copy File Names" if multiple_files else "Copy File Name",
            tip="",
            icon="",
        )
        copy_name_item.connect(
            "activate",
            lambda menu_item, files=files: self.copy_name(files),
        )

        submenu.append_item(copy_path_item)
        submenu.append_item(copy_name_item)
        menu_item = Nautilus.MenuItem(
            name="MoreCopyExtension::MoreCopy",
            label="Copy Path/Name",
            tip="",
            icon="edit-copy",
        )
        menu_item.set_submenu(submenu)

        return [
            menu_item,
        ]

    def copy_path(self, files: List[Nautilus.FileInfo]) -> None:
        paths = [file.get_location().get_path() for file in files]
        app = ClipboardApp("\n".join(paths))
        app.run()

    def copy_name(self, files: List[Nautilus.FileInfo]) -> None:
        names = [file.get_name() for file in files]
        app = ClipboardApp("\n".join(names))
        app.run()
