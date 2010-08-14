





class MyException(Exception): pass

# whatever you do, do not move this function, it must start on line 10
def fail_horribly(request):
    raise MyException('XXX')
