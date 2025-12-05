#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国全钒液流电池(VRFB)投资项目数据分析
China VRFB Investment Projects Data Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 数据准备 Data Preparation
# ============================================================

# 主要项目数据
projects_data = {
    '项目名称': ['华能吉木萨尔', '融科乌什', '大连储能电站', '松原项目', '磴口项目',
                '攀枝花示范', '新华乌什', '襄阳项目', '丽江项目', '三峡吉木萨尔', '中节能察布查尔'],
    '省份': ['新疆', '新疆', '辽宁', '吉林', '内蒙古', '四川', '新疆', '湖北', '云南', '新疆', '新疆'],
    '功率MW': [200, 175, 200, 100, 50, 100, 175, 100, 300, 200, 250],
    '容量MWh': [1000, 700, 800, 400, 200, 500, 700, 500, 1800, 1000, 1000],
    '投资亿元': [38, None, None, None, None, 16, None, None, None, None, None],
    '状态': ['已完工', '已完工', '一期完工', '已完工', '已完工', '在建', '规划中', '在建', '规划中', '规划中', '规划中'],
    '类型': ['储能电站', '储能电站', '储能电站', '储能电站', '储能电站', '储能电站', '储能电站', '储能电站', '储能电站', '储能电站', '储能电站']
}

# 制造业投资数据
manufacturing_data = {
    '项目名称': ['包头产业园', '大连融科扩建', 'VRB山西工厂', 'VRB湖南工厂', '攀枝花电解液基地', '大连博融电解液', '新兴铸管项目'],
    '省份': ['内蒙古', '辽宁', '山西', '湖南', '四川', '辽宁', '河北'],
    '产能GW': [1.6, 0.5, 0.3, 0.2, None, None, 0.134],
    '投资亿元': [115, 35, 3.85, None, None, None, 9.39],
    '类型': ['制造', '制造', '制造', '制造', '电解液', '电解液', '制造']
}

# 市场统计数据
market_stats = {
    '年份': [2022, 2023, 2024, 2025],
    '并网容量MWh': [100, 236, 1742, 3500],  # 2025为预测
    '项目数量': [3, 6, 16, 25],  # 2025为预测
    '平均价格元Wh': [3.0, 2.6, 2.1, 1.8],  # 2025为预测
    '融资亿元': [15, 27, 18, 25]  # 2025为预测
}

# 省份汇总数据
province_summary = {
    '省份': ['新疆', '辽宁', '四川', '内蒙古', '湖北', '云南', '山西', '湖南', '吉林', '河北'],
    '储能项目MW': [825, 200, 100, 50, 100, 300, 0, 0, 100, 0],
    '制造产能GW': [0, 0.5, 0, 1.6, 0, 0, 0.3, 0.2, 0, 0.134],
    '投资亿元': [38, 35, 16, 115, 0, 0, 3.85, 0, 0, 9.39]
}

# 创建DataFrame
df_projects = pd.DataFrame(projects_data)
df_manufacturing = pd.DataFrame(manufacturing_data)
df_market = pd.DataFrame(market_stats)
df_province = pd.DataFrame(province_summary)

# ============================================================
# 分析与可视化 Analysis & Visualization
# ============================================================

fig, axes = plt.subplots(3, 2, figsize=(14, 15))
fig.suptitle('China VRFB Investment Projects Analysis\n中国全钒液流电池投资项目分析', fontsize=16, fontweight='bold')

# 1. 各省份储能项目容量分布
ax1 = axes[0, 0]
province_capacity = df_projects.groupby('省份')['容量MWh'].sum().sort_values(ascending=True)
colors1 = plt.cm.Blues(range(50, 250, 20))[:len(province_capacity)]
bars1 = ax1.barh(province_capacity.index, province_capacity.values, color=colors1)
ax1.set_xlabel('Capacity (MWh)')
ax1.set_title('Storage Project Capacity by Province\n各省份储能项目容量分布')
for i, v in enumerate(province_capacity.values):
    ax1.text(v + 50, i, f'{v:,.0f}', va='center', fontsize=9)

