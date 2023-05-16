FFXIII-2 clock puzzle solver
===========

Analogue in web version:
http://shauninman.com/utils/ffxiii2/#solution

##
![](screenshot.jpg)

##

Input:
```
#       2
#    4     4
#   1        1
# 2           3
#   5      4
#       3
# clock_items = [2, 4, 1, 3, 4, 3, 5, 2, 1, 4]
clock_items = list(map(int, '2413435214'))
```

Output:
```
Winning results: 9
1.
Simple:
4(4) -> 0(2) -> 8(1) -> 7(2) -> 9(4) -> 5(3) -> 2(1) -> 3(3) -> 6(5) -> 1(4)

Extended:
[2, 4, 1, 3, 4, 3, 5, 2, 1, 4] -> #4 (4)
[2, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #0 (2)
[0, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #8 (1)
[0, 4, 1, 3, 0, 3, 5, 2, 0, 4] -> #7 (2)
[0, 4, 1, 3, 0, 3, 5, 0, 0, 4] -> #9 (4)
[0, 4, 1, 3, 0, 3, 5, 0, 0, 0] -> #5 (3)
[0, 4, 1, 3, 0, 0, 5, 0, 0, 0] -> #2 (1)
[0, 4, 0, 3, 0, 0, 5, 0, 0, 0] -> #3 (3)
[0, 4, 0, 0, 0, 0, 5, 0, 0, 0] -> #6 (5)
[0, 4, 0, 0, 0, 0, 0, 0, 0, 0] -> #1 (4)

2.
Simple:
4(4) -> 0(2) -> 8(1) -> 7(2) -> 9(4) -> 3(3) -> 6(5) -> 1(4) -> 5(3) -> 2(1)

Extended:
[2, 4, 1, 3, 4, 3, 5, 2, 1, 4] -> #4 (4)
[2, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #0 (2)
[0, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #8 (1)
[0, 4, 1, 3, 0, 3, 5, 2, 0, 4] -> #7 (2)
[0, 4, 1, 3, 0, 3, 5, 0, 0, 4] -> #9 (4)
[0, 4, 1, 3, 0, 3, 5, 0, 0, 0] -> #3 (3)
[0, 4, 1, 0, 0, 3, 5, 0, 0, 0] -> #6 (5)
[0, 4, 1, 0, 0, 3, 0, 0, 0, 0] -> #1 (4)
[0, 0, 1, 0, 0, 3, 0, 0, 0, 0] -> #5 (3)
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0] -> #2 (1)

3.
Simple:
4(4) -> 0(2) -> 8(1) -> 9(4) -> 5(3) -> 2(1) -> 3(3) -> 6(5) -> 1(4) -> 7(2)

Extended:
[2, 4, 1, 3, 4, 3, 5, 2, 1, 4] -> #4 (4)
[2, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #0 (2)
[0, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #8 (1)
[0, 4, 1, 3, 0, 3, 5, 2, 0, 4] -> #9 (4)
[0, 4, 1, 3, 0, 3, 5, 2, 0, 0] -> #5 (3)
[0, 4, 1, 3, 0, 0, 5, 2, 0, 0] -> #2 (1)
[0, 4, 0, 3, 0, 0, 5, 2, 0, 0] -> #3 (3)
[0, 4, 0, 0, 0, 0, 5, 2, 0, 0] -> #6 (5)
[0, 4, 0, 0, 0, 0, 0, 2, 0, 0] -> #1 (4)
[0, 0, 0, 0, 0, 0, 0, 2, 0, 0] -> #7 (2)

4.
Simple:
4(4) -> 0(2) -> 8(1) -> 9(4) -> 3(3) -> 6(5) -> 1(4) -> 7(2) -> 5(3) -> 2(1)

Extended:
[2, 4, 1, 3, 4, 3, 5, 2, 1, 4] -> #4 (4)
[2, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #0 (2)
[0, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #8 (1)
[0, 4, 1, 3, 0, 3, 5, 2, 0, 4] -> #9 (4)
[0, 4, 1, 3, 0, 3, 5, 2, 0, 0] -> #3 (3)
[0, 4, 1, 0, 0, 3, 5, 2, 0, 0] -> #6 (5)
[0, 4, 1, 0, 0, 3, 0, 2, 0, 0] -> #1 (4)
[0, 0, 1, 0, 0, 3, 0, 2, 0, 0] -> #7 (2)
[0, 0, 1, 0, 0, 3, 0, 0, 0, 0] -> #5 (3)
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0] -> #2 (1)

5.
Simple:
4(4) -> 0(2) -> 2(1) -> 1(4) -> 7(2) -> 5(3) -> 8(1) -> 9(4) -> 3(3) -> 6(5)

Extended:
[2, 4, 1, 3, 4, 3, 5, 2, 1, 4] -> #4 (4)
[2, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #0 (2)
[0, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #2 (1)
[0, 4, 0, 3, 0, 3, 5, 2, 1, 4] -> #1 (4)
[0, 0, 0, 3, 0, 3, 5, 2, 1, 4] -> #7 (2)
[0, 0, 0, 3, 0, 3, 5, 0, 1, 4] -> #5 (3)
[0, 0, 0, 3, 0, 0, 5, 0, 1, 4] -> #8 (1)
[0, 0, 0, 3, 0, 0, 5, 0, 0, 4] -> #9 (4)
[0, 0, 0, 3, 0, 0, 5, 0, 0, 0] -> #3 (3)
[0, 0, 0, 0, 0, 0, 5, 0, 0, 0] -> #6 (5)

6.
Simple:
4(4) -> 0(2) -> 2(1) -> 1(4) -> 5(3) -> 8(1) -> 7(2) -> 9(4) -> 3(3) -> 6(5)

Extended:
[2, 4, 1, 3, 4, 3, 5, 2, 1, 4] -> #4 (4)
[2, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #0 (2)
[0, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #2 (1)
[0, 4, 0, 3, 0, 3, 5, 2, 1, 4] -> #1 (4)
[0, 0, 0, 3, 0, 3, 5, 2, 1, 4] -> #5 (3)
[0, 0, 0, 3, 0, 0, 5, 2, 1, 4] -> #8 (1)
[0, 0, 0, 3, 0, 0, 5, 2, 0, 4] -> #7 (2)
[0, 0, 0, 3, 0, 0, 5, 0, 0, 4] -> #9 (4)
[0, 0, 0, 3, 0, 0, 5, 0, 0, 0] -> #3 (3)
[0, 0, 0, 0, 0, 0, 5, 0, 0, 0] -> #6 (5)

7.
Simple:
4(4) -> 0(2) -> 2(1) -> 3(3) -> 6(5) -> 1(4) -> 7(2) -> 5(3) -> 8(1) -> 9(4)

Extended:
[2, 4, 1, 3, 4, 3, 5, 2, 1, 4] -> #4 (4)
[2, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #0 (2)
[0, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #2 (1)
[0, 4, 0, 3, 0, 3, 5, 2, 1, 4] -> #3 (3)
[0, 4, 0, 0, 0, 3, 5, 2, 1, 4] -> #6 (5)
[0, 4, 0, 0, 0, 3, 0, 2, 1, 4] -> #1 (4)
[0, 0, 0, 0, 0, 3, 0, 2, 1, 4] -> #7 (2)
[0, 0, 0, 0, 0, 3, 0, 0, 1, 4] -> #5 (3)
[0, 0, 0, 0, 0, 0, 0, 0, 1, 4] -> #8 (1)
[0, 0, 0, 0, 0, 0, 0, 0, 0, 4] -> #9 (4)

8.
Simple:
4(4) -> 0(2) -> 2(1) -> 3(3) -> 6(5) -> 1(4) -> 7(2) -> 9(4) -> 5(3) -> 8(1)

Extended:
[2, 4, 1, 3, 4, 3, 5, 2, 1, 4] -> #4 (4)
[2, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #0 (2)
[0, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #2 (1)
[0, 4, 0, 3, 0, 3, 5, 2, 1, 4] -> #3 (3)
[0, 4, 0, 0, 0, 3, 5, 2, 1, 4] -> #6 (5)
[0, 4, 0, 0, 0, 3, 0, 2, 1, 4] -> #1 (4)
[0, 0, 0, 0, 0, 3, 0, 2, 1, 4] -> #7 (2)
[0, 0, 0, 0, 0, 3, 0, 0, 1, 4] -> #9 (4)
[0, 0, 0, 0, 0, 3, 0, 0, 1, 0] -> #5 (3)
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0] -> #8 (1)

9.
Simple:
4(4) -> 0(2) -> 2(1) -> 3(3) -> 6(5) -> 1(4) -> 5(3) -> 8(1) -> 7(2) -> 9(4)

Extended:
[2, 4, 1, 3, 4, 3, 5, 2, 1, 4] -> #4 (4)
[2, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #0 (2)
[0, 4, 1, 3, 0, 3, 5, 2, 1, 4] -> #2 (1)
[0, 4, 0, 3, 0, 3, 5, 2, 1, 4] -> #3 (3)
[0, 4, 0, 0, 0, 3, 5, 2, 1, 4] -> #6 (5)
[0, 4, 0, 0, 0, 3, 0, 2, 1, 4] -> #1 (4)
[0, 0, 0, 0, 0, 3, 0, 2, 1, 4] -> #5 (3)
[0, 0, 0, 0, 0, 0, 0, 2, 1, 4] -> #8 (1)
[0, 0, 0, 0, 0, 0, 0, 2, 0, 4] -> #7 (2)
[0, 0, 0, 0, 0, 0, 0, 0, 0, 4] -> #9 (4)
```