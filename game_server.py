import tkinter as tk
from types import TracebackType
from typing import Optional, Type

from networking.server import Server


class GameServerWindow(object):
    """ This class manages game server frame. """

    def __init__(self) -> None:
        self.parent = tk.Tk(className='Battleship - Game server')
        self.parent.geometry('300x300')
        self.parent.resizable(width=False, height=False)
        self.parent.eval('tk::PlaceWindow . center')

        # Core attributes
        self.server = None
        # self.parent = parent
        self.polling_interval = 1000

        # Top frame for start and stop game server
        self.top_frame = tk.Frame(self.parent)
        self.start_btn = tk.Button(
            self.top_frame, text='Start', command=lambda: self.start_server())
        self.start_btn.pack(side=tk.LEFT)
        self.stop_btn = tk.Button(
            self.top_frame, text='Stop', command=lambda: self.stop_server(), state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)
        self.top_frame.pack(side=tk.TOP, pady=(5, 0))

        # Middle frame for showing Server IP address and Port
        self.mid_frame = tk.Frame(self.parent)
        self.lbl_host = tk.Label(self.mid_frame, text='Address: X.X.X.X')
        self.lbl_host.pack(side=tk.LEFT)
        self.lbl_port = tk.Label(self.mid_frame, text='Port: XXXX')
        self.lbl_port.pack(side=tk.LEFT)
        self.mid_frame.pack(side=tk.TOP, pady=(5, 0))

        # Client frame for show connected clients
        self.client_frame = tk.Frame(self.parent)
        self.lbl_line = tk.Label(
            self.client_frame, text='**********Client List**********').pack()
        self.text_display = tk.Text(self.client_frame, height=10, width=30)
        self.text_display.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text_display.config(background='#F4F6F7',
                                 highlightbackground='grey', state='disabled')
        self.client_frame.pack(side=tk.TOP, pady=(5, 0))

        # Dev sign frame
        self.dev_sign_frame = tk.Frame(self.parent)
        self.lbl_dev_sign = tk.Label(
            self.dev_sign_frame, text='Made by jvillegasd :D')
        self.lbl_dev_sign.pack(side=tk.RIGHT)
        self.dev_sign_frame.pack(side=tk.BOTTOM, pady=(0, 20))

        # Define a timer for client refresh polling
        self.text_display.after(self.polling_interval,
                                self.refresh_clients_display)

    def __enter__(self) -> 'GameServerWindow':
        return self

    def __exit__(
            self,
            exctype: Optional[Type[BaseException]],
            excinst: Optional[BaseException],
            exctb: Optional[TracebackType]) -> None:
        """ This build-in function close server if window is closed. """
        if self.server:
            self.server.stop_server()
            self.server = None

    def start_server(self) -> None:
        """ This function starts a new server instance. """

        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        host_address = 'localhost'
        host_port = 65432

        self.server = Server(host_address, host_port)
        self.server.start_server()

        self.lbl_host['text'] = f'Address: {host_address}'
        self.lbl_port['text'] = f'Port: {host_port}'

    def stop_server(self) -> None:
        """ This function stops current server instances and delete it. """

        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

        self.server.stop_server()
        self.server = None

        self.lbl_host['text'] = 'Address: X.X.X.X'
        self.lbl_port['text'] = 'Port: XXXX'

    def refresh_clients_display(self) -> None:
        """ This function polls connected clients to current server. """

        if self.server:
            connected_clients = self.server.get_connected_clients()
            self.text_display.config(state=tk.NORMAL)
            self.text_display.delete('1.0', tk.END)

            for client_name in connected_clients:
                self.text_display.insert(tk.END, client_name + '\n')

            self.text_display.config(state=tk.DISABLED)

        self.text_display.after(self.polling_interval,
                                self.refresh_clients_display)


def main() -> None:
    with GameServerWindow() as gs:
        gs.parent.mainloop()


if __name__ == '__main__':
    main()
