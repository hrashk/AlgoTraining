# from pprint import pprint

class Solution(object):
  def numOffices(self, grid):
    """
    :type grid: List[List[str]]
    :rtype: int
    """
    # your code here
    # pprint(grid)
    visited = [[False] * len(grid[0]) for i in range(len(grid))]
    res = 0

    for row in range(len(grid)):
      for col in range(len(grid[0])):
        if grid[row][col] == '1' and not visited[row][col]:
          res += 1
          self.bfs(grid, visited, row, col)

    return res
  
  def bfs(self, grid, visited, row, col):
    visited[row][col] = True
    frontier = [(row, col)]

    while len(frontier) > 0:
      # print(frontier)
      r, c = frontier.pop()
      for dr, dc in [(r-1, c), (r+1, c), (r, c-1), (r, c + 1)]:
        # print((dr, dc), grid[dr][dc], visited[dr][dc])
        if grid[dr][dc] == '1' and not visited[dr][dc]:
          visited[dr][dc] = True
          frontier.append((dr, dc))


def get_matrix():
  row = int(input())
  col = int(input())
  grid = [ ['0'] * (col + 2) ]

  for i in range(row):
    line = input()
    grid.append(['0'] + list(line)[0:col] + ['0'])
  
  grid.append(['0'] * (col + 2))

  return grid

        
if __name__ == "__main__":
  sol = Solution()
  matrix = get_matrix()
  offices = sol.numOffices(matrix)
  print(offices)
