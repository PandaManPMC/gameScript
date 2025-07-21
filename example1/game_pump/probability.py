from decimal import Decimal, getcontext

# 设置高精度，防止幂运算精度丢失
getcontext().prec = 50

# 关卡数和对应的最终通关概率（百分比 → 小数）
data = [
    (24, Decimal("0.04")),        # 4%
    (22, Decimal("0.000435")),    # 0.0435%
    (20, Decimal("0.0000182")),   # 0.00182%
    (14, Decimal("0.0000034")),   # 0.00034%
]

# 计算每关通关概率
results = []
for levels, final_prob in data:
    per_level_prob = final_prob ** (Decimal(1) / Decimal(levels))
    results.append((levels, final_prob, per_level_prob, per_level_prob * 100))

# 打印结果
for levels, final_prob, per_level_prob, percent in results:
    print(f"{levels} 关，最终通关率 {final_prob}：")
    print(f"  每关通关概率（小数）: {per_level_prob}")
    print(f"  每关通关概率（百分比）: {percent}%")
    print()
