import socket
import time
import os


CRAGH_HOST = os.environ.get("CRAGH_HOST")
CRAGH_PORT = os.environ.get("CRAGH_PORT")
CRAGH_NICK = os.environ.get("CRAGH_NICK")
CRAGH_PASS = os.environ.get("CRAGH_PASS")
CRAGH_CHAN = os.environ.get("CRAGH_CHAN")

assert CRAGH_HOST, "Missing CRAGH env var 'CRAGH_HOST'"
assert CRAGH_PORT, "Missing CRAGH env var 'CRAGH_PORT'"
assert CRAGH_NICK, "Missing CRAGH env var 'CRAGH_NICK'"
assert CRAGH_PASS, "Missing CRAGH env var 'CRAGH_PASS'"
assert CRAGH_CHAN, "Missing CRAGH env var 'CRAGH_CHAN'"


class CraghBot(object):

    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, int(port)))
        self.channel = None
        self.rate_limit = (20/30)

    def login(self, password, nick, channel):
        self.channel = channel

        self.send_message("PASS {}\r\n".format(password))
        self.send_message("NICK {}\r\n".format(nick))
        self.send_message("JOIN {}\r\n".format(channel))

    def chat(self, msg, channel=None):
        channel = channel or self.channel
        self.send_message("PRIVMSG {} :{}\r\n".format(channel, msg))
        print("Trying to send message gurl", channel, msg)

    def listen_loop(self):
        response_buffer = ""
        while True:
            response_buffer += self.sock.recv(1024).decode("utf-8")
            while "\r\n" in response_buffer:
                # Grab a full message off the buffer
                split_message = response_buffer.split("\r\n")
                message = split_message[0]

                # Remove that full message from the beginning of the buffer -- +2 for \r\n
                response_buffer = response_buffer[len(message) + 2:]
                self.process_packet(message)

            time.sleep(0.1)

    def process_packet(self, packet):
        if "PING :tmi.twitch.tv" in packet:
            self.send_packet("PONG :tmi.twitch.tv\r\n")
        elif "!" in packet and "@" in packet and "PRIVMSG" in packet:
            # Chat message format looks something like:
            #     :nickname!nickname@nickname.tmi.twitch.tv PRIVMSG #channel :message
            name = packet[1:].split("!")[0]
            message = packet.split(":")[2]

            # TODO: Remove echo!
            self.chat(message)



    def send_message(self, message):
        assert "\r\n" in message, "ERROR! Tried sending message without proper terminal character \\r\\n!"
        time.sleep(1 / self.rate_limit)
        self.sock.send(message.encode("utf-8"))


if __name__ == "__main__":
    bot = CraghBot(CRAGH_HOST, CRAGH_PORT)
    bot.login(CRAGH_PASS, CRAGH_NICK, CRAGH_CHAN)
    bot.listen_loop()
