# bbt
Bored Battle Theater



pip 安装tcod包，
运行如果引用tcod包提示DLL LOAD FAILED
去 https://support.microsoft.com/en-ca/help/2977003/the-latest-supported-visual-c-downloads

安装x64 版本的 vc_redist.x64.exe 
Visual Studio 2017

## 截止到Part 7总结

### 当前结构
当前项目结构图如下：
```
bbt:
|   death_functions.py        处理死亡信息
|   engine.py                 游戏主程序/引擎
|   entity.py                 内涵一个通用类，敌人/玩家的方法都在其中，玩家移动，怪物移动（a-star寻路算法）
|   fov_funcitons.py          处理field-of-view，就是一个光照系统
|   game_messages.py          处理模块间通信信息，封装各类信息给主程序/引擎
|   game_states.py            处理游戏状态
|   input_handlers.py         处理游戏内按键控制
|   LICENSE
|   README.md
|   render_functions.py       游戏内各种实体（墙，物品，怪物，玩家...)的渲染
|
+---components
|   |   ai.py                 包括一个BasicMonster类，可以进行攻击
|   |   fighter.py            战斗类的小插件，给player装配上Fighter就具备攻击行为
|   |   __init__.py             
|   
+---fonts
|       arial10x10.png        游戏字体渲染
|
+---map_objects
|   |   game_map.py           GameMap，可以生成地图，生成H和V向通道，放置怪物
|   |   rectangle.py          Rect，生成矩形，进而在GameMap里生成Room
|   |   tile.py               Tile，生成地图块，有block和sight_block属性，在FOV里处理地图的光照
|   |   __init__.py
|
```

### Part1
在part1中主要讲了怎么创建一个console，然后在console中显示一个“@”并通过按键操纵@走动。

```python
tcod.console_set_custom_font('fontfile', flags)
tcod.console_init_root(width,height,'title',False)
tcod.console_put_char(0,1,1,"@",tcod.BKGND_NONE)
```

### 怎么做一个roguelike游戏

15步做一个roguelike游戏

1. 下决心写游戏
2. Hello World
3. It's a Boy
4. 地图
5. 保存和读取
6. It's Alive(其实就是做AI和战斗系统)
7. 交互
8. 数据文件（数据文件这一步至今没看到教程）
9. 物品
10. 魔法
11. 简单游戏
12. 关卡
13. 经验值
14. 村民（NPC）
15. 随心所以加入任何想加入的coooooool的特性