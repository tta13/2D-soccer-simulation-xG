
class Parser:
    def __init__(self, rcg_path):
        self.rcg_path = rcg_path
        self.set_data_rcg()
        self.set_teams_name()
        self.right_team
        self.left_team

    def set_data_rcg(self):
        try:
            f = open(self.rcg_path, 'r')
        except:
            print("RCG file does not exist")
            exit(1)
        data_rcg = []

        def parse(expr):
            def _helper(iter):
                items = []
                for item in iter:
                    if item == '(':
                        result, closeparen = _helper(iter)
                        if not closeparen:
                            return [], False
                        items.append(result)
                    elif item == ')':
                        return items, True
                    else:
                        items.append(item)
                return items, False
            return _helper(iter(expr))[0]

        def cleaner(lis):

            def isfloat(value):
                try:
                    float(value)
                    return True
                except ValueError:
                    return False
            arr = []
            string = ''
            for i in range(len(lis)):
                if type(lis[i]) is list:
                    if string != '':
                        if string.isdigit():
                            arr += [int(string)]
                        elif isfloat(string):
                            arr += [float(string)]
                        else:
                            arr += [string]
                    string = ''
                    arr += [cleaner(lis[i])]
                elif type(lis[i]) is str:
                    if lis[i] == ' ':
                        if string != '':
                            if string.isdigit():
                                arr += [int(string)]
                            elif isfloat(string):
                                arr += [float(string)]
                            else:
                                arr += [string]
                        string = ''
                    else:
                        string += lis[i]
            if string != '':
                if string.isdigit():
                    arr += [int(string)]
                elif isfloat(string):
                    arr += [float(string)]
                else:
                    arr += [string]
            return arr
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", '')
        for line in lines:
            p = parse(line)
            if p != []:
                data_rcg += [cleaner(p)]
        f.close()
        self.data_rcg = data_rcg

    def get_data_rcg(self):
        return self.data_rcg

    def set_teams_name(self):
        for cycle in self.data_rcg:
            if cycle[0][0] == 'team':
                self.left_team = cycle[0][2]
                self.right_team = cycle[0][3]

                return
