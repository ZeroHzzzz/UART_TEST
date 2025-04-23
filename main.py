import mode
import pick

# 配置串口参数
SERIAL_PORT = 'COM3'  # 根据实际情况修改为您的串口号（如 '/dev/ttyUSB0'）
BAUD_RATE = 115200      # 波特率
TIMEOUT = 1           # 超时时间


def main():
    serial_mode = mode.Serial_Mode(SERIAL_PORT, BAUD_RATE, TIMEOUT)
    serial_mode.open()
    try:
        options = ["发送模式", "接收模式", "both"]
        title = "请选择模式："

        # 显示选项并获取用户选择
        _, index = pick.pick(options, title)
        
        if index == 0: 
            while True:
                user_input = input()
                values = user_input.strip().split()

                if len(values) != 2:
                    continue
            
                left, right = map(int, values)

                if not (-9999 <= left <= 9999) or not (-9999 <= right <= 9999):
                    continue

                serial_mode.send_duty(left, -right)
        elif index == 1:
            while True:
                serial_mode.receive_data()
        else:
            duty = int(input())
            serial_mode.send_duty(duty, duty)

            while True:
                serial_mode.receive_data()

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        serial_mode.close()

if __name__ == "__main__":
    main()