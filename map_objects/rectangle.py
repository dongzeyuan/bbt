class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.w = w
        self.h = h
        self.c_x = (self.x1 + self.x2) // 2
        self.c_y = (self.y1 + self.y2) // 2

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one.
        # 这里修改了重叠判定算法
        return ((abs(self.c_x - other.c_x) < (self.w + other.w) // 2 + 4) and
                (abs(self.c_y - other.c_y) < (self.h + other.h) // 2 + 4))