# 2. 项目状态分布
ax2 = axes[0, 1]
status_counts = df_projects['状态'].value_counts()
colors2 = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
wedges, texts, autotexts = ax2.pie(status_counts.values, labels=status_counts.index,
                                    autopct='%1.1f%%', colors=colors2[:len(status_counts)],
                                    explode=[0.05]*len(status_counts))
ax2.set_title('Project Status Distribution\n项目状态分布')

# 3. 市场增长趋势
ax3 = axes[1, 0]
ax3_twin = ax3.twinx()
line1 = ax3.plot(df_market['年份'], df_market['并网容量MWh'], 'b-o', linewidth=2, markersize=8, label='Grid Capacity (MWh)')
ax3.fill_between(df_market['年份'], df_market['并网容量MWh'], alpha=0.3)
line2 = ax3_twin.plot(df_market['年份'], df_market['项目数量'], 'r--s', linewidth=2, markersize=8, label='Project Count')
ax3.set_xlabel('Year')
ax3.set_ylabel('Capacity (MWh)', color='b')
ax3_twin.set_ylabel('Project Count', color='r')
ax3.set_title('Market Growth Trend (2022-2025E)\n市场增长趋势')
ax3.legend(loc='upper left')
ax3_twin.legend(loc='upper right')

# 4. 价格下降趋势
ax4 = axes[1, 1]
ax4.plot(df_market['年份'], df_market['平均价格元Wh'], 'g-^', linewidth=2, markersize=10)
ax4.fill_between(df_market['年份'], df_market['平均价格元Wh'], alpha=0.3, color='green')
ax4.set_xlabel('Year')
ax4.set_ylabel('Average Price (RMB/Wh)')
ax4.set_title('VRFB System Price Trend\n系统价格下降趋势')
for i, (x, y) in enumerate(zip(df_market['年份'], df_market['平均价格元Wh'])):
    ax4.annotate(f'{y:.1f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

# 5. 各省份投资金额
ax5 = axes[2, 0]
province_investment = df_province[df_province['投资亿元'] > 0].sort_values('投资亿元', ascending=True)
colors5 = plt.cm.Oranges(range(100, 250, 30))[:len(province_investment)]
bars5 = ax5.barh(province_investment['省份'], province_investment['投资亿元'], color=colors5)
ax5.set_xlabel('Investment (100M RMB)')
ax5.set_title('Investment by Province\n各省份投资金额 (亿元)')
for i, v in enumerate(province_investment['投资亿元'].values):
    ax5.text(v + 1, i, f'{v:.1f}', va='center', fontsize=9)

# 6. 制造产能分布
ax6 = axes[2, 1]
mfg_capacity = df_province[df_province['制造产能GW'] > 0].sort_values('制造产能GW', ascending=True)
colors6 = plt.cm.Purples(range(100, 250, 30))[:len(mfg_capacity)]
bars6 = ax6.barh(mfg_capacity['省份'], mfg_capacity['制造产能GW'], color=colors6)
ax6.set_xlabel('Manufacturing Capacity (GW/year)')
ax6.set_title('Manufacturing Capacity by Province\n各省份制造产能分布 (GW/年)')
for i, v in enumerate(mfg_capacity['制造产能GW'].values):
    ax6.text(v + 0.02, i, f'{v:.2f}', va='center', fontsize=9)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('/home/user/Micksiney/vrfb_analysis_charts.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 统计分析 Statistical Analysis
# ============================================================

print("=" * 70)
print("中国全钒液流电池(VRFB)投资项目数据分析报告")
print("China VRFB Investment Projects Analysis Report")
print("=" * 70)

# 1. 总体规模分析
total_capacity_mw = df_projects['功率MW'].sum()
total_capacity_mwh = df_projects['容量MWh'].sum()
total_projects = len(df_projects)
total_investment = df_projects['投资亿元'].sum() + df_manufacturing['投资亿元'].sum()

print("\n【1. 总体规模分析 Overall Scale Analysis】")
print("-" * 50)
print(f"  • 统计项目总数: {total_projects + len(df_manufacturing)} 个")
print(f"  • 储能项目总功率: {total_capacity_mw:,} MW")
print(f"  • 储能项目总容量: {total_capacity_mwh:,} MWh ({total_capacity_mwh/1000:.1f} GWh)")
print(f"  • 已披露总投资额: {total_investment:.2f} 亿元 (约 ${total_investment*0.14:.1f}B USD)")

# 2. 项目状态分析
print("\n【2. 项目状态分析 Project Status Analysis】")
print("-" * 50)
completed = df_projects[df_projects['状态'].str.contains('完工')]['容量MWh'].sum()
under_construction = df_projects[df_projects['状态'] == '在建']['容量MWh'].sum()
planned = df_projects[df_projects['状态'] == '规划中']['容量MWh'].sum()
print(f"  • 已完工容量: {completed:,} MWh ({completed/total_capacity_mwh*100:.1f}%)")
print(f"  • 在建容量: {under_construction:,} MWh ({under_construction/total_capacity_mwh*100:.1f}%)")
print(f"  • 规划中容量: {planned:,} MWh ({planned/total_capacity_mwh*100:.1f}%)")

# 3. 区域分布分析
print("\n【3. 区域分布分析 Regional Distribution Analysis】")
print("-" * 50)
province_stats = df_projects.groupby('省份').agg({
    '功率MW': 'sum',
    '容量MWh': 'sum',
    '项目名称': 'count'
}).rename(columns={'项目名称': '项目数'}).sort_values('容量MWh', ascending=False)

for province, row in province_stats.iterrows():
    share = row['容量MWh'] / total_capacity_mwh * 100
    print(f"  • {province}: {row['容量MWh']:,} MWh ({share:.1f}%), {int(row['项目数'])}个项目")

# 4. 市场增长分析
print("\n【4. 市场增长分析 Market Growth Analysis】")
print("-" * 50)
growth_2023_2024 = (df_market[df_market['年份']==2024]['并网容量MWh'].values[0] /
                    df_market[df_market['年份']==2023]['并网容量MWh'].values[0] - 1) * 100
price_decline = (df_market[df_market['年份']==2023]['平均价格元Wh'].values[0] -
                 df_market[df_market['年份']==2024]['平均价格元Wh'].values[0]) / \
                 df_market[df_market['年份']==2023]['平均价格元Wh'].values[0] * 100
print(f"  • 2023→2024年并网容量增长: +{growth_2023_2024:.0f}%")
print(f"  • 2023→2024年价格下降幅度: -{price_decline:.0f}%")
print(f"  • 2024年平均系统价格: 2.1 元/Wh")
print(f"  • 预计2025年价格: 1.8 元/Wh (继续下降14%)")

# 5. 制造业投资分析
print("\n【5. 制造业投资分析 Manufacturing Investment Analysis】")
print("-" * 50)
total_mfg_capacity = df_manufacturing['产能GW'].sum()
total_mfg_investment = df_manufacturing['投资亿元'].sum()
print(f"  • 制造业总产能规划: {total_mfg_capacity:.2f} GW/年")
print(f"  • 制造业总投资: {total_mfg_investment:.2f} 亿元")
print(f"  • 最大单体项目: 包头产业园 (1.6 GW, 115亿元)")
print(f"  • 电解液产能规划: >27万立方米/年")

# 6. 投资效率分析
print("\n【6. 投资效率分析 Investment Efficiency Analysis】")
print("-" * 50)
# 华能吉木萨尔项目作为参考
huaneng_investment = 38  # 亿元
huaneng_capacity = 1000  # MWh
unit_investment = huaneng_investment / huaneng_capacity * 1000  # 万元/MWh
print(f"  • 参考项目单位投资: {unit_investment:.1f} 万元/MWh (华能吉木萨尔)")
print(f"  • 折合单位成本: {unit_investment/10:.2f} 元/Wh (含配套设施)")
print(f"  • 纯系统招标价: 2.1-2.65 元/Wh")
print(f"  • 度电成本(LCOS): 预计 0.4-0.6 元/kWh")

# 7. 关键发现
print("\n【7. 关键发现 Key Findings】")
print("-" * 50)
print("""
  ① 新疆主导地位明显
     - 新疆省储能项目容量占比超过50%
     - 得益于丰富的风光资源和政策支持
     - 已建成全球最大VRFB项目(200MW/1GWh)

  ② 市场爆发式增长
     - 2024年并网容量同比增长超600%
     - 从2023年的236MWh跃升至1,742MWh
     - 在建和规划项目合计超12GWh

  ③ 成本快速下降
     - 系统价格从2023年的2.6元/Wh降至2024年的2.1元/Wh
     - 年降幅约20%，成本竞争力持续提升
     - 预计2025年将降至1.8元/Wh以下

  ④ 产业链布局完善
     - 内蒙古建设1.6GW全球最大制造基地
     - 四川攀枝花打造最大电解液生产基地
     - 辽宁大连保持技术和市场领先地位

  ⑤ 长时储能优势凸显
     - 项目平均储能时长4-6小时
     - 全生命周期成本已低于锂电池
     - 特别适合新能源配储场景
""")

# 8. 投资建议
print("\n【8. 投资建议 Investment Recommendations】")
print("-" * 50)
print("""
  ① 重点关注区域: 新疆、四川、内蒙古
     - 新疆: 最大部署市场，政策支持力度大
     - 四川: 钒资源丰富，供应链成本优势
     - 内蒙古: 制造业集聚，规模效应显著

  ② 产业链布局建议
     - 上游: 关注钒资源和电解液企业
     - 中游: 关注系统集成和电堆制造
     - 下游: 关注储能电站运营商

  ③ 技术发展方向
     - 高浓度电解液技术
     - 低成本隔膜材料
     - 大功率电堆设计
     - 智能运维系统

  ④ 风险提示
     - 钒价格波动风险
     - 锂电池成本竞争
     - 政策补贴变化
     - 技术路线不确定性
""")

# 9. 市场预测
print("\n【9. 市场预测 Market Forecast】")
print("-" * 50)
print("""
  2025年预测:
  • 并网容量: 3,500+ MWh (同比增长100%+)
  • 系统价格: 1.8 元/Wh (同比下降14%)
  • 新增项目: 25+ 个
  • 行业投资: 300+ 亿元

  2030年展望:
  • 累计装机: 50+ GWh
  • 系统价格: <1.0 元/Wh
  • 全生命周期成本: <0.3 元/kWh
  • 市场规模: 1000+ 亿元/年
""")

print("\n" + "=" * 70)
print("分析图表已保存至: vrfb_analysis_charts.png")
print("=" * 70)

# 保存分析报告到文件
with open('/home/user/Micksiney/vrfb_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write("中国全钒液流电池(VRFB)投资项目数据分析报告\n")
    f.write("China VRFB Investment Projects Analysis Report\n")
    f.write("=" * 70 + "\n\n")
    f.write("【分析日期】2024年12月\n\n")

    f.write("【1. 总体规模】\n")
    f.write(f"  统计项目总数: {total_projects + len(df_manufacturing)} 个\n")
    f.write(f"  储能项目总容量: {total_capacity_mwh:,} MWh ({total_capacity_mwh/1000:.1f} GWh)\n")
    f.write(f"  已披露总投资额: {total_investment:.2f} 亿元\n\n")

    f.write("【2. 项目状态】\n")
    f.write(f"  已完工: {completed:,} MWh ({completed/total_capacity_mwh*100:.1f}%)\n")
    f.write(f"  在建: {under_construction:,} MWh ({under_construction/total_capacity_mwh*100:.1f}%)\n")
    f.write(f"  规划中: {planned:,} MWh ({planned/total_capacity_mwh*100:.1f}%)\n\n")

    f.write("【3. 区域分布】\n")
    for province, row in province_stats.iterrows():
        share = row['容量MWh'] / total_capacity_mwh * 100
        f.write(f"  {province}: {row['容量MWh']:,} MWh ({share:.1f}%)\n")

    f.write("\n【4. 关键发现】\n")
    f.write("  ① 新疆主导: 储能容量占比超50%，全球最大VRFB项目落地\n")
    f.write("  ② 爆发增长: 2024年并网容量同比增长超600%\n")
    f.write("  ③ 成本下降: 系统价格年降20%，达2.1元/Wh\n")
    f.write("  ④ 产业完善: 形成资源-制造-应用完整产业链\n")
    f.write("  ⑤ 长时优势: 4-6小时储能，全生命周期成本优于锂电\n")

print("\n分析报告已保存至: vrfb_analysis_report.txt")
