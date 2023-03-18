
def fibonacci(n):
   if n == 0:
     return 0
   if n == 1:
     return 1
   return fibonacci(n-1) + fibonacci(n-2)

def fibonacci2(n):
   lst = [0, 1]
   while len(lst) < n + 1:
      lst.append(lst[-1] + lst[-2])
   return lst[-1]


for i in range(1, 101):
   print(i, fibonacci2(i))