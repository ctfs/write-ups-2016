class QSet:
    def __init__(self, input=None):
        self.__repr__=self.__str__
        self.qset = {}
        if input!=None:
            for item in input:
                self.add_item(item)
    def add_item(self, item, amt=1):
        if item in self.qset:
            self.qset[item]+=amt
            if self.qset[item]==0:
                del self.qset[item]
        else:
            self.qset[item]=amt
    def add_qset(self, aqset):
        for item in aqset.qset:
            self.add_item(item, aqset.qset[item])
    def remove_qset(self, aqset):
        for item in aqset.qset:
            self.add_item(item, -aqset.qset[item])
    def contains_qset(self, aqset):
        for item in aqset.qset:
            if item in self.qset:
                if self.qset[item]<aqset.qset[item]:
                    return False
            else:
                return False
        return True
    def is_empty(self):
        return len(self.qset)==0
    def __str__(self):
        return str(self.qset)

def parse(x):
    steps = x.strip()
    steps = steps.split(',')
    reps = []
    for step in steps:
        rep = [y.strip() for y in step.split('/')]
        if len(rep)!=2:
            raise Exception("Failed to parse input!")
        reps.append(rep)
    return [[QSet([] if x.split(' ')==[''] else x.split(' ')) for x in vals] for vals in reps]

def interpret_step(program, qset):
    for process in program:
        if qset.contains_qset(process[1]):
            qset.remove_qset(process[1])
            qset.add_qset(process[0])
            return False
    return True

def interpret(program, input, maxsteps=100000):
    try:
        program = parse(program)
        qset = QSet()
        for x in range(len(input)):
            if type(input[x]) is int or type(input[x]) is long:
                qset.add_item('i%i'%x, input[x])
            else:
                raise Exception("Invalid input type")
        step = 0
        while True:
            if step==maxsteps:
                raise Exception("Too many execution steps!")
            ret = interpret_step(program, qset)
            if ret:
                break
            step += 1
        success = True
        outputs = {}
        for key in qset.qset:
            if len(key)>1:
                if key[0]=="o":
                    idx = key[1:]
                    idx = int(idx)
                    outputs[idx] = qset.qset[key]
                else:
                    success = False
            else:
                success = False
        if success:
            outputs_arr = []
            for x in range(len(outputs)):
                if x in outputs:
                    outputs_arr.append(outputs[x])
                else:
                    raise Exception("Invalid output!")
            return outputs_arr
        else:
            raise Exception("Invalid output!")
    except Exception as e:
        return ",".join(e.args)