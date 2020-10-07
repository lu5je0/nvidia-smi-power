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
    avg_count = 10

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
        time.sleep(0.25)
        power_num = "power:{:.2f}W".format(power)
        text.set(power_num)
        print(power_num, end="\r")


if __name__ == '__main__':
    gui = tk.Tk()
    gui.title("nvidia-power")
    x = int(gui.winfo_screenwidth() / 6)
    y = int(0.3 * x)
    gui.geometry("{}x{}".format(x, y))
    text = tk.StringVar()
    font = tk_font.Font(size=20)
    label = tk.Label(gui, textvariable=text, font=font)
    label.pack()
    threading.Thread(target=update, daemon=True).start()
    gui.mainloop()
