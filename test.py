import random
x = 2
y = 10

print("x: ", x)
print("y: ", y)

# print values of circle around x and y
# for idx in range(x-1, x+2):
#     for idy in range(y-1, y+2):
#         print("value: ", idx, idy)

# print values of square around x and y
# for idx in range(x-1, x+2):
#     for idy in range(y-1, y+2):
#         if idx != x:
#             print("value: ", idx, idy)
#         elif idy != y:
#             print("value: ", idx, idy)

# print ("\n")

# print values of square around x and y
# for idx in range(x-2, x+3):
#     for idy in range(y-2, y+3):
#         if idx != x:
#             print("value: ", idx, idy)
#         elif idy != y:
#             print("value: ", idx, idy)

print(random.choice(list(set([x for x in range(0, 700)]) - set(range(160, 220)))))
