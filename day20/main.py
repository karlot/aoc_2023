import sys
from collections import deque
from rich.pretty import pprint


# I guess our hashmap of modules, starts with implicit button
modules = {}
total_lo = 0
total_hi = 0

class Broadcast():
    def __init__(self, outputs):
        # self.sent_lo = 0
        # self.sent_hi = 0
        self.name = "broadcaster"
        self.outputs = outputs if outputs else []   # Normally names of connected modules

    # def __repr__(self):
    #     return f"(name={self.name}, type=broadcaster, outputs={self.outputs})"

    def process(self, src, signal):
        # print(f"<< '{self.name}' sending next signal:{signal} to {self.outputs}")
        global total_hi
        global total_lo
        if signal == 1:
            total_hi += len(self.outputs)
        else:
            total_lo += len(self.outputs)
        return self.name, signal, self.outputs


class FlipFlop():
    def __init__(self, name, outputs=[]):
        # self.sent_lo = 0
        # self.sent_hi = 0
        self.name = name
        self.outputs = outputs  # Connected output modules
        self.enabled = False
        self.ignore = False

    def process(self, src, signal_in):
        # print(f">> %{self.name}' received input from {src}:{input}, ON={self.enabled}")
        if signal_in == 1:
            # print(f"!! %{self.name} received:1, ignoring...!")
            return
        # print(f"!! %{self.name}' flipping state ON from {self.enabled} to {not self.enabled}")
        self.enabled = not self.enabled         # Flip on/off
        signal_out = 1 if self.enabled else 0   # Send high(1) when ON, lo(0) when OFF
        # print(f"<< %{self.name} sending next signal:{signal_out} to {self.outputs}")
        global total_hi
        global total_lo
        if signal_out == 1:
            total_hi += len(self.outputs)
        else:
            total_lo += len(self.outputs)
        return self.name, signal_out, self.outputs


class Conjunction():
    def __init__(self, name, outputs=[], sources=[]):
        # self.sent_lo = 0
        # self.sent_hi = 0
        self.name = name
        self.outputs = outputs  # Connected output modules
        self.memory = {}
        for s in sources:
            self.memory[s] = 0
    
    def process(self, src, signal_in):
        # print(f">> &{self.name} received input from '{src}':{input}")
        self.memory[src] = signal_in
        # print(f"!! &{self.name} memory: {self.memory}")
        signal_out = 0 if all([True if v == 1 else False for v in self.memory.values()]) else 1
        # print(f"<< &{self.name} sending next signal:{signal_out} to {self.outputs}")
        global total_hi
        global total_lo
        if signal_out == 1:
            total_hi += len(self.outputs)
        else:
            total_lo += len(self.outputs)
        return self.name, signal_out, self.outputs




def main(filename):
    """
    # Results:
    Part1: 794930686
    Part2:
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())

    # Reverse lookup to find out all modules that point to specific module (mainly used by Conjunction module )
    rev = {}
    for line in lines:
        m, t = line.split(" -> ")
        if m[0] == "%" or m[0] == "&":
            m = m[1:]
        for targ in t.split(", "):
            if not targ in rev:
                rev[targ] = [m]
            else:
                rev[targ].append(m)

    for line in lines:
        m, t = line.split(" -> ")
        outputs = t.split(", ")
        if m[0] == "%":
            name = m[1:]
            # print(f"+ Adding FlipFlop module: {name} -> {outputs}")
            modules[name] = FlipFlop(name, outputs)
        elif m[0] == "&":
            name = m[1:]
            # print(f"+ Adding Conjunction module: {name} -> {outputs}")
            modules[name] = Conjunction(name, outputs, sources=rev[name])
        else:
            # print(f"+ Adding Broadcast module: -> {outputs}")
            name = m
            modules[name] = Broadcast(outputs)
    
    Q = deque()
    global total_lo
    global total_hi

    for _ in range(1000):
        # print(f"---- PUSHING BUTTON ----")
        # We push a button, starting a "broadcaster"
        total_lo += 1
        current_module = "broadcaster"
        Q.append(modules[current_module].process("button", 0))

        while Q:
            src, sig, dst = Q.popleft()
            # pprint((src, sig, dst))
            for n in dst:
                if n in modules:
                    out = modules[n].process(src, sig)
                    if out: Q.append(out)


    print(f"Part1: {total_lo * total_hi}")
    # print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
