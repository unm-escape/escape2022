# functions
def ex1(a,b):
    c = a + b 
    d = a - c*b
    return (c,d)

def ex2(a,b):
    c = a * b 
    d = a + c - b
    return (c,d)

def ex3(a,b):
    c = a - b 
    d = a - c + b
    return (c,d)

def example_four(a,b):
    c = a + b 
    d = a + c + b
    return (c,d)


# main script
if __name__ == '__main__':
    
    # do example 1
    r,s = ex1(1,4)
    print (r,s)
    
    # do example 2
    r,s = ex2(2,4)
    print (r,s)
    
    # do example 3
    r,s = ex3(1,2)
    print (r,s)
    
    # do example 4
    r,s = example_four(1,1)
    print (r,s)