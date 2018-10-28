while len(path):
	print(len(path))
	x, y = path[-1]
	# 判断四个方向坐标是否在地图内，如果在地图内，将其加入dir_list1
	for key in dir_dict:
		dx, dy = dir_dict.get(key)
		if 1 <= x+dx <= 80 and 1 <= y+dy <= 50 and self.tiles[x+dx][y+dy].color == tcod.yellow:
			dir_list1.append(dir_dict.get(key))
			dx, dy = sample(dir_list1, 1)[0]
			self.tiles[x+dx][y+dy].color = tcod.red
			path.append((x+dx, y+dy))
		else:
			continue

