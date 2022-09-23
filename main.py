import serial
import time
import argparse

import posix_ipc


class GRBL:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate)
        # Wake up grbl
        self.ser.write("\r\n\r\n".encode("utf-8"))
        # Wait for grbl to initialize and flush startup text in serial input
        time.sleep(2)
        self.ser.flushInput()

    def home(self, log=False):
        self.ser.flushInput()
        self.ser.write("$H\n".encode("utf-8"))
        print(serca.ser.readline())
        # self.ser.write("G92X0Y0Z0\n".encode("utf-8"))
        self.ser.write("G10P0L20X0Y0Z0\n".encode("utf-8"))
        print(serca.ser.readline())

    def send(self, lines, log=False):
        self.ser.flushInput()
        l_count = 0
        for line in lines:
            l_count += 1  # Iterate line counter
            l_block = line.strip()  # Strip all EOL characters for consistency
            print(
                f"{l_count:03d}>> {l_block} <<"
                + str(self.ser.write(f"{l_block}\n".encode("utf-8")))
                + "\n"
            )  # Send g-code block to grbl
            print(f"{self.ser.readline().strip()}\n")  # Wait for grbl response

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        deion="Stream g-code to grbl. (pySerial and argparse libraries required)"
    )
    parser.add_argument("port", help="GRBL serial port")
    # parser.add_argument('file', help='G-code file to stream', required=False)
    port = parser.parse_args().port

    print("Iniciando GRBL...")
    serca = GRBL(port)
    print('Casa')
    serca.home(True)

    mq = posix_ipc.MessageQueue("/cuts", posix_ipc.O_CREAT)
    ack_mq = posix_ipc.MessageQueue("/ack", posix_ipc.O_CREAT)
    print("Conectado a fila")
    while True:
        msg = mq.receive()
        gcode_lines = msg[0].decode("utf-8").split("\n")
        print("Executando GCODE:")
        print(gcode_lines)
        serca.send(gcode_lines, log=True)
        ack_mq.send("ok")

    print("Mandando")
    # serca.send(
    #     [
    #         "G90",
    #         "G21",
    #         "G01X0Y5.2F2000",
    #         "G01X100Y5.2F2000",
    #         "G01X100Y105.2F2000",
    #         "G01X200Y105.2F2000",
    #         "G01Z-126F1000",
    #         "G01X100Y5.2F2000",
    #         "G01Z-0F1000",
    #     ]
    #     , log=True)

    # Escreve aqui
    # with open("file.gcode") as f:
    #     lines = f.readlines()
    #     print('Iniciando a transmissão do arquivo G-Code.\n')
    #     serca.send(lines, log=True)
    #     print('\nFim da transmissão.')

    serca.close()
