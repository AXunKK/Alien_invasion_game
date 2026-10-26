# generate_sounds.py
import wave
import struct
import math
import random
import os

# 确保 sounds 文件夹存在
if not os.path.exists('sounds'):
    os.makedirs('sounds')

def save_wav(filename, samples, sample_rate=44100):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        for s in samples:
            f.writeframes(struct.pack('h', int(max(-1, min(1, s)) * 32767)))

# 1. 生成激光音效 (Laser) - 频率从高到低
laser_samples = []
for i in range(10000):
    t = float(i) / 44100
    freq = 1500 - (1200 * (i / 10000)) # 频率下降
    val = math.sin(2 * math.pi * freq * t)
    # 添加衰减
    envelope = 1.0 - (i / 10000)
    laser_samples.append(val * envelope * 0.5)
save_wav('sounds/laser.wav', laser_samples)

# 2. 生成爆炸音效 (Explosion) - 随机白噪声
explosion_samples = []
for i in range(20000):
    val = random.uniform(-1, 1)
    # 衰减包络
    envelope = max(0, 1.0 - (i / 20000) * 1.5)
    explosion_samples.append(val * envelope * 0.8)
save_wav('sounds/explosion.wav', explosion_samples)

# 3. 生成飞船被撞音效 (Hit) - 低频嗡嗡声
hit_samples = []
for i in range(30000):
    t = float(i) / 44100
    freq = 150 - (100 * (i / 30000))
    val = math.sin(2 * math.pi * freq * t) + 0.5 * math.sin(2 * math.pi * (freq-20) * t)
    envelope = 1.0 - (i / 30000)
    hit_samples.append(val * envelope * 0.7)
save_wav('sounds/hit.wav', hit_samples)

print("音效生成完毕！请查看 sounds 文件夹。")