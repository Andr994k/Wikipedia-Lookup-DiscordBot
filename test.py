yeah = [("result 1", 437280),("result 2", 437232480),("result 3", 4372865430),("result 4", 4371234280),("result 5", 4377645280)]

yeah = [(t[0],) for t in yeah]

result = ''.join(['{}\n'.format(t[0]) for t in yeah])

print(result)