grid_size = 15

def generate_r_craft_grid(grid_size=grid_size):
    if grid_size % 2 == 0:
        raise ValueError("Er is geen middelpunt als je gridsize een even getal is...")
        
    grid = []
    for g in range(grid_size):
        line = []
        for h in range(grid_size):
            line.append([])
        grid.append(line)
    xm = ym = int((grid_size - 1) / 2)
    print(xm, ym)
    grid = fill_grid((xm, ym), (xm, ym), grid, None, True)
    return grid


def fill_grid(center_point, start_point, grid, direction, on_main_branch):
    if center_point == start_point:
        xm = center_point[0]
        ym = center_point[1]
        directions = ["up", "rup", "rdown", "down", "ldown", "lup"]
        for indx, point in enumerate([(xm, ym-1), (xm+1, ym-1+xm%2), (xm+1, ym+xm%2), (xm, ym+1), (xm-1, ym+xm%2), (xm-1, ym-1+xm%2)]):
            grid[ym][xm].append(point)
            fill_grid(center_point, point, grid, directions[indx], True)
    
    else:
        sx = start_point[0]
        sy = start_point[1]
        print(sx, sy)
        match direction:
            case 'up':
                if sy > 0:
                    grid[sy][sx].append((sx, sy - 1))
                    fill_grid(center_point, (sx, sy-1), grid, direction, on_main_branch)
                
                if on_main_branch:
                    if sx + 1 < grid_size and sy - 1 + sx % 2 >= 0:
                        grid[sy][sx].append((sx+1, sy - 1 + sx % 2))
                        fill_grid(center_point, (sx+ 1, sy - 1 + sx % 2), grid, 'rup', False)
                
            case 'rup':
                if sy + sx % 2 > 0 and sx + 1 < grid_size:
                    grid[sy][sx].append((sx + 1, sy - 1 + sx % 2))
                    fill_grid(center_point, (sx + 1, sy - 1 + sx % 2), grid, direction, on_main_branch)
                
                if on_main_branch:
                    if sx + 1 < grid_size and sy + sx % 2 >= 0:
                        grid[sy][sx].append((sx + 1, sy + sx % 2))
                        fill_grid(center_point, (sx + 1, sy + sx % 2), grid, 'rdown', False)
                
            case 'rdown':
                if sy - 1 + sx % 2 > 0 and sx + 1 < grid_size:
                    grid[sy][sx].append((sx + 1, sy + sx % 2))
                    fill_grid(center_point, (sx + 1, sy + sx % 2), grid, direction, on_main_branch)
                
                if on_main_branch:
                    if sx < grid_size and sy <= grid_size:
                        grid[sy][sx].append((sx, sy + 1))
                        fill_grid(center_point, (sx, sy + 1), grid, 'down', False)

            case 'down':
                if sy + 1 < grid_size:
                    grid[sy][sx].append((sx, sy + 1))
                    fill_grid(center_point, (sx, sy + 1), grid, direction, on_main_branch)
                
                if on_main_branch:
                    if sx + 1 < grid_size and sy + sx % 2 < grid_size:
                        grid[sy][sx].append((sx - 1, sy + sx % 2))
                        fill_grid(center_point, (sx - 1, sy + sx % 2), grid, 'ldown', False)
                
               
            case 'ldown':
                if sy + sx % 2 < grid_size and sx > 0:
                    grid[sy][sx].append((sx - 1, sy + sx % 2))
                    fill_grid(center_point, (sx - 1, sy + sx % 2), grid, direction, on_main_branch)
                
                if on_main_branch:
                    if sx > 0 and sy <= grid_size:
                        grid[sy][sx].append((sx - 1, sy - 1 + sx % 2))
                        fill_grid(center_point, (sx - 1, sy - 1 + sx % 2), grid, 'lup', False)
                
            case 'lup':
                if sy - 1 + sx % 2 > 0 and sx > 0:
                    grid[sy][sx].append((sx - 1, sy - 1 + sx % 2))
                    fill_grid(center_point, (sx - 1, sy - 1 + sx % 2), grid, direction, on_main_branch)
                
                if on_main_branch:
                    if sx + 1 < grid_size and sy + sx % 2 >= 0:
                        grid[sy][sx].append((sx, sy - 1))
                        fill_grid(center_point, (sx, sy - 1), grid, 'up', False)
             



    return grid


with open("Data/r_crafter_grid.txt", "w") as f:
    f.write(str(generate_r_craft_grid()))


boolean_grid = []
for row in range(grid_size):
    row_line = []
    for index in range(grid_size):
        if row == int(grid_size / 2) and index == int(grid_size / 2):
            row_line.append(True)
        else:
            row_line.append(False)
            
    boolean_grid.append(row_line[:])

for world in ["another_world", "research_world", "research_world_copy", "~menu_world"]:
    with open("Data/Saves/{}/research_grid.txt".format(world), "w") as f:
        f.write(str(boolean_grid))
