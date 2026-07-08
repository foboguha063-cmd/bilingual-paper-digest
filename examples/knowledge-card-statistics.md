# LD score regression

## **规范名 / 别名**
- 规范名：LD score regression
- 别名 / 同义名：LDSC；LD-score regression；连锁不平衡评分回归
- 不合并：linkage disequilibrium

## **知识层级**
- 所属领域：统计方法 / 遗传统计
- 上级概念：[[GWAS summary statistics 方法]]
- 下级概念：[[遗传相关性估计]]
- 同级 / 相关概念：[[Mendelian randomization]]；[[PGS]]

## **定义**
LD score regression 是一种利用 GWAS summary statistics 估计遗传相关性和区分多基因信号与群体结构混杂影响的统计方法。

## **适用问题**
- 研究问题类型：两个复杂性状是否共享遗传基础。
- 数据类型：GWAS summary statistics、LD scores。
- 常见论文语境：遗传相关、精神疾病共病、疼痛与睡眠等复杂性状研究。

## **核心假设**
- 多基因效应会使高 LD score 位点呈现更高检验统计量。
- 使用的 LD reference panel 与研究人群遗传背景应尽量匹配。

## **输入 / 输出**
- 输入：两个性状的 GWAS summary statistics、LD score reference。
- 输出：遗传相关系数 rg、标准误、p 值、截距等。

## **关键结果如何解读**
- rg：表示两个性状遗传效应方向和程度的相关性。
- p 值：检验遗传相关是否显著偏离 0。
- 截距：可用于评估混杂或样本重叠影响，但不能单独解决所有偏倚。

## **常见误读**
- 遗传相关不等于个体水平表型相关。
- 遗传相关不等于因果关系。
- 显著 rg 不能说明具体基因或通路机制。

## **相关方法**
- [[GWAS]]
- [[PGS]]
- [[Mendelian randomization]]

# **来源论文 / 应用场景**
1. [[慢性疼痛与睡眠障碍之间关联的多基因证据和重叠的大脑功能连接]]：用于评估慢性疼痛与睡眠障碍之间的遗传相关性。
