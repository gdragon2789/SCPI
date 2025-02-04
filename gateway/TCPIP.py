# socket_instrument.py
import socket

class TCPIP_Controller:
    def __init__(self,
                 ip_address : str,
                 tcp_port: int | None = 5025,
                 timeout : float | None = 5,
                 buffer_size : int = 4096,
                 debug=False) -> None:
        """
        Initializes the TCPIP_Controller class for communicating with SCPI instruments over TCP/IP.
        :param ip_address:
        :param tcp_port:
        :param timeout:
        :param buffer_size:
        """
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.settimeout(timeout)
        self._connection.connect((ip_address, tcp_port))
        self.buffer_size = buffer_size
        self.debug = debug

        idn = self.query("*IDN?")
        if idn:
            self._idn = idn
            if self.debug:
                print(f"Connected to {idn}.")
        else:
            self.close()
            if self.debug:
                print("Socket Instrument could not be identified.")

    def write(self, command: str) -> None:
        """
        Sends a SCPI command to the instrument.

        :param command:
        :return:
        """
        command += "\n"  # Add termination
        self._connection.sendall(command.encode())

    def query(self, command: str) -> str:
        """
        Sends a SCPI command and reads the response.

        :param command: SCPI command string.
        :return: The response string from the instrument.
        """
        self.write(command)
        recv_bytes = bytes(0)
        while True:
            recv_bytes += self._connection.recv(self.buffer_size)
            if recv_bytes[-1:] == b"\n":
                return recv_bytes.decode()[:-1]

    def close(self) -> None:
        """Closes TCP/IP connection."""
        self._connection.close()

    @property
    def idn(self):
        return self._idn