import sys
from collections import deque
from math import lcm


class Button():
    def __init__(self):
        self.sent_lo = 0
        self.sent_hi = 0
        self.name = "button"
    
    def press(self):
        self.sent_lo += 1
        return self.name, 0, ["broadcaster"]


class Broadcast():
    def __init__(self, outputs):
        self.sent_lo = 0
        self.sent_hi = 0
        self.name = "broadcaster"
        self.outputs = outputs if outputs else []   # Normally names of connected modules

    def process(self, src, signal):
        # print(f"<< {self.name} sending next signal:{signal} to {self.outputs}")
        if signal == 1:
            self.sent_hi += len(self.outputs)
        else:
            self.sent_lo += len(self.outputs)
        return self.name, signal, self.outputs


class FlipFlop():
    def __init__(self, name, outputs=[]):
        self.sent_lo = 0
        self.sent_hi = 0
        self.name = name
        self.outputs = outputs  # Connected output modules
        self.enabled = False

    def process(self, src, signal_in):
        # print(f">> %{self.name} received input from {src}:{input}, ON={self.enabled}")
        if signal_in == 1:
            # print(f"!! %{self.name} received:1, ignoring...!")
            return
        # print(f"!! %{self.name} flipping state ON from {self.enabled} to {not self.enabled}")
        self.enabled = not self.enabled         # Flip on/off
        # print(f"<< %{self.name} sending next signal:{signal_out} to {self.outputs}")
        signal_out = 1 if self.enabled else 0   # Send high(1) when ON, lo(0) when OFF
        if signal_out == 1:
            self.sent_hi += len(self.outputs)
        else:
            self.sent_lo += len(self.outputs)
        return self.name, signal_out, self.outputs


class Conjunction():
    def __init__(self, name, outputs=[], sources=[]):
        self.sent_lo = 0
        self.sent_hi = 0
        self.name = name
        self.outputs = outputs  # Connected output modules
        self.memory = {}
        for s in sources:
            self.memory[s] = 0
    
    def process(self, src, signal_in):
        # print(f">> &{self.name} received input from {src}:{input}")
        self.memory[src] = signal_in
        # print(f"!! &{self.name} memory: {self.memory}")
        # print(f"<< &{self.name} sending next signal:{signal_out} to {self.outputs}")
        signal_out = 0 if all([True if v == 1 else False for v in self.memory.values()]) else 1
        if signal_out == 1:
            self.sent_hi += len(self.outputs)
        else:
            self.sent_lo += len(self.outputs)
        return self.name, signal_out, self.outputs


def get_rev_dict(lines):
    """
    Reverse lookup to find out all modules that point to specific module
    (mainly used by Conjunction module ) 
    """
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
    return rev


def populate_modules(lines, rev):
    """
    Populate modules based on input lines, and use reverse lookup to
    set Conjunction links to initial values (lo)
    """
    modules = {}
    for line in lines:
        m, t = line.split(" -> ")
        outputs = t.split(", ")     # list of linked output modules
        if m[0] == "%":
            name = m[1:]
            modules[name] = FlipFlop(name, outputs)
        elif m[0] == "&":
            name = m[1:]
            modules[name] = Conjunction(name, outputs, sources=rev[name])
        else:
            name = m
            modules[name] = Broadcast(outputs)
    return modules


def main(filename):
    """
    # Results:
    Part1: 794930686
    Part2: 25353592599423
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())

    # Some switches when running only single part
    run_part1 = True
    run_part2 = True

    # Load reverse lookup table
    rev = get_rev_dict(lines)

    # Populate module list, and add our button to the modules as well (button presses are counting)
    modules = populate_modules(lines, rev)
    modules["button"] = Button()

    # ---------------------------------
    # Part 1
    # ---------------------------------
    if run_part1:
        Q = deque()
        BUTTON_PRESSES = 1000
        for _ in range(BUTTON_PRESSES):
            # We push a button, starting a "broadcaster"
            Q.append(modules["button"].press())

            # Run while there is something in queue
            while Q:
                src, sig, dst = Q.popleft()
                for n in dst:
                    if n in modules:
                        out = modules[n].process(src, sig)
                        if out: Q.append(out)

        # Count how many lo and hi signals are sent, and multiply them
        total_lo = sum(m.sent_lo for m in modules.values())
        total_hi = sum(m.sent_hi for m in modules.values())
        print(f"Part1: {total_lo * total_hi}")


    # ---------------------------------
    # Part 2
    # ---------------------------------
    if run_part2:
        # We cant press button that many times to get RX node to get "lo" signal, so we need to inspect input and detect
        # connected segments in which button press cycles they feed towards RX to detect cycle-lengths and compute LCM
        (rx_inverter,)    = rev["rx"]           # from input data, assume single conjunction module inputs to RX (inverter)
        rx_inverter_feeds = rev[rx_inverter]    # into conjunction node pre-rx, multiple conjunction nodes are the inputs
                                                # try detecting cycles on those nodes to output "lo"

        Q = deque()
        presses = 0
        stop = False
        cycles = {}     # Store cycle values rx_inverter_feeds nodes (cycle of button press before they emit "hi")

        while not stop:
            presses += 1
            Q.append(modules["button"].press())
            
            while Q:
                src, sig, dst = Q.popleft()
                # Check cycles if source is one of the nodes we are looking for
                if src in rx_inverter_feeds and sig == 1:
                    if not src in cycles:
                        cycles[src] = presses
                        # Once we have all cycles, we can stop pressing the button
                        if len(cycles.keys()) == len(rx_inverter_feeds):
                            stop = True
                            break
                # If loop is not stopped, continue processing signals
                for n in dst:
                    if n in modules:
                        out = modules[n].process(src, sig)
                        if out: Q.append(out)
        
        # Finally once loop is exited, we should have all cycle info for feed into pre-RX Conjunction
        # To get total count of presses, we need to calculate LCM of all values
        print(f"Part2: {lcm(*cycles.values())}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
