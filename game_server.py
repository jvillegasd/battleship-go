# https://github.com/effiongcharles/network_rock_paper_scissors_game/blob/master/game_server.py
import tkinter as tk

from networking.server import Server


class GameServer(tk.Frame):

    def __init__(self, parent: tk.Tk, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

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
        self.client_frame.pack(side=tk.BOTTOM, pady=(0, 20))

        # Define a timer for client refresh polling
        self.text_display.after(1000, self.refresh_clients_display)

    def start_server(self) -> None:
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        host_address = 'localhost'
        host_port = 65432

        self.server = Server(host_address, host_port)
        self.server.start_server()

        self.lbl_host['text'] = f'Address: {host_address}'
        self.lbl_port['text'] = f'Port: {host_port}'

    def stop_server(self) -> None:
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

        self.server.stop_server()

        self.lbl_host['text'] = 'Address: X.X.X.X'
        self.lbl_port['text'] = 'Port: XXXX'

    def refresh_clients_display(self) -> None:
        print('hi')


def main() -> None:
    root = tk.Tk(className='Battleship - Game server')
    root.geometry('300x300')
    root.resizable(width=False, height=False)

    GameServer(root).pack(side='top', fill='both', expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
