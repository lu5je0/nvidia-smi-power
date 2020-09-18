import os
import time
import re

pattern = re.compile("Power Draw                  : (.+?) W")

def read_smi():
    with os.popen("nvidia-smi -q -d power") as f:
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

avg = Avg()

while True:
    text = read_smi()
    match = pattern.findall(text)
    power = avg.cal(match[0])
    time.sleep(0.2)
    print("{:.2f}W".format(power), end="\r")
