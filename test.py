test = None

def sub():
    test_list = []
    global test
    test_list.append(1)
    test = test_list

sub()

print(test)
