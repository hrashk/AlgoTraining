def minimumConcat(initial, goal):
   lenG = len(goal)

   if lenG == 0:
      return 1
   elif not set(goal).issubset(set(initial)):
      return -1

   res = 1
   lcs = [[0, 0]] * (lenG + 1)
   col, prev = 1, 0

   row = 1
   pos = 0

   while row <= lenG:
      idx = row

      while idx <= lenG:
         if goal[row - 1] == initial[pos]:
            # print(lcs[idx][col], prev, idx)
            lcs[idx][col] = max(1 + lcs[idx - 1][prev], lcs[idx - 1][col], lcs[idx][prev])
         else:
            lcs[idx][col] = max(lcs[idx - 1][col], lcs[idx][prev])

         idx += 1

      # skip the rows that have reached their limit
      while row <= lenG and lcs[row][col] == row:
         row += 1

      if row > lenG:
         break

      prev, col = col, prev
      pos += 1
      if pos >= len(initial):
         res += 1
         pos = 0


   return res

initial = input()
goal = input()
# from string import ascii_lowercase
# initial = ascii_lowercase[0:3][::-1]
# goal = ascii_lowercase[0:3] * 2
print(minimumConcat(initial, goal))
