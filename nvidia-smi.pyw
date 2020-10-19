import os
import re
import time
import threading
import tkinter as tk
import tkinter.font as tk_font

pattern = re.compile("Power Draw.*?: (.*?) W")


def read_smi():
    with os.popen("nvidia-smi.exe -q -d power") as f:
        return f.read()


class Avg:
    powers = []
    time = 0.25
    total_time = 5
    avg_count = int(total_time / time)

    def cal(self, cur_power):
        cur_power = float(cur_power)
        self.powers.append(cur_power)
        if len(self.powers) >= self.avg_count:
            self.powers.pop(0)
        return sum(self.powers) / len(self.powers)


def update():
    avg = Avg()
    while True:
        command = read_smi()
        match = pattern.findall(command)
        power = avg.cal(match[0])
        time.sleep(avg.time)
        power_num = "cur:{:.2f}W\n{}s:{:.2f}W".format(float(match[0]), avg.total_time, power)
        text.set(power_num)


if __name__ == '__main__':
    gui = tk.Tk()
    gui.title("nvidia-power")
    x = int(gui.winfo_screenwidth() / 6)
    y = int(0.2 * x)
    gui.geometry("{}x{}".format(x, y))
    text = tk.StringVar()
    font = tk_font.Font(size=20)
    label = tk.Label(gui, textvariable=text, font=font)
    label.pack()
    threading.Thread(target=update, daemon=True).start()
    gui.mainloop()
