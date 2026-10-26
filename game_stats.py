import json
import os

class GameStats():
    """跟踪游戏的统计信息"""
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # 游戏刚启动时处于非活动状态
        self.game_active = False

        # 读取本地最高分
        self.high_score = self.load_high_score()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        """从文件中读取历史最高分"""
        filename = 'high_score.json'
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError):
                return 0 # 如果文件损坏，返回0
        return 0

    def save_high_score(self):
        """将当前最高分保存到文件"""
        filename = 'high_score.json'
        with open(filename, 'w') as f:
            json.dump(self.high_score, f)