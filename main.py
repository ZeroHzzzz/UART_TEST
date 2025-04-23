import mode
import pick
import time

# 配置串口参数
SERIAL_PORT = 'COM3'  # 根据实际情况修改为您的串口号（如 '/dev/ttyUSB0'）
BAUD_RATE = 115200      # 波特率
TIMEOUT = 1           # 超时时间


def main():
    serial_mode = mode.Serial_Mode(SERIAL_PORT, BAUD_RATE, TIMEOUT)
    serial_mode.open()
    try:
        options = ["单驱", "主控", "Exit"]
        title = "请选择设备："
        _, index = pick.pick(options, title)

        if index == 0:
            options = ["发送模式", "接收模式", "Both", "Exit"]
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

                    serial_mode.single_send_data(left, -right)
            elif index == 1:
                while True:
                    serial_mode.single_receive_data()
            elif index == 2:
                duty = int(input())
                serial_mode.single_send_data(duty, duty)

                while True:
                    serial_mode.single_receive_data()
            else:
                return
        elif index == 1:
            tar = 1
            increment = True
            while True:
                serial_mode.main_send_data(tar)
                if increment:
                    tar += 1
                    if tar > 9999:
                        increment = False
                else:
                    tar -= 1
                    if tar < -9999:
                        increment = True
                # time.sleep(0.5)
                
        else:
            return

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        serial_mode.close()

if __name__ == "__main__":
    main()