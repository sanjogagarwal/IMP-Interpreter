import re
import sys
var={}
operators = ['+', '-', '*', '/']
code = ""

class CompoundStatement:
    def __init__(self, code_base):
        self.string = code_base
        self.list = code_base.split('\n')
        #   self.list.remove(' ')
        #print(self.list)
        while(1):
            try:
                self.list.remove('')
            except:
                break;
        #print(self.list)    
        #self.list = self.list[0].split(';')
        k=0
        #print('k')
        #print(len(self.list))
        
        #print(len(self.list))
        while(k<len(self.list)):

            parse = LineParser(self.list[k].split(';')[0], k, code_base)
            k += parse.counter
            #print(k)

class LineParser:
    def __init__(self, codesegment, k,code_base):
        self.line = codesegment
        self.code_base = code_base
        self.line = self.line.strip()
        self.counter=0
        self.k = k
        self.check()

    def check(self):
        if(self.line.count(':=')>0):
            self.assignment()
            self.counter+=1
        if(self.line.count('print')>0):
            self.print()
            self.counter+=1
        if(self.line.count('if')>0):
            self.buildif()
        if(self.line.count('while')>0):
            self.buildloop()

    def assignment(self):
        self.line = self.line.split(':=')
        newtemp = self.line[0].strip()
        if(newtemp in var):
            var[newtemp] = Expression.eval_exp(self.line[1].strip())
        else:
            newdict = {newtemp:Expression.eval_exp(self.line[1].strip())}
            var.update(newdict)

    def print(self):
        self.line = self.line.split('print')
        newtemp = self.line[1].strip()
        flag=0
        for op in operators:
            if(newtemp.count(op)>0):
                flag=1
        if(flag==0):
            ktemp = checkVar.find(newtemp)
            if(ktemp=='Error!!'):
                print(newtemp)
            else:
                print(ktemp)

    def buildif(self):

        self.line = self.line.split('if')
        newtemp = self.line[1].strip()
        self.line = newtemp.split('then')
        newtemp = self.line[0].strip()
        #print(newtemp)
        #print(code)
        codetemp = self.code_base.split('\n')
        #print(codetemp)
        #print(self.k)
        block = '\n'.join(codetemp[self.k:])
        #print(type(block))
        if_tuple = [(m.start(0), m.end(0)) for m in re.finditer('if', block)]
        #print(if_tuple)
        fi_tuple = [(m.start(0), m.end(0)) for m in re.finditer('fi', block)]
        #print(fi_tuple)
        first_fi = fi_tuple[0][0]
        counter = 0
        for ele in if_tuple:
            counter += 1
            if (ele[0] > first_fi):
                counter-=1
                break
        #print(counter)        
        last_fi = fi_tuple[counter - 1][0]

        n_tuple = [(m.start(0), m.end(0)) for m in re.finditer('\n', block[:last_fi])]
        #print(len(n_tuple))
        else_tuple = [(m.start(0), m.end(0)) for m in re.finditer('else', block[:last_fi])]
        increment_line = len(n_tuple) + 1
        #print(self.counter)
        self.counter += increment_line
        #print(self.counter)
        #print(newtemp)
        if(ConditionalExpression.eval_exp(newtemp)):
            lowerlimit = else_tuple[counter-1][0]-1
            #print(block[:lowerlimit])
            upperlimit = block[:lowerlimit].split('\n')
            #print('\n'.join(upperlimit[1:]))
            upperlimit = '\n'.join(upperlimit[1:])
            #print(upperlimit)
            CompoundStatement(upperlimit)
        else:
            lowerlimit = fi_tuple[counter-1][0]-1
            upperlimit = block[else_tuple[counter-1][1]:lowerlimit].split('\n')
            upperlimit = '\n'.join(upperlimit[1:])
            CompoundStatement(upperlimit)


    def buildloop(self):
        self.line = self.line.split('while')
        newtemp = self.line[1].strip()
        self.line = newtemp.split('do')
        newtemp = self.line[0].strip()
        #print(newtemp)
        codetemp = self.code_base.split('\n')
        #print(codetemp)
        block = '\n'.join(codetemp[self.k:])
        #print(block)
        while_tuple = [(m.start(0), m.end(0)) for m in re.finditer('while', block)]
        #print(while_tuple)
        done_tuple = [(m.start(0), m.end(0)) for m in re.finditer('done', block)]
        #print(done_tuple)
        first_done = done_tuple[0][0]
        counter = 0
        for ele in while_tuple:
            counter += 1
            if (ele[0] > first_done):
                counter-=1
                break
        #print(counter)        
        last_done = done_tuple[counter - 1][0]
        n_tuple = [(m.start(0), m.end(0)) for m in re.finditer('\n', block[:last_done])]
        increment_line = len(n_tuple) + 1
        self.counter += increment_line
        while(ConditionalExpression.eval_exp(newtemp)):
            lowerlimit = last_done -1
            upperlimit = block[:lowerlimit].split('\n')
            upperlimit = '\n'.join(upperlimit[1:])
            CompoundStatement(upperlimit)


class Expression:
    def eval_exp(codeline):
        if(codeline.count('-')>0):
            return SubstExp.eval_exp(codeline)
        elif(codeline.count('+')>0):
            return AddExp.eval_exp(codeline)
        elif(codeline.count('*')>0):
            return MultExp.eval_exp(codeline)
        elif(codeline.count('/')>0):
            return DivExp.eval_exp(codeline)
        else:
            decide = checkVar.find(codeline)
            if(decide == 'Error!!'):
                print('Error in assignment operation(s)')
                exit()
            else:
                return decide

class ConditionalExpression:
    def eval_exp(codeline):
        if(codeline.count('>')):
            return GreaterExp.eval_exp(codeline)
        elif(codeline.count('<')):
            return LesserExp.eval_exp(codeline)
        elif(codeline.count('==')):
            return EqualExp.eval_exp(codeline)
        elif(codeline.count('!=')):
            return NotEqualExp.eval_exp(codeline)
        else:
            if(codeline=='1'):
                return 1
            decide = checkVar.find(codeline)
            if(decide=='Error!!'):
                print('Error in conditional expression(s)')
                exit()
            else:
                return codeline

class GreaterExp:
    def eval_exp(codeline):
        codeline = codeline.split('>')
        leftexp = Expression.eval_exp(codeline[0].strip())
        rightexp = Expression.eval_exp(codeline[1].strip())
        if(leftexp>rightexp):
            return 1
        else:
            return 0

class LesserExp:
    def eval_exp(codeline):
        codeline = codeline.split('<')
        leftexp = Expression.eval_exp(codeline[0].strip())
        #print(leftexp)
        rightexp = Expression.eval_exp(codeline[1].strip())
        #print(rightexp)
        if(leftexp<rightexp):
            return 1
        else:
            return 0

class EqualExp:
    def eval_exp(codeline):
        codeline = codeline.split('==')
        leftexp = Expression.eval_exp(codeline[0].strip())
        rightexp = Expression.eval_exp(codeline[1].strip())
        if(leftexp==rightexp):
            return 1
        else:
            return 0

class NotEqualExp:
    def eval_exp(codeline):
        codeline = codeline.split('!=')
        leftexp = Expression.eval_exp(codeline[0].strip())
        rightexp = Expression.eval_exp(codeline[1].strip())
        if(leftexp!=rightexp):
            return 1
        else:
            return 0


class SubstExp:
    def eval_exp(codeline):
        codeline = codeline.split('-')
        leftexp = Expression.eval_exp(codeline[0].strip())
        rightexp = Expression.eval_exp(codeline[1].strip())
        return leftexp - rightexp

class AddExp:
    def eval_exp(codeline):
        codeline = codeline.split('+')
        leftexp = Expression.eval_exp(codeline[0].strip())
        rightexp = Expression.eval_exp(codeline[1].strip())
        return rightexp + leftexp

class MultExp:
    def eval_exp(codeline):
        codeline = codeline.split('*')
        leftexp = Expression.eval_exp(codeline[0].strip())
        rightexp = Expression.eval_exp(codeline[1].strip())
        return rightexp*leftexp

class DivExp:
    def eval_exp(codeline):
        codeline = codeline.split('/')
        leftexp = Expression.eval_exp(codeline[0].strip())
        rightexp = Expression.eval_exp(codeline[1].strip())
        return leftexp/rightexp


class checkVar:
    def find(codeline):
        if(codeline.isdigit()):
            return int(codeline)
        elif(codeline in var):
            return int(var[codeline])
        else:
            return 'Error!!'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    text = open(filename).read()
    code = text
    #print(text.split('\n')[0].split(';')[0])
    z = CompoundStatement(text)
               