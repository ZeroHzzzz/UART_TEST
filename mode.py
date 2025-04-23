import serial

class Serial_Mode:
    port:str
    baudrate:int
    timeout:int
    ser:serial.Serial
    receive_data_buffer = bytearray(5) # 接收数据缓冲区
    receive_data_count = 0 # 接收数据计数器
    receive_output_hex = False
    receive_output_speed = True

    def __init__(self, port: str, baudrate: int, timeout: int = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def open(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Serial port {self.port} opened successfully.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            raise

    def close(self):
        if self.ser.is_open:
            self.ser.close()
            print(f"Serial port {self.port} closed.")

    def single_send_data(self, left_duty: int, right_duty: int):
        """
        向串口发送占空比数据包。
        :param left_duty: 左侧占空比（范围 -9999 到 9999）
        :param right_duty: 右侧占空比（范围 -9999 到 9999）
        """
        send_data_buffer = bytearray(7)
        send_data_buffer[0] = 0xA5  # 帧头
        send_data_buffer[1] = 0x01  # 功能字

        send_data_buffer[2] = (left_duty >> 8) & 0xFF  # 高八位
        send_data_buffer[3] = left_duty & 0xFF         # 低八位

        send_data_buffer[4] = (right_duty >> 8) & 0xFF  # 高八位
        send_data_buffer[5] = right_duty & 0xFF         # 低八位

        checksum = sum(send_data_buffer[:6]) & 0xFF
        send_data_buffer[6] = checksum

        self.ser.write(send_data_buffer)
        print("Sent data: " + " ".join(f"0x{byte:02X}" for byte in send_data_buffer))
        
    def single_receive_data(self):
        while self.ser.in_waiting > 0:
            receive_data = self.ser.read(1)[0]

            if receive_data == 0xA5 and self.receive_data_count == 0:
                self.receive_data_count = 0

            self.receive_data_buffer[self.receive_data_count] = receive_data
            self.receive_data_count += 1

            if self.receive_data_count >= 5:
                if self.receive_data_buffer[0] == 0xA5:
                    if self.receive_output_hex:
                        print("Received Data Frame:", " ".join([f"{byte:02X}" for byte in self.receive_data_buffer]))

                    sum_check_data = sum(self.receive_data_buffer[:4]) & 0xFF
                    if sum_check_data == self.receive_data_buffer[4]:
                        if self.receive_data_buffer[1] == 0x02:
                            speed_data_raw = (
                                (self.receive_data_buffer[2] << 8) |
                                self.receive_data_buffer[3]
                            )

                            if speed_data_raw & 0x8000:  # 检查最高位是否为 1（负数）
                                speed_data = speed_data_raw - 0x10000  # 转换为负数
                            else:
                                speed_data = speed_data_raw

                            if self.receive_output_speed:
                                print(f"Speed Data: {speed_data}")
                    else:
                        print("Checksum Error!")
                else:
                    print("Invalid Frame Header!")

                # 清空缓冲区，准备接收下一帧数据
                self.receive_data_count = 0
                self.receive_data_buffer = bytearray(5)

    def main_send_data(self, duty):
        send_data_buffer = bytearray(5)
        send_data_buffer[0] = 0xA5  # 帧头
        send_data_buffer[1] = 0x02  # 功能字

        send_data_buffer[2] = (duty >> 8) & 0xFF  # 高八位
        send_data_buffer[3] = duty & 0xFF         # 低八位

        checksum = sum(send_data_buffer[:4]) & 0xFF
        send_data_buffer[4] = checksum

        self.ser.write(send_data_buffer)
        print("Sent data: " + " ".join(f"0x{byte:02X}" for byte in send_data_buffer))
