import time

start = time.time()
print(start)

time.sleep(10)
end = time.time()

diff = end - start
print(diff)

timer = 10
if timer < diff:
    print("YES")
else:
    print("NO")
