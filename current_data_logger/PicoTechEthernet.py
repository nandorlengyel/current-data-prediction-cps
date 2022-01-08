"""."""
import socket
import binascii

socket.setdefaulttimeout(1)  # for disconnection cases, otherwise it stalls


class PicoTechEthernet(object):
    """."""

    def connect(self):
        """Connect to device."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # prepare socket for UDP
        self.socket.connect((self.ip, self.port))  # Connect
        self.socket.send('\x00'.encode('ascii'))  # Greet
        recv = self.socket.recv(200)

        if recv.startswith(self.model):
            # Get an initial response
            return(recv)
        else:
            print(recv)
            return(False)

    def lock(self):
        """Establish control of device."""
        return(self.set(
            'lock\x00',
            [b'Lock Success\x00',
             b'Lock Success (already locked to this machine)\x00']
        ))

    def alive(self):
        """Send the keepalive command."""
        # print('alive')
        return(self.set('4', b'Alive\x00'))

    def set(self, value, response=False):
        """Send text, if required check response."""
        self.socket.send(value.encode('ascii'))

        if response is not False:

            recv = self.socket.recv(60)
            # print(recv)
            if type(response) == list:
                for item in response:
                    if recv == item:
                        return(True)
            else:
                if recv == response:
                    return(True)
            print(recv)
            return(False)

        else:
            return(True)

    def filter(self, Hz=50):
        """Set the filters for 50 or 60 Hz mains."""
        if filter == 50:
            self.socket.send('\x30\x00'.encode('ascii'))
        else:
            if filter == 60:
                self.socket.send('\x30\x01'.encode('ascii'))
        # print(self.socket.recv(136))

    def EEPROM(self):
        """Read the EEPROM."""
        self.socket.send('2'.encode('ascii'))  # Ask for EEPROM of device
        EEPROM = self.socket.recv(136)
        # Parse EEPROM
        return(EEPROM)

    def read(self):
        """Read value from device."""
        recv = self.socket.recv(60)
        if len(recv) == 20:  # assume len of 20 is valid data
            return(binascii.hexlify(recv).decode())
        else:
            print(recv)
            return(False)

    def __next__(self):
        """Read values and decode."""
        while True:  # Loop forever
            self.alive()
            for _ in range(12):  # every 12 reads send/read a keepalive
                read = self.read()
                if read is not False:
                    channel, value = self.decode(read)
                    # print(channel, value)
                    yield {'channel': channel, 'value': value}


class PicoTechEthernetCM3(PicoTechEthernet):
    """."""

    def __init__(self, ip='127.0.0.1', port=6554):
        """."""
        self.model = b'CM3'
        self.ip = ip
        self.port = port

    def decode(self, data='00200059120120005b8b0220005ce30320005b97'):  # = CH0: ~ 0.218 mV
        """."""
        channel, zero, one, two, three = data[0:2], int(data[3:10], 16), int(data[13:20], 16), int(data[23:30], 16), int(data[33:40], 16)

        # result = (2.5 * (float(zero+one+two+three) / 4) * 1000) / 2**28
        # result = ((float(zero+one+two+three) / 4) * 2500) / 2**28  # combine the multipliers
        # result = (float(zero+one+two+three) * 625) / 2**28  # remove the /, scale the multipler down by 4
        result = (zero + one + two + three) * 625 / 2**28  # simplify the brackets

        channeloffset = {'00': 0, '04': 1, '08': 2}
        return channeloffset[channel], result


'''
# ? setup channels details required
\x3166
\x3144
\x3100
\x3000
\x3111
\x3133
\x3177
'''

