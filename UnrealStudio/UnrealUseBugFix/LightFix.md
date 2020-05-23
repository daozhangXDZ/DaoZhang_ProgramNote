中文 光照的常见问题和解决

2019年1月10日 星期四

18:54

 

中文 光照的常见问题和解决

**Contents**

 [hide] 

·         [1**关于本指南**](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.85.B3.E4.BA.8E.E6.9C.AC.E6.8C.87.E5.8D.97)

·         [2**一般照明**](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E4.B8.80.E8.88.AC.E7.85.A7.E6.98.8E)

·         [2.1为什么我的阴影是黑色的？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E4.B8.BA.E4.BB.80.E4.B9.88.E6.88.91.E7.9A.84.E9.98.B4.E5.BD.B1.E6.98.AF.E9.BB.91.E8.89.B2.E7.9A.84.EF.BC.9F)

·         [2.2将 BSP 转换为静态网格时光照贴图设置无效](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.B0.86_BSP_.E8.BD.AC.E6.8D.A2.E4.B8.BA.E9.9D.99.E6.80.81.E7.BD.91.E6.A0.BC.E6.97.B6.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE.E8.AE.BE.E7.BD.AE.E6.97.A0.E6.95.88)

·         [2.3如果我完全不想要光照贴图或游戏不需要光照贴图呢？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.A6.82.E6.9E.9C.E6.88.91.E5.AE.8C.E5.85.A8.E4.B8.8D.E6.83.B3.E8.A6.81.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE.E6.88.96.E6.B8.B8.E6.88.8F.E4.B8.8D.E9.9C.80.E8.A6.81.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE.E5.91.A2.EF.BC.9F)

·         [2.4用于单面网格的双侧照明，或者为何我的照明是穿过屋顶的？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E7.94.A8.E4.BA.8E.E5.8D.95.E9.9D.A2.E7.BD.91.E6.A0.BC.E7.9A.84.E5.8F.8C.E4.BE.A7.E7.85.A7.E6.98.8E.EF.BC.8C.E6.88.96.E8.80.85.E4.B8.BA.E4.BD.95.E6.88.91.E7.9A.84.E7.85.A7.E6.98.8E.E6.98.AF.E7.A9.BF.E8.BF.87.E5.B1.8B.E9.A1.B6.E7.9A.84.EF.BC.9F)

·         [2.5为何看起来与原来完全不同，即引擎比例调整](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E4.B8.BA.E4.BD.95.E7.9C.8B.E8.B5.B7.E6.9D.A5.E4.B8.8E.E5.8E.9F.E6.9D.A5.E5.AE.8C.E5.85.A8.E4.B8.8D.E5.90.8C.EF.BC.8C.E5.8D.B3.E5.BC.95.E6.93.8E.E6.AF.94.E4.BE.8B.E8.B0.83.E6.95.B4)

·         [2.6为何我的照明上有一个红色的“X”？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E4.B8.BA.E4.BD.95.E6.88.91.E7.9A.84.E7.85.A7.E6.98.8E.E4.B8.8A.E6.9C.89.E4.B8.80.E4.B8.AA.E7.BA.A2.E8.89.B2.E7.9A.84.E2.80.9CX.E2.80.9D.EF.BC.9F)

·         [2.7不合理的光照贴图 UV 布局](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E4.B8.8D.E5.90.88.E7.90.86.E7.9A.84.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE_UV_.E5.B8.83.E5.B1.80)

·         [2.8后期处理全局光照设置的作用](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.90.8E.E6.9C.9F.E5.A4.84.E7.90.86.E5.85.A8.E5.B1.80.E5.85.89.E7.85.A7.E8.AE.BE.E7.BD.AE.E7.9A.84.E4.BD.9C.E7.94.A8)

·         [2.9关节囊阴影](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.85.B3.E8.8A.82.E5.9B.8A.E9.98.B4.E5.BD.B1)

·         [3**动态（可移动）照明**](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.8A.A8.E6.80.81.EF.BC.88.E5.8F.AF.E7.A7.BB.E5.8A.A8.EF.BC.89.E7.85.A7.E6.98.8E)

·         [3.1阴影渗透或错误的阴影质量](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E9.98.B4.E5.BD.B1.E6.B8.97.E9.80.8F.E6.88.96.E9.94.99.E8.AF.AF.E7.9A.84.E9.98.B4.E5.BD.B1.E8.B4.A8.E9.87.8F)

·         [3.1.1只有定向光：层叠阴影贴图设置：](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.8F.AA.E6.9C.89.E5.AE.9A.E5.90.91.E5.85.89.EF.BC.9A.E5.B1.82.E5.8F.A0.E9.98.B4.E5.BD.B1.E8.B4.B4.E5.9B.BE.E8.AE.BE.E7.BD.AE.EF.BC.9A)

·         [3.1.2远处阴影](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E8.BF.9C.E5.A4.84.E9.98.B4.E5.BD.B1)

·         [3.1.3调整层叠以获得更好的质量：](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E8.B0.83.E6.95.B4.E5.B1.82.E5.8F.A0.E4.BB.A5.E8.8E.B7.E5.BE.97.E6.9B.B4.E5.A5.BD.E7.9A.84.E8.B4.A8.E9.87.8F.EF.BC.9A)

·         [3.1.4所有动态照明（“照明”选项卡设置）：](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E6.89.80.E6.9C.89.E5.8A.A8.E6.80.81.E7.85.A7.E6.98.8E.EF.BC.88.E2.80.9C.E7.85.A7.E6.98.8E.E2.80.9D.E9.80.89.E9.A1.B9.E5.8D.A1.E8.AE.BE.E7.BD.AE.EF.BC.89.EF.BC.9A)

·         [3.2为什么我的可移动照明在很远的距离透过网格照射出来？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E4.B8.BA.E4.BB.80.E4.B9.88.E6.88.91.E7.9A.84.E5.8F.AF.E7.A7.BB.E5.8A.A8.E7.85.A7.E6.98.8E.E5.9C.A8.E5.BE.88.E8.BF.9C.E7.9A.84.E8.B7.9D.E7.A6.BB.E9.80.8F.E8.BF.87.E7.BD.91.E6.A0.BC.E7.85.A7.E5.B0.84.E5.87.BA.E6.9D.A5.EF.BC.9F)

·         [4**静态照明**](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E9.9D.99.E6.80.81.E7.85.A7.E6.98.8E)

·         [4.1光照贴图分辨率/阴影质量](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE.E5.88.86.E8.BE.A8.E7.8E.87.2F.E9.98.B4.E5.BD.B1.E8.B4.A8.E9.87.8F)

·         [4.2间接照明的阴影接缝/明暗差异](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E9.97.B4.E6.8E.A5.E7.85.A7.E6.98.8E.E7.9A.84.E9.98.B4.E5.BD.B1.E6.8E.A5.E7.BC.9D.2F.E6.98.8E.E6.9A.97.E5.B7.AE.E5.BC.82)

·         [4.3构建照明时出现的“重叠 UV 错误”是什么意思？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E6.9E.84.E5.BB.BA.E7.85.A7.E6.98.8E.E6.97.B6.E5.87.BA.E7.8E.B0.E7.9A.84.E2.80.9C.E9.87.8D.E5.8F.A0_UV_.E9.94.99.E8.AF.AF.E2.80.9D.E6.98.AF.E4.BB.80.E4.B9.88.E6.84.8F.E6.80.9D.EF.BC.9F)

·         [4.4如何在编辑器中生成光照贴图 UV？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.A6.82.E4.BD.95.E5.9C.A8.E7.BC.96.E8.BE.91.E5.99.A8.E4.B8.AD.E7.94.9F.E6.88.90.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE_UV.EF.BC.9F)

·         [4.5如何使用静态照明控制全局光照？即反射的优点](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.A6.82.E4.BD.95.E4.BD.BF.E7.94.A8.E9.9D.99.E6.80.81.E7.85.A7.E6.98.8E.E6.8E.A7.E5.88.B6.E5.85.A8.E5.B1.80.E5.85.89.E7.85.A7.EF.BC.9F.E5.8D.B3.E5.8F.8D.E5.B0.84.E7.9A.84.E4.BC.98.E7.82.B9)

·         [4.6为什么我的静态网格上有阴影斑点？或者如何清理这些不干净的光照贴图？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E4.B8.BA.E4.BB.80.E4.B9.88.E6.88.91.E7.9A.84.E9.9D.99.E6.80.81.E7.BD.91.E6.A0.BC.E4.B8.8A.E6.9C.89.E9.98.B4.E5.BD.B1.E6.96.91.E7.82.B9.EF.BC.9F.E6.88.96.E8.80.85.E5.A6.82.E4.BD.95.E6.B8.85.E7.90.86.E8.BF.99.E4.BA.9B.E4.B8.8D.E5.B9.B2.E5.87.80.E7.9A.84.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE.EF.BC.9F)

·         [4.7左上角错误中的“需要重建照明”是什么意思？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.B7.A6.E4.B8.8A.E8.A7.92.E9.94.99.E8.AF.AF.E4.B8.AD.E7.9A.84.E2.80.9C.E9.9C.80.E8.A6.81.E9.87.8D.E5.BB.BA.E7.85.A7.E6.98.8E.E2.80.9D.E6.98.AF.E4.BB.80.E4.B9.88.E6.84.8F.E6.80.9D.EF.BC.9F)

·         [4.7.1故障排除技巧](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E6.95.85.E9.9A.9C.E6.8E.92.E9.99.A4.E6.8A.80.E5.B7.A7)

·         [4.8照明质量比较，或制作 > 预览](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E7.85.A7.E6.98.8E.E8.B4.A8.E9.87.8F.E6.AF.94.E8.BE.83.EF.BC.8C.E6.88.96.E5.88.B6.E4.BD.9C_.3E_.E9.A2.84.E8.A7.88)

·         [4.9光照贴图错误颜色](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE.E9.94.99.E8.AF.AF.E9.A2.9C.E8.89.B2)

·         [4.10查找“需要重建照明（X 个对象）”中引用的对象](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E6.9F.A5.E6.89.BE.E2.80.9C.E9.9C.80.E8.A6.81.E9.87.8D.E5.BB.BA.E7.85.A7.E6.98.8E.EF.BC.88X_.E4.B8.AA.E5.AF.B9.E8.B1.A1.EF.BC.89.E2.80.9D.E4.B8.AD.E5.BC.95.E7.94.A8.E7.9A.84.E5.AF.B9.E8.B1.A1)

·         [4.11照明构建统计信息](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E7.85.A7.E6.98.8E.E6.9E.84.E5.BB.BA.E7.BB.9F.E8.AE.A1.E4.BF.A1.E6.81.AF)

·         [4.12景观草类资产平铺图案](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E6.99.AF.E8.A7.82.E8.8D.89.E7.B1.BB.E8.B5.84.E4.BA.A7.E5.B9.B3.E9.93.BA.E5.9B.BE.E6.A1.88)

·         [4.13通过命令行构建照明](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E9.80.9A.E8.BF.87.E5.91.BD.E4.BB.A4.E8.A1.8C.E6.9E.84.E5.BB.BA.E7.85.A7.E6.98.8E)

·         [4.14植物叶子工具光照贴图分辨率](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E6.A4.8D.E7.89.A9.E5.8F.B6.E5.AD.90.E5.B7.A5.E5.85.B7.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE.E5.88.86.E8.BE.A8.E7.8E.87)

**关于本指南**

好游戏和优秀游戏的差距往往在于照明。即使是最优秀的模型，如果以较差的阴影分辨率渲染，并且没有利用适当的后期处理设置，也会看起来十分糟糕。在虚幻引擎中，这意味着要深入挖掘我们强大的照明、反射和后期处理设置。本《故障排除指南》尽量包含用户在最初深入挖掘照明和渲染系统时遇到的一些常见问题。本指南并不全面，但会随着引擎变化动态更新，所以我们会补充和变更此处提供的建议。本指南旨在为尝试充分利用引擎渲染系统的美工提供一个良好的开端。

**供参考的常用照明文档页面：**

[**光照系统 (Lightmass)** **全局光照**](https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/Lightmass/index.html)

[**照明基本知识**](https://docs.unrealengine.com/latest/INT/Resources/ContentExamples/Lighting/index.html)

[**环境照明**](https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/index.html)

[**照明内容示例**](https://docs.unrealengine.com/latest/INT/Resources/ContentExamples/Lighting/index.html)

[**移动平台照明**](https://docs.unrealengine.com/latest/INT/Platforms/Mobile/Lighting/index.html)

[**渲染和图形**](https://docs.unrealengine.com/latest/INT/Engine/Rendering/index.html)

**一般照明**

_________________________________________________________________________________________________

**为什么我的阴影是黑色的？**

用照明术语来说，深黑色阴影通常意味着没有辅助光。这种情况通常发生于单一方向光照是为了表示太阳的室外环境。UE4 内置了一种方法来提供全局影响辅助光，我们称之为**天空光**。[**想要进一步了解天空光？**](https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/LightTypes/SkyLight/index.html)

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image002.gif)](https://wiki.unrealengine.com/index.php?title=File:No_Skylight.png)

无天空光
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image004.gif)](https://wiki.unrealengine.com/index.php?title=File:Skylight.PNG)

有天空光

_________________________________________________________________________________________________

**将 BSP 转换为静态网格时光照贴图设置无效**

**从 4.6 及后续版本开始，任何转换的 BSP 的默认光照贴图分辨率将设置为 4，但仍需要根据下列步骤设置正确的光照贴图坐标索引。**

在将 BSP 几何结构转换为静态网格时，很可能会看到如下结果：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image006.gif)](https://wiki.unrealengine.com/index.php?title=File:BSPToSM_InvalidLMSettings.PNG)

从 BSP 箱体转换的静态网格

不必担心，这是正常情况！由于我们现在已经将 BSP 转换为了静态网格，所以需要确保指定正确的光照贴图通道。为了方便操作，在转换 BSP 时，会自动为你生成光照贴图 UV。唯一没有自动设置的是需要确保指定正确的通道和分辨率。 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image008.gif)](https://wiki.unrealengine.com/index.php?title=File:BSPLMSetup.png)

静态网格编辑器“细节”面板

·         为执行此操作，打开新创建的静态网格。查看右侧的“细节”面板，并找到“静态网格设置”选项卡。

·         在这里需要设置光照贴图分辨率。这可以是 2 的任何幂次方（即32、64、128 等）。这将是光照贴图纹理的分辨率。光照贴图分辨率越高，烘焙到纹理中的阴影质量越好，但也会增加内存占用量和照明构建时间。

·         接下来，将光照贴图坐标索引设置为 1（这是大多数情况下使用的光照贴图 UV 通道）。这是不会有任何重叠面的光照贴图 UV 位置。

·         如果想要查看光照贴图 UV 的效果，可以单击工具栏中的 UV 对应按钮，从按钮右侧的下拉列表中选择“UV 通道 1”。

 

_________________________________________________________________________________________________

**如果我完全不想要光照贴图或游戏不需要光照贴图呢？**

有时，游戏并不需要光照贴图，因为已经选择只使用可移动（动态）照明。有一个选项可以禁用全部光照贴图，方法是打开“全局设置”，选中“不使用预先计算的照明”选项。当重新构建照明时，会删除之前烘焙过的所有光照贴图。

禁用静态照明有两种方法：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image010.gif)](https://wiki.unrealengine.com/index.php?title=File:1_ProjectSettings.png)

项目设置、“渲染”选项卡、“照明”选项卡

**特定于项目：禁用静态照明**

·         菜单 > 编辑 > 项目设置

·         转至“渲染”选项卡 >“照明”选项卡

·         取消选中**允许静态照明**选项

·         要使该选项彻底生效，需要**重新启动编辑器**

 

**特定于关卡：禁用静态照明**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image012.gif)](https://wiki.unrealengine.com/index.php?title=File:World_Settings_Toolbar.png)

全局设置

1.打开“全局设置”

 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image014.gif)](https://wiki.unrealengine.com/index.php?title=File:2_WorldSettings.png)

光照系统设置

2.转至“光照系统”选项卡

3.取消选中**不使用预先计算的照明**

 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image016.gif)](https://wiki.unrealengine.com/index.php?title=File:3_ForcedNoPreComp_Warning.png)

不使用预先计算的照明警告

4.你会看到一个警告。单击“确定”。

5.构建照明以擦除已经存储的照明数据。

 

_________________________________________________________________________________________________

**用于单面网格的双侧照明，或者为何我的照明是穿过屋顶的？**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image018.gif)](https://wiki.unrealengine.com/index.php?title=File:1_3Ds_Max_geometry.png)

用 3DS Max 创建的资产

在该图中，你已经看到我创建了一面效果很不错的墙和一个管子，如果我把管子放倒的话，走进去会很瘆人！

 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image020.gif)](https://wiki.unrealengine.com/index.php?title=File:2_UE4Import.png)

用 UE4 创建的资产

整体看起来不错，效果理想，而且在我自己的选择的建模程序中能看到网格的两个面。但是，导入到虚幻引擎 4 之后就变样了！

那么为何会如此呢，难道是因为这样就是不对吗？

这完全是 100% 正常的（一语双关）。即使这个平面看起来正常，但是背面并没有像管子网格最靠近我们的这一面一样进行渲染。

 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image022.gif)](https://wiki.unrealengine.com/index.php?title=File:3_Wireframe.png)

用 UE4 创建的资产的线框

默认情况下，在建模程序中创建几何结构时，软件会设置为让你看到几何结构的两个面。

在 UE4 中，会自动剔除多边形的背面以提高性能，每一个细节都会有助于性能的提高！并不总是需要显示额外的多边形或者渲染可能并不需要的面，否则，会调用额外的绘图功能，从而导致性能变慢，在一些情况下，影响可能并不明显，但针对特定平台进行开发或者每次调用绘图功能都要进行大量计算时，影响就会凸显出来。

为了理解为何只能看到一面，我们可以在静态网格编辑器中打开网格，勾选工具栏选项“法线”。就会看到绿色线条指向多边形面的方向。在下面这个管子资产图形中，我们可以看到，不可见面的线条指向网格中心。这是可以观察到可见面的方向。

 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image024.gif)](https://wiki.unrealengine.com/index.php?title=File:4_SMEditor_Normals.png)

静态网格编辑器

**专家提示：**在 UE4 中，如果有任何网格包含似乎不可见的几何结构或者缺少某些面，可以在这里检查法线，然后再去建模软件中解决该问题。

 

现在，我们已经扫清了障碍，可以直奔主题，通过一些复选框和材质解决不可见面的问题。

1.**（仅限静态）像双面一样照明**

o  在“细节”面板中，针对关卡视口中选中的资产启用该选项。

o  选中该选项后，当构建照明时，光照系统会将该几何结构计算到烘焙中。它会投射阴影以便将其烘焙到光照贴图纹理中，虽然我们从这个角度看不到阴影。这并不适用于可移动/动态照明，因为虚幻引擎 4 会使用延迟渲染管道。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image026.gif)](https://wiki.unrealengine.com/index.php?title=File:6_twosidedDetailsPanel.png)

关卡视口中资产的“细节”面板
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image028.gif)](https://wiki.unrealengine.com/index.php?title=File:5_LightasTwoSided.png)

最终结果

2.**创建双面材质**

o  打开材质编辑器，在左侧的“细节”面板中，选择“双面”选项。

o  保存并编译材质以使该设置生效。

o  这种方法可以用于静态/静止/可移动照明。由于正在渲染的是材质，因此之前不可见的面不会再被剔除，因此可能会阻挡光线。但请注意，现在会渲染网格的两个面，因此会增加绘图调用。正如之前所述，在较小场景或设置中这未必会影响性能，但如果你的目标硬件很容易受到性能影响则另当别论。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image030.gif)](https://wiki.unrealengine.com/index.php?title=File:7_Materials_DetailPanel.png)

材质属性“细节”面板
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image032.gif)](https://wiki.unrealengine.com/index.php?title=File:8_materialtwosidedresults.png)

最终结果

_________________________________________________________________________________________________

**为何看起来与原来完全不同，即引擎比例调整**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image034.gif)](https://wiki.unrealengine.com/index.php?title=File:1_EngineScalability.png)

引擎比例调整设置

引擎比例调整设置可以通过工具栏中的“设置 > 引擎比例调整”选项进行访问。

该设置的目的是按比例调整引擎渲染设置，以适应难以流畅运行的机器。默认情况下，编辑器会在 FPS 降得过低时降低这里的设置。

“阴影”选项会直接影响任何可移动（动态）阴影的阴影距离。当列表设置为“可移动”或者尚未构建静态照明时确实如此，因为此时会使用动态阴影作为临时参考，直到照明构建完成并烘焙到光照贴图中为止。

 

下面的图形演示了“引擎比例调整”选项卡中每种阴影设置的阴影距离。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image036.gif)](https://wiki.unrealengine.com/index.php?title=File:2_StatueShadowsEPIC.png)

Epic
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image038.gif)](https://wiki.unrealengine.com/index.php?title=File:3_StatueShadowsHIGH.png)

高
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image040.gif)](https://wiki.unrealengine.com/index.php?title=File:4_StatueShadowsMEDIUM.png)

中
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image042.gif)](https://wiki.unrealengine.com/index.php?title=File:5_StatueShadowsLOW.png)

低

如果你的关卡中没有阴影，则最好先从这里开始检查。即使用的是最顶级的系统，这些设置仍会自动设置为较低值，并且在 FPS 降得过低时保持不变。最好总是先检查这里的设置，然后再查看可能的其他问题。

如果因为某种原因而不需要自动按比例调整，可以取消选中“引擎比例调整”窗口底部的对应选项来将其禁用。需要注意的是，这样可能会导致性能问题，因为编辑器不会再监视需要调整为较低设置以保持正常性能的情况。

[**想要进一步了解引擎比例调整？**](https://docs.unrealengine.com/latest/INT/Engine/Performance/Scalability/ScalabilityReference/index.html#scalabilitysettings) _________________________________________________________________________________________________

**为何我的照明上有一个红色的“X”？**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image043.jpg)](https://wiki.unrealengine.com/index.php?title=File:OverlappingLights.jpg)

重叠静止照明

静止照明限制为最多可以重叠 4 层阴影投射照明。如果添加了第 5 层，就会出现一个红色的“X”，表示这一重叠区域中半径最小的照明将还原为动态照明。这会导致性能问题，因为投射阴影的动态照明比烘焙照明相比耗用的资源更多。

 

如果照明是使用任何静止光照构建的，并且这些静止光照是重叠问题光，那么就会显示一个警告，详细指出哪个是问题光，哪个是衍生光。

 

为了更正此问题，请确保一个区域中的阴影投射重叠静止光照不会超过 4 层。可能需要删除光照，禁用投射阴影标志，或者调整半径直到不再重叠为止。

如果只放置了三层静止光照，而第 4 层光照上出现了红色 X，请确保关卡中没有其他静止光照会导致重叠。这往往是因为定向光设置为静止而导致发生此问题。

[**想要进一步了解静止光照？**](https://docs.unrealengine.com/latest/INT/Resources/ContentExamples/Lighting/2_2/index.html)

_________________________________________________________________________________________________

**不合理的光照贴图 UV 布局**

实现良好的光照贴图烘焙的关键就是正确设置光照贴图，让它能够有效地利用 0-1 UV 空间。超出该空间范围或者有重叠面时，就会在贴图检查警告中看到“光照贴图重叠 xx%”！

建议首先阅读我们提供的关于正确设置光照贴图的文档。在以下地址阅读关于 UE4 光照贴图的所有资料。

·         <https://docs.unrealengine.com/latest/INT/Engine/Content/Types/StaticMeshes/LightmapUnwrapping/>

以下是设置光照贴图时需要谨记的要点：

·         不能有重叠面

·         不能超出 0,1 UV 空间范围

·         平面贴图不是最佳方法，通常会导致光照贴图出现许多错误

·         要充分利用 0,1 UV 空间，以便不会浪费纹理空间。

·         如果你的网格较大并且可能会很复杂，为了达到良好的光照贴图分辨率以及一些其他性能因素（例如遮蔽剔除），最好细分成多个部分。

·         使用尽可能最低的光照贴图分辨率，以节省运行时纹理内存。

·         确保 UV 岛之间至少有 2 个像素的间隔，以防止发生光线透射。光照贴图的目标分辨率可能会导致发生此情况。

_________________________________________________________________________________________________

**后期处理全局光照设置的作用**

后期处理体积可以成为处理场景照明的强大工具，尤其是静态照亮区域。你可以通过调整后期处理设置中的下列设置，进行轻松控制。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image045.gif)](https://wiki.unrealengine.com/index.php?title=File:PPV_GlobalIllumination.png)

GI 后期处理设置

在以下这个简单的示例中，完全是用发光材质表示杆，在房间设置一个暗淡的点光源，并设置了两个重叠的后期处理体积进行控制的。这是使用后期处理伪造某种动态 GI 的极其低端的方法！

设置：

·         利用非常暗淡的点光源来表示房间中某种柔和的环境光。

·         对移动杆应用了简单的发光材质，并用一个乘数来控制亮度。

·         围绕着场景运用了一个后期处理体积，使用的是默认设置，除非要针对基本场景更改其他设置，否则其实并不需要该设置。

·         第二个后期处理体积是与移动杆相连的，跟随着杆移入和移出视线。长度上比移动杆稍大，这样就会存在一部分的重叠。这里进行了三处设置调整，令其更顺利地发挥作用。

·         “间接照明颜色”设置为类似于移动杆自发光色的颜色，但颜色较浅。

·         “间接照明强度”进行了调整，令人感觉这种自发光并没有投射到房间里。

·         后期处理体积的转接半径用于转接两个体积，在房间里形成一种自然的光线渗透效果。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image047.jpg)](https://wiki.unrealengine.com/index.php?title=File:GIChange.gif)

示例场景（如果未加载 gif，请单击此图）

这完全是用后期处理体积和静态照明控制的！如果需要作出一些风格选择，能够控制烘焙 GI 可以让你更多地控制整个场景，不必完全依赖于照明构建就可以达到 100% 的精确性。

_________________________________________________________________________________________________

**关节囊阴影**

关节囊阴影是 4.11 及后续版本中的新功能，让骨架网格能够更好地融入到间接照亮和直接照亮区域中，并带有柔和阴影。

如果你尚未使用过该功能，该页面教程可以帮助你入门。

<http://timhobsonue4.snappages.com/lighting-capsule-shadows>

_________________________________________________________________________________________________

**动态（可移动）照明**

_________________________________________________________________________________________________

**阴影渗透或错误的阴影质量**

在本指南中，我们将研究如何帮助提高质量，以使阴影更精准地融入到网格中。我们还会提供一些提示来改善远距离的动态照明。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image049.gif)](https://wiki.unrealengine.com/index.php?title=File:Dynamic_Default_Shadows.png)

阴影渗透或阴影质量不正确示例

**只有定向光：层叠阴影贴图设置：**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image051.gif)](https://wiki.unrealengine.com/index.php?title=File:2_settings.png)

定向光细节中的层叠阴影贴图设置

**动态阴影距离可移动**：这是阴影将覆盖到的距离镜头的距离。值 0 将禁用此设置。

 

**动态阴影距离静止**：这是阴影将覆盖到的与镜头的距离。默认情况下，针对定向静止光，该选项设置为 0

 

**动态阴影层叠数**：这是视锥体将拆分成的层叠数。层叠越多，阴影分辨率越高，但也会显著增加渲染成本。要进一步了解视锥体，请查看以下文章：<http://en.wikipedia.org/wiki/Viewing_frustum>

·         **动态阴影层叠数（在以下示例中，下文将会讲述的阴影偏移已经设置为 0，可以更清楚地看到层叠。**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image053.gif)](https://wiki.unrealengine.com/index.php?title=File:1Cascades0.png)

层叠数 = 0
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image055.gif)](https://wiki.unrealengine.com/index.php?title=File:1Cascades1.png)

层叠数 = 1
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image057.jpg)](https://wiki.unrealengine.com/index.php?title=File:1Cascades2.png)

层叠数 = 2

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image059.gif)](https://wiki.unrealengine.com/index.php?title=File:1Cascades3.png)

层叠数 = 3（默认值）
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image061.jpg)](https://wiki.unrealengine.com/index.php?title=File:1Cascades4.png)

层叠数 = 4

**层叠分布指数**：该设置控制层叠分布的是离镜头更近一些（值越大）还是更远一些（值越小）。值 1 表示将按照分辨率成比例地过渡。

·         **层叠分布指数**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image063.gif)](https://wiki.unrealengine.com/index.php?title=File:2Distribution1.png)

分布 = 1
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image065.gif)](https://wiki.unrealengine.com/index.php?title=File:2Distribution2.png)

分布 = 2
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image067.gif)](https://wiki.unrealengine.com/index.php?title=File:2Distribution3.png)

分布 = 3

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image069.jpg)](https://wiki.unrealengine.com/index.php?title=File:2Distribution4.png)

分布 = 4

**层叠过渡指数**：该选项控制各个层叠之间的消退区域比例。较低值会在阴影层叠之间产生硬边，较大的值会让两个层叠融合起来。

·         **层叠过渡指数**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image071.jpg)](https://wiki.unrealengine.com/index.php?title=File:3TransitionGif.gif)

过渡效果

·         **层叠过渡指数**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image073.jpg)](https://wiki.unrealengine.com/index.php?title=File:3TransitionHard.png)

硬边（值较低）
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image075.jpg)](https://wiki.unrealengine.com/index.php?title=File:3TransitionBlended.png)

融合边（值较高）

**阴影距离淡出分数**：该选项控制一定距离阴影的淡出效果。较大的值会令阴影淡出，而较低的值会留下一定距离的较深阴影。

·         **阴影距离淡出分数**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image077.jpg)](https://wiki.unrealengine.com/index.php?title=File:4Fadeout0.png)

淡出 = 0
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image079.jpg)](https://wiki.unrealengine.com/index.php?title=File:4Fadeout1.png)

淡出 = 1

**远处阴影**

该选项用于为静态网格或景观设置远处阴影，好处是能够让层叠阴影贴图延伸到非常远的距离，而不是局限在接近镜头的有限范围内。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image081.jpg)](https://wiki.unrealengine.com/index.php?title=File:FarShadows.png)

启用远处阴影

通过在定向光设置中的“层叠阴影贴图”下启用“远处阴影层叠”可以控制该设置。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image083.jpg)](https://wiki.unrealengine.com/index.php?title=File:CSMFarShadowSettings.png)

远处阴影设置

你可以将要使用的远处阴影层叠数和启用了远处阴影标志的 Actor 将投射阴影的距离一起设置。对于该默认设置，使用 300 米作为起始距离。该值也应该比离镜头最近的层叠阴影贴图距离要大。

此外，还需记住的是，该选项最合适用于远处的较大物体，不建议用于所拥有的每一个网格。这样可能会对性能产生明显影响，正因如此，需要选择想要使用远处阴影的每个静态网格

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image085.jpg)](https://wiki.unrealengine.com/index.php?title=File:Farshadow.gif)

远处阴影演示（如果未加载 gif，请单击此图）

在该设置中，定向光的动态阴影距离已经设置为 5000 个单位，远处阴影距离设置为 50000 个单位，具有 4 层远处阴影层叠。

左侧的静态网格不使用远处阴影，右侧的启用了远处阴影。

 

 

**调整层叠以获得更好的质量：**

阴影渗透和精确性可以通过调整上述演示的设置组合进行微调。本节将尝试调整这些值，以获得更好的阴影精确性，并且令阴影紧随着镜头的移动而移动。寻找一种适合任何特定游戏的平衡需要投入时间和精力，反复测试才能得出最合适的设置。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image087.jpg)](https://wiki.unrealengine.com/index.php?title=File:1AdjustingSettings1.png)

基本场景，默认设置

这是只采用了默认设置的基本场景：

 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image087.jpg)](https://wiki.unrealengine.com/index.php?title=File:1AdjustingSettings2_ProblemAreas.png)

高亮问题区域

该场景中已经普遍存在一些与阴影边缘精确性有关的问题。

 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image089.jpg)](https://wiki.unrealengine.com/index.php?title=File:1AdjustingSettings2_ProblemAreasCloser.png)

高亮问题区域，特写镜头

这里展示得更为清楚。

 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image091.jpg)](https://wiki.unrealengine.com/index.php?title=File:1AdjustingSettings2_finalResult.png)

默认场景，最终效果

通过着重调整**层叠分布指数**，阴影渗透当然可以尽量降低。动态阴影的默认距离是 20,000 个单位。不一定非要设置为默认值，为了更好地利用层叠，可以设置为更低的值。

如果游戏关卡要使用室内和室外场景，寻找一种适合所有或大部分区域的组合非常难，需要经过大量的调整。没有任何一种设置会让所有画面都有完美的效果。

在该场景中，通过调整分布、阴影距离和层叠数设置，渗透和精确性才达到可以接受的程度。

 

**所有动态照明（“照明”选项卡设置）：**

最后，在光源的“照明”选项卡中还有两个设置对提高照明精确性有所帮助。

这些设置位于以下位置：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image093.jpg)](https://wiki.unrealengine.com/index.php?title=File:DynamicLightSettings.png)

照明细节、阴影偏移和过滤清晰度

**阴影偏移**控制如何在场景中显示确切的阴影，但如果设置的值较低，就会产生失真。缺省值为 0.5，能够很好地权衡精确性和实际效果。

**阴影过滤清晰度**可以帮助遮住一些因为较低值产生的失真，这也会直接影响阴影边缘的清晰度。

考虑到没有对下面的图片调整过上述任何设置，它们演示了**阴影偏移**和**阴影过滤清晰度**默认的效果。

·         **阴影偏移**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image095.jpg)](https://wiki.unrealengine.com/index.php?title=File:Dynamic_AdjustedShadows.png)

阴影偏移 = 0.5（默认值）
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image097.jpg)](https://wiki.unrealengine.com/index.php?title=File:Dynamic_Artifacts.png)

阴影偏移 = 0，调整得过低会导致失真

关键在于要找到一个很好的平衡点，不能设置得过低，合理地利用选项卡中的层叠阴影设置。

·         **阴影过滤清晰度，较高的值会锐化阴影边缘**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image099.jpg)](https://wiki.unrealengine.com/index.php?title=File:FilterSharpen1.png)

过滤清晰度 = 0
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image101.jpg)](https://wiki.unrealengine.com/index.php?title=File:FilterSharpen2.png)

过滤清晰度 = 1

最明显的是，清晰度过滤的值越高，阴影越清晰。较低值导致的软边现在已经消失。 _________________________________________________________________________________________________

**为什么我的可移动照明在很远的距离透过网格照射出来？**

动态照明，尤其是点光源会导致突然发生此类问题。虚幻引擎 4 在这方面优化具有很好的表现，这样用户就不必太过担心此问题。问题是有时会失去控制，导致发生此类没有明显解决办法的问题。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image103.jpg)](https://wiki.unrealengine.com/index.php?title=File:1.png)

这是我们需要的效果，靠近镜头
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image103.jpg)](https://wiki.unrealengine.com/index.php?title=File:4.png)

离镜头较远

那么为何会如此呢？

为了方便解释，我们需要讨论引擎实现了哪些非常棒的优化。引擎使用场景深度来确定哪些内容可见，哪些不可见。由于我们这里有一个点光源，按照设定的半径射出光线，当网格超出其边界时，就会被遮蔽或者不再显现。这就会导致我们所看到的问题，即光线开始朝着所有的方向投射。

从下图中可以看到，当镜头逐渐远去，网格遮蔽部分开始在外边缘形成光晕，直到光线可以朝着所有方向投射。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image103.jpg)](https://wiki.unrealengine.com/index.php?title=File:WallOcclusion.gif)

网格照明遮蔽

你或许已经注意到，如果在远距离处选择网格，照明就会恢复为正常。这是正常情况，因为你刚刚选择了网格，网格现在获得了焦点。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image105.jpg)](https://wiki.unrealengine.com/index.php?title=File:Detailspanel.png)

对象界限，“细节”面板，“渲染”选项卡

为防止网格被遮挡，需要选择网格并转至“细节”面板。在这里搜索或滚动到“界限比例”（位于“渲染”选项卡下面。）

 

默认值设置为 1.0。增大这个比例时，确保仅使用较小的增量数字。使用值 2.0 会导致已经设置好的距离翻倍，这可能是过度设置。尝试每次增加较小的值。（即1.1、1.2）。不必超过自己所需的设置，因为这样会影响性能和阴影质量。

你可以转至“视口 > 显示 > 高级 > 界限”来显示网格界限。

你会看到如下示例：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image107.jpg)](https://wiki.unrealengine.com/index.php?title=File:Bounds.png)

显示的对象界限

 

附加提示：

如果你遇到网格遮蔽的问题，但考虑到性能原因而不想增大界限比例，可以尝试使用聚光灯。由于这只会朝着单一方向投射光线，所以当网格被遮蔽时，不会看到点光源朝着所有方向投射光线的情况。这非常适用于曾经演示过的相似情况，但可能需要针对具体项目进行一些测试来达到理想的效果。

或者，你可以放弃完全可移动/动态照明，使用静止照明来烘焙光照贴图纹理，这样在运行时渲染阴影信息是零开销的，所以也有助于性能稳定。 _________________________________________________________________________________________________

**静态照明**

 

**光照贴图分辨率/阴影质量**

每一个项目都有其独特的艺术方向和目标，所以本节意在介绍一些常见的概念，提供一些基本知识，便于你开始实现通过静态照明想要达到的效果。我们在此提供的设置并不一定始终适合于每一个项目。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image109.jpg)](https://wiki.unrealengine.com/index.php?title=File:LM_Resolution.PNG)

包含 3 个静态网格的样本场景

该场景中有 3 个对象，两面墙和一个地板网格。每一个对象都有自己的阴影，阴影烘焙到纹理中，称为光照贴图。该光照贴图将投射到自身的任何阴影/照明信息存储到该纹理中。这通常由美工在创建资产时处理。[**想要进一步了解光照贴图以及如何有效地创建光照贴图？**](https://docs.unrealengine.com/latest/INT/Engine/Content/Types/StaticMeshes/LightmapUnwrapping/index.html)

换言之，如果我想提高墙投射到门口的阴影的分辨率，我不会调整门口，而是调整地板的光照贴图分辨率。这是阴影所投射到并烘焙到光照贴图的位置。

明确这一点之后，我们可能只需要提高一部分网格的光照贴图分辨率。每个网格都有自己的光照贴图分辨率，选择网格后可以通过“细节”面板进行设置，也可以通过网格编辑器进行设置。

对于该光照贴图质量演示，我们只需研究地板网格的光照贴图分辨率即可。

在调整 LM 分辨率时，确保使用 2 的幂次方（32 [引擎默认值]、64、128 等），但 BSP 例外（详情见下文）

该光照贴图分辨率的质量主要取决于两个因素：网格大小和光照贴图 UV 中的 UV 壳的大小。

·         **静态网格的光照贴图分辨率**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image111.jpg)](https://wiki.unrealengine.com/index.php?title=File:LM64.PNG)

分辨率 = 64
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image113.jpg)](https://wiki.unrealengine.com/index.php?title=File:LM128.PNG)

分辨率 = 128
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image115.jpg)](https://wiki.unrealengine.com/index.php?title=File:LM256.PNG)

分辨率 = 256

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image117.jpg)](https://wiki.unrealengine.com/index.php?title=File:LM512.PNG)

分辨率 = 512

需要注意的是，在 BSP 上使用光照贴图与在静态网格上使用光照贴图的主要差异在于值不会增大，而是降低才能获得更好的分辨率。

·         **BSP** **光照贴图分辨率**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image119.jpg)](https://wiki.unrealengine.com/index.php?title=File:BSPLM32.PNG)

分辨率 = 32
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image121.jpg)](https://wiki.unrealengine.com/index.php?title=File:BSPLM24.PNG)

分辨率 = 24
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image123.jpg)](https://wiki.unrealengine.com/index.php?title=File:BSPLM16.PNG)

分辨率 = 16

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image125.jpg)](https://wiki.unrealengine.com/index.php?title=File:BSPLM8.PNG)

分辨率 = 8

虽然调整光照贴图分辨率可以获得更好的结果，但是仍有一些取舍。如果使用较小网格，那么光照贴图分辨率较低的地板会有更好的效果，如果使用更大的网格，就需要增大光照贴图分辨率，纹理也会占用更多游戏资源。

·         **景观光照贴图分辨率**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image127.jpg)](https://wiki.unrealengine.com/index.php?title=File:LandscapeDefault1.png)

分辨率 = 1.0
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image129.jpg)](https://wiki.unrealengine.com/index.php?title=File:Landscape2.png)

分辨率 = 2.0

就像在使用 BSP 和静态网格时设置静态照明分辨率的差异一样，景观也有稍许不同。景观光照贴图分辨率使用一个乘数，为烘焙后的阴影提供更好的分辨率。较大景观可能需要更大的分辨率值，而较小景观则相反。

在“细节”面板中，你可以选择增大**静态照明分辨率**，其默认值为 1。调整该设置时，只需以整数为增量逐渐增大即可，直到达到所需分辨率。 _________________________________________________________________________________________________

**间接照明的阴影接缝/明暗差异**

通常在构建项目照明时，在间接照亮区域中，可能会注意到模块化平面之间有时会出现明暗差异，通常是墙面、地面和天花板。这是目前由于对静态间接照明的处理方式而导致的负面影响，无法轻易解决。希望将来能够加以改善。

以下是对该问题的详细剖析，方便对此尚不熟悉的读者学习。

·         照明点亮了一个表面，然后光线反射到了周围的表面上。这种类型的反射光称为间接照明。有些表面也会被直接照亮，同时也会接收到一些反射光，比如下图中的墙，一部分是完全照亮的，一部分接收了间接照明，因此在有阴影的角落出现了明暗问题。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image131.jpg)](https://wiki.unrealengine.com/index.php?title=File:LightBounce.png)

光线反射示例

·         如果接收间接照明的表面是纯平面，就会产生下图这样的明暗差异：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image133.jpg)](https://wiki.unrealengine.com/index.php?title=File:Shading.png)

间接照明失真

 

其过程是这样的，每一个静态网格都会发送到 CPU，按照接收的顺序通过不同的 CPU 线程进行处理。这就意味着，虽然每一个静态网格都通过光照系统构建了自己的照明，而其他网格并不知道自己前面的网格具有怎样的明暗设置，也就无法参考边缘来确保匹配。因此导致各个平面之间存在轻微的明暗差异。

现在大家一定在想，我该怎么解决这个问题呢？

在全局设置的光照系统部分下，可以调整一些设置来获得更好的效果。

·         间接照明质量可以设置为 2 或更大的值。

·         间接照明平滑度通常可以设置为 .65-.75 的范围。该值越低，失真的可能性越大，导致光照贴图看起来就像有污渍。

·         （仅建议高级用户使用！！）静态照明关卡比例可以调整为较低值，也可以获得更好的融合效果。但是这会更改为整个关卡计算照明的比例。如果将该值降低，会明显增加构建时间，但结果也会更好。该设置通常被建筑可视化领域的从业者们使用，游戏开发者则不常用，除非具有特定的原因并理解该选择的效果。

调整间接照明的质量时，降低照明平滑度总是很好的做法，这样可以获得更好的结果。这样有助于各个面更自然地衔接起来，但不一定会彻底解决该问题，而且也可能会产生其他负面影响。应该在项目或测试贴图中进行测试，充分理解各种调整的影响以及原因。

还可以执行一些其他步骤来降低这种失真的明显程度，并执行一些其他操作来改进项目设计。

·         尽量不要将关卡设计得过于模块化！这一点十分重要。有些人可能会觉得，把一面中等面积的墙体分解成一块块小型的精简拼块，然后像乐高一样打包在一起是最好的做法，但这就会有明暗差异的风险，而且现在会有更多的 Actor，导致绘图调用增加，资产可见性检查量也会增加。最好是就设计一面墙，这样更为合理，而不是许多小的拼块。这样绘图调用数量降低，照明问题也会减少。

·         只需要使用一些其他的几何结构来隐藏可能存在接缝的位置即可，比如柱状体、邻接墙或踢脚线。

 

_________________________________________________________________________________________________

**构建照明时出现的“重叠 UV 错误”是什么意思？**

在使用静态或静止照明时，必须在网格中使用两个 UV，否则在构建照明时就会看到如下警告：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image135.jpg)](https://wiki.unrealengine.com/index.php?title=File:Overlapping_UV_Error.PNG)

消息日志，照明结果

这意味着需要为光照贴图建立第二个 UV 通道，否则编辑器就会使用现有的纹理 UV 作为光照贴图，从而引起这一类的错误。

要解决该问题，可以调整光照贴图的 UV，以便不会出现重叠面。

该操作可以[在编辑器中](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E5.A6.82.E4.BD.95.E5.9C.A8.E7.BC.96.E8.BE.91.E5.99.A8.E4.B8.AD.E7.94.9F.E6.88.90.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE_UV.EF.BC.9F)通过生成光照贴图执行，也可以使用所选的建模软件来创建和编辑 UV。

·         **原始 UV 和结果**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image137.jpg)](https://wiki.unrealengine.com/index.php?title=File:Overlapping_LogoUV.PNG)

重叠 UV
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image139.jpg)](https://wiki.unrealengine.com/index.php?title=File:Overlapping_UV_Results.PNG)

编辑器中的结果

·         **更正后的 UV 和结果**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image141.jpg)](https://wiki.unrealengine.com/index.php?title=File:Overlapping_LogoUV_Adjusted.PNG)

更正后的 UV
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image143.jpg)](https://wiki.unrealengine.com/index.php?title=File:Overlapping_UV_Results_Adjusted.PNG)

编辑器中的结果

请注意，最终结果中的 UV 没有重叠面，所以可以正确烘焙纹理的阴影/照明信息，从而在构建照明后应用到网格。

如果有重叠面，就会因为无法正确烘焙照明信息而产生不正确的明暗效果。 _________________________________________________________________________________________________

**如何在编辑器中生成光照贴图 UV？**

在 4.5 版本中，编辑器会自动在导入时或使用网格编辑器生成 UV。

我们假设你想要从网格编辑器进行设置。

·         打开想要为其创建光照贴图的网格。

·         在右侧找到如下面板：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image145.jpg)](https://wiki.unrealengine.com/index.php?title=File:GeneratedLMs.png)

静态网格编辑器“细节”面板

该面板允许您创建光照贴图通道，但这里不能直接控制光照贴图分辨率，也不能指定坐标索引。这些设置将在下文进一步介绍。

“构建设置”选项卡中需要重点关注的设置包括：

**生成光照贴图 UV** = 确保选中该项。

**最低光照贴图分辨率** = 这是你希望光照贴图分辨率具有的最小值。

**源点光照贴图索引** = 这是要从中生成光照贴图 UV 的源点。

**目标光照贴图索引** = 这是在创建后将用于存储该 UV 的位置。

对于大多数资产而言，上述设置足以满足需要。关键是要确保选择正确的源点光照贴图索引。这是通常用于纹理的 UV。该 UV 中的 UV 壳/岛会重新打包，避免出现重叠面，这对于使用光照贴图而言至关重要。

对于光照贴图分辨率设置，从较低值开始使用也并不是坏事，因为不一定会用到这个分辨率。如果决定使用较高分辨率，无需回到这里更改设置，除非你知道这样会改善光照贴图烘焙。在大多数情况下不必如此。

单击“应用更改”之后，可以验证是否创建了光照贴图，查看是否有任何错误。

要执行此操作，可以转至网格编辑器工具栏，单击 UV 图标来显示 UV，并使用右侧的下拉按钮来选择 UV 通道 1，就可以看到新创建的光照贴图。

应该类似于以下内容：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image147.jpg)](https://wiki.unrealengine.com/index.php?title=File:UVChannelSelection.png)

静态网格编辑器，UV 通道选择

至此本过程还未结束。我们还需要指定正确的 UV 通道来用于光照贴图。

在网格编辑器右侧的“细节”面板中，找到“静态网格设置”选项卡?

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image149.jpg)](https://wiki.unrealengine.com/index.php?title=File:LightmapUVSet.PNG)

静态网格编辑器细节，光照贴图设置

·         在该选项卡中，需要调整所需的光照贴图分辨率。

32 是默认光照贴图分辨率。该值适用于较小物体。对于较大物体，可能需要使用更高的分辨率。

确保以 2 的幂次方调整该值。（即32、64、128、256 等）

·         需要核实的下一个设置时光照贴图坐标索引现在是否指向正确的通道。确保设置为你在上述构建设置中所设置的通道。通常应该设置为 1。

在使用这些设置后，你现在应该具有正确的光照贴图分辨率了。

 

但这里也有一些注意事项，可能需要使用 Blender、3Ds Max 或 Maya 之类的建模程序来彻底更正该问题。

生成的光照贴图不会导致现有 UV 中来自纹理 UV 通道 1 的接缝断开。只会重新打包现有的 UV 布局，以更好地适应光照贴图 UV 的需要。

例如，可以想象一个圆柱体。如果要把这些面全部平铺展开，需要在圆柱体的侧面剪开一条线才可以。在建模程序中，这不是必需操作，具体取决于你是如何设置要使用的纹理 UV 的。如果切割这个侧面不是为了平铺展开，那么通过网格编辑器生成的 UV 就不起作用，但仍会在构建照明后引起重叠 UV 警告。 _________________________________________________________________________________________________

**如何使用静态照明控制全局光照？即反射的优点**

在使用静态照明时，需要构建照明来查看结果。光照系统用于编译和生成纹理，通过将场景的照明和阴影信息烘焙到光照贴图纹理，将该信息存储到纹理中。

默认情况下，光照系统设置为使用三次光线反射，以通过静态照明控制 GI。如果还需要进一步设置，需要通过“全局设置”选项卡直接更改光照系统设置来获得不同的结果。我们可以通过更改光线投射的反射次数来影响全局光照。

要启用“全局设置”选项卡，需要转至工具栏，选择“设置 > 全局设置”

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image151.jpg)](https://wiki.unrealengine.com/index.php?title=File:World_Settings_Toolbar.png)

全局设置

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image153.jpg)](https://wiki.unrealengine.com/index.php?title=File:LightmassSettings.png)

默认光照系统全局设置

单击右侧“细节”面板选项旁边的“全局设置”选项卡。

这里看到的很多设置都会影响通过光照系统处理照明的方式，从而直接影响场景。对于 GI，我们只会着重讲解第二个选项“间接光线反射次数”。该滑块的范围是 1 到 4。但只能通过手动输入值覆盖原有设置。

右侧显示的是默认设置。

·         **全局光照样本场景，单一点光源位于 250（≈ 15W 灯泡）**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image155.jpg)](https://wiki.unrealengine.com/index.php?title=File:Scene_Setup.PNG)

场景设置
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image157.jpg)](https://wiki.unrealengine.com/index.php?title=File:NumBounces0.png)

0 次反射
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image159.jpg)](https://wiki.unrealengine.com/index.php?title=File:NumBounces1.png)

1 次反射

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image161.jpg)](https://wiki.unrealengine.com/index.php?title=File:NumBounces2.png)

2 次反射
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image163.jpg)](https://wiki.unrealengine.com/index.php?title=File:NumBounces3.png)

3 次反射
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image157.jpg)](https://wiki.unrealengine.com/index.php?title=File:NumBounces4.png)

4 次反射

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image159.jpg)](https://wiki.unrealengine.com/index.php?title=File:NumBounces100.png)

100 次反射

**第一次反射的计算时间最长。后续反射对实际构建时间具有较小影响，但视觉影响也会大幅降低。**

 

[**想要进一步了解光照系统和全局光照？**](https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/Lightmass/index.html)

_________________________________________________________________________________________________

**为什么我的静态网格上有阴影斑点？或者如何清理这些不干净的光照贴图？**

在 UE4 中，无论使用哪种类型的静态照明，出现污渍、斑点、污垢等都是十分常见的问题。但不要担心，因为我们可以通过光照系统设置来清理这些不干净的光照贴图。

首先，看到类似效果的原因是光照系统构建时 GI 反射产生的间接照明导致的。

为了最有效地重现此问题，下面这个简单的场景有两个房间。

·         **样本场景**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image165.jpg)](https://wiki.unrealengine.com/index.php?title=File:1_sceneSetup.png)

外部
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image167.jpg)](https://wiki.unrealengine.com/index.php?title=File:2_sceneSetup.png)

内部

该场景将使用“制作”质量进行照明构建。该场景使用“起步内容”包中的资产，这些内容可以添加到任何新建的项目当中。场景中的所有网格都使用光照贴图分辨率 256，除非另有说明。后期处理效果设置为默认值且具有眼部适应设置，以便更容易看清较暗的房间。

构建照明后得出以下结果：

·         **初始照明构建，默认设置**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image169.jpg)](https://wiki.unrealengine.com/index.php?title=File:3_Room1_Clean.png)

第一个室内，直接照亮且有一次反射光
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image171.jpg)](https://wiki.unrealengine.com/index.php?title=File:4_Room2_dirty.png)

第二个室内，完全通过间接照明照亮

可以借助简单粗暴的方法消除部分间接照明失真，也就是提高光照贴图分辨率，这样实际上会增大用于存储照明和阴影信息的纹理大小，但这并不总是最好的做法，比如可以使用较低分辨率并调整光照系统设置来达到高质量结果。在引擎中处理任何渲染应用，尤其是照明会增大纹理大小的情况下，解决此问题的这种方法未必总是对性能最有利的方法，甚至可能导致在后面的开发过程中产生更多性能问题。

例如，下面是光照贴图分辨率更改为 1024 的上述第二个室内。

·         **初始照明构建，默认设置**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image171.jpg)](https://wiki.unrealengine.com/index.php?title=File:4_Room2_dirty.png)

第二个室内，光照贴图分辨率 256
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image173.jpg)](https://wiki.unrealengine.com/index.php?title=File:5_lightmap1024.png)

第二个室内，光照贴图分辨率 1024

在该示例中，通过使用较高的光照贴图分辨率大幅减少了失真，但这也导致纹理内存增加为原来的 4 倍。还有一种更有利于性能的解决方案来处理这些间接照明失真，即对“全局设置”进行简单调整。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image175.jpg)](https://wiki.unrealengine.com/index.php?title=File:7_World_Settings.png)

全局设置

·         您可以在该位置找到“全局设置”：

 

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image177.jpg)](https://wiki.unrealengine.com/index.php?title=File:6_LightmassSettings.png)

全局设置

·         这是可以调整的光照系统设置：

 

**间接照明质量**：这会增大全局光照解算器计数，为需要高质量的关卡提高质量。

**间接照明平滑度**：这是要应用于间接照明的平滑度因子。

警告：间接照明质量使用大于 1 的值会大幅增加构建时间。

·          

[![8 settings.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image179.jpg)](https://wiki.unrealengine.com/index.php?title=File:8_settings.png)

 

[![10 settings.png](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image181.jpg)](https://wiki.unrealengine.com/index.php?title=File:10_settings.png)

 

·         [

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image171.jpg)](https://wiki.unrealengine.com/index.php?title=File:9_results.png)

默认设置
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image183.jpg)](https://wiki.unrealengine.com/index.php?title=File:11_results.png)

示例设置 1

如上文“如何使用静态照明控制全局光照？即反射的优点”所述，你可能还想调整间接照明反射的次数来产生以下结果：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image185.jpg)](https://wiki.unrealengine.com/index.php?title=File:13_results.png)

间接照明反弹次数 = 4
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image171.jpg)](https://wiki.unrealengine.com/index.php?title=File:14_Results2.png)

间接照明反弹次数 = 5

至此，对照明设置的调整足以隐藏一些纹理的失真效果，但如果这种方法不可行，也可以将每个网格的光照贴图分辨率直接增大到较高值。这里使用的光照贴图分辨率是 256。如果更改为 512，将会获得如下结果：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image185.jpg)](https://wiki.unrealengine.com/index.php?title=File:15_FinalResult.png)

调整间接设置，512 光照贴图分辨率
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image186.jpg)](https://wiki.unrealengine.com/index.php?title=File:5_lightmap1024.png)

不调整间接设置，1024 光照贴图分辨率

在本教程开始时，显示了一个使用 1024 光照贴图消除失真的比较效果。通过调整几项光照系统设置，失真效果有所减少，资产使用较低纹理分辨率呈现出较好的结果。

虽然这种方法深入探索了不在房间里设置任何照明的选项，并寻找各种方法减少由于间接照明导致的“不干净”失真，但必须注意的是，在这些区域中使用照明，即使是密度极低的无阴影投射光线，也会产生一定的效果。以上所列的方法可以作为起点，可能需要经历一些试验和错误才能得到更理想的结果。

[想要进一步了解光照系统基本支持？](https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/Lightmass/Basics/index.html)

[想要进一步了解光照系统全局光照？](https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/Lightmass/index.html)

_________________________________________________________________________________________________

**左上角错误中的“需要重建照明”是什么意思？**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image188.jpg)](https://wiki.unrealengine.com/index.php?title=File:1_lighting_rebuilt.png)

错误消息

如果在使用 PIE（在编辑器中播放）、模拟或独立游戏时，视口左上角出现该错误，这只是表示需要为场景重建照明。这仅影响静态和静止照明。动态照亮的场景无需重建照明。

当照明因移动或修改照明 Actor 而导致失效时会产生此警告。这样会导致问题的原因是关卡中的渲染照明不能准确地表示关卡中当前的照明状态。要解决该错误，可以转至“构建”菜单并重建地图照明。

**故障排除技巧**

**未构建 Actor 列表**

有时会发现已经构建了照明，但仍会看到弹出该警告，指出有多个未构建的对象，但无法直接识别是哪些对象。

您可以从“开发者工具”菜单打开**输出日志**窗口。输入命令 **DumpUnbuiltLightInteractions** 就会显示一列没有构建照明或者照明失效的 Actor。

这一列 Actor 对于确定所发生的问题十分有用。可能只是因为某个蓝图设置为静态但包含可移动组件，也可能是因为某个 Actor 是通过构造脚本放置的，然后构建照明后被移到了其他位置。

**统计信息窗口**

转至“窗口 > 统计信息”可以打开**统计信息**窗口。该工具可以用于确定构建照明的信息以及场景中设置了光照贴图分辨率的所有静态网格的信息。要排查特定 Actor 在照明构建过程中构建照明所需的确切时间，该工具十分有用。如果感觉某些进程十分缓慢，该工具可以帮助轻松识别照明构建时间较长的有问题对象。

 

_________________________________________________________________________________________________

**照明质量比较，或制作 > 预览**

当需要为某个关卡构建照明时，可以转至工具栏中的“构建 > 照明质量”并选择质量级别来设置光照贴图的照明构建质量。

默认情况下，该质量设置为**预览**。该设置具有最快的计算时间，而**制作**的计算时间最慢，但准确性要高得多。

“照明质量”设置位于以下位置：

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image190.jpg)](https://wiki.unrealengine.com/index.php?title=File:2_BuildOptions.png)

照明质量设置

在以下演示中，用了一个封闭的房间显示所构建阴影的质量：（该场景与[#为什么我的静态网格上有阴影斑点？或者如何清理这些不干净的光照贴图？](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E4.B8.BA.E4.BB.80.E4.B9.88.E6.88.91.E7.9A.84.E9.9D.99.E6.80.81.E7.BD.91.E6.A0.BC.E4.B8.8A.E6.9C.89.E9.98.B4.E5.BD.B1.E6.96.91.E7.82.B9.EF.BC.9F.E6.88.96.E8.80.85.E5.A6.82.E4.BD.95.E6.B8.85.E7.90.86.E8.BF.99.E4.BA.9B.E4.B8.8D.E5.B9.B2.E5.87.80.E7.9A.84.E5.85.89.E7.85.A7.E8.B4.B4.E5.9B.BE.EF.BC.9F)所用的场景设置一样

·         **照明质量设置，建筑**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image192.jpg)](https://wiki.unrealengine.com/index.php?title=File:3_Preview.png)

预览
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image192.jpg)](https://wiki.unrealengine.com/index.php?title=File:4_Medium.png)

中
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image194.jpg)](https://wiki.unrealengine.com/index.php?title=File:5_High.png)

高

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image192.jpg)](https://wiki.unrealengine.com/index.php?title=File:6_Production.png)

制作

在该示例中，很容易看出默认的“预览”设置和“制作”设置的差异。在“制作”设置中，在前面几种质量设置中普遍存在的所有漏光现象几乎全部消失。这是发生漏光时排查照明问题的好方法。如果“制作”没有消除漏光问题，则需要查看光照贴图 UV 的设置方式，甚至可能需要检查关卡中的网格布局。

在以下场景中，雕塑静态网格的阴影质量调整并不明显。质量上有轻微的差异，但这个具体的对象不足明显地显示出来。

·         **照明质量设置，有机线条**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image192.jpg)](https://wiki.unrealengine.com/index.php?title=File:7_statue_preview.png)

预览
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image194.jpg)](https://wiki.unrealengine.com/index.php?title=File:8_statue_Medium.png)

中
  

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image192.jpg)](https://wiki.unrealengine.com/index.php?title=File:9_Statue_High.png)

高

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image194.jpg)](https://wiki.unrealengine.com/index.php?title=File:10_Statue_Production.png)

制作

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image196.jpg)](https://wiki.unrealengine.com/index.php?title=File:11_StatueQuality.gif)

雕塑照明质量

在该动画 Gif 中，质量差异相较于该预览是极其细微的。较为有机的形状应该也是这种行为。如果颜色和亮度相同，人眼会先注意到非有机直线（例如建筑直角），然后才会注意到弯曲或更有机的形状。需要注意的是，平坦地面上的阴影粗糙度是较大网格采用较低光照贴图分辨率所导致的结果。提高光照贴图分辨率会改善阴影定义的质量。

 

 

_________________________________________________________________________________________________

**光照贴图错误颜色**

选择“使用错误颜色”并使用“预览”或“中”照明质量设置时，通过“构建菜单”下拉按钮可以启用该选项。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image198.jpg)](https://wiki.unrealengine.com/index.php?title=File:LightingErrorColoring.png)

错误颜色选项

当光照系统遇到错误时，会用颜色表示错误类型，方便用户识别。以下是针对所遇到问题反映出的颜色类型。

·         橙色：因非唯一或重叠 UV 导致的。

·         绿色：因环绕 UV 或 UV 超出了 0,1 UV 空间范围导致的。

·         黄色：这是没有贴图的纹理元素，它们或者没有光照贴图区域，或者光照贴图分辨率过低（如果是 BSP）。

您可以在仍然适用的 UE3 文档中查看更多信息： <https://udn.epicgames.com/Three/LightmassTools.html#Lightmap> error colors

_________________________________________________________________________________________________

**查找“需要重建照明（X 个对象）”中引用的对象**

有时，可能会遇到照明总是无效的问题，或者你可能调整了关卡中的某些设置，但没有意识到因此而导致了令人沮丧的“需要重建照明（[数量] 个对象）”，但却不能轻松识别这 [数量] 个对象都是什么。

幸运的是，我们为你提供了一种简单的方法来获取此信息，帮助你更有效地跟踪、调查和解决照明无效的问题。

·         首先转至“窗口 > 开发者工具 > 输出日志”以打开“输出日志”窗口。

·         使用 `（波浪符）键，输入命令 **DumpUnbuiltLightInteractions** 来打开控制台

那么这种方法作用在哪呢？

·         你可以快速识别导致出现该警告的 Actor。

·         所构建的某个 Actor 是静态的，然后使用代码或蓝图进行了移动，从而导致出现该警告。

·         使用大量实例和高光照贴图分辨率实例化的网格可能没有正确构建，因为没有生成集群实例光照贴图。这表示需要降低光照贴图分辨率。

·         在某些情况下，使用构造脚本通过蓝图生成网格位置时，如果之前构建了照明，那么移动网格会导致照明失效。该命令也可以快速识别这种情况。

_________________________________________________________________________________________________

**照明构建统计信息**

编辑器中提供的“统计信息”窗口是在光照构建完成后查看关卡统计信息的好方法。该窗口可以提供有用的统计信息，帮助缩小场景中耗时最长的 Actor 的范围，计算该 Actor 的照明所耗用的时间及其光照贴图分辨率。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image200.jpg)](https://wiki.unrealengine.com/index.php?title=File:StatisticsWindow.png)

统计信息窗口

*该窗口取自 Epic Games 启动程序“学习”选项卡中提供的 Sun Temple 照明构建。*

照明构建信息和静态网格照明信息中包含的所有信息都有助于优化、调查和排查照明构建。

也可以在下列文档中找到该信息：<https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/Lightmass/#gettingthebestlightingbuildtimes>

 

_________________________________________________________________________________________________

**景观草类资产平铺图案**

你或许没有注意到，景观草类资产中有一个隐藏的小功能。此功能允许使用景观光照贴图，通过引用间接照明缓存样本，对过程景观草类材质获得更好的融合效果。

你可以选中“使用景观光照贴图”复选框来启用该功能。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image202.jpg)](https://wiki.unrealengine.com/index.php?title=File:LandscapeGrassTypeSettings.png)

景观草类设置

该功能最初是为了动态照亮环境而开发的，但在使用静止或静态照亮环境时，会发现此类环境的图案是根据景观间接照明的平铺组件生成的，效果非常分散。

·         **景观草类使用景观光照贴图**

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image204.jpg)](https://wiki.unrealengine.com/index.php?title=File:LandscapeGrassType1.png)

禁用

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image206.jpg)](https://wiki.unrealengine.com/index.php?title=File:LandscapeGrassType2.png)

启用

启用或禁用“使用景观光照贴图”选项后，材质会重新生成，而无需重构照明，前提是之前已经构建好了照明。

_________________________________________________________________________________________________

**通过命令行构建照明**

如果需要通过命令行构建照明，该功能从 4.10.2 开始已经添加到引擎中。

要使用命令行构建照明，请使用以下结构进行设置以作为基础：

·         UE4-Editor.exe [Project Folder Path] -run=resavepackages -buildlighting -MapsOnly -ProjectOnly -AllowCommandletRendering -Map=[Name of map]

如果想要构建项目中所有可用的地图/关卡，可以删除 -Map=[Map Name]。

在以下 GitHub 提交版本中可以找到更多详细信息：<https://github.com/EpicGames/UnrealEngine/commit/f89256dd0efb7d0b1427729a8f8a6007>

如果看到 404 错误页面，需要确保你有 GitHub 帐户，并且 Epic 帐户已经与 GitHub 帐户关联起来。

 

_________________________________________________________________________________________________

**植物叶子工具光照贴图分辨率**

使用植物叶子工具时，工具面板中有一些不同的设置可供所选 Actor 使用。一个重要的设置是覆盖网格光照贴图分辨率的选项。

[

![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image208.jpg)](https://wiki.unrealengine.com/index.php?title=File:FoliageLightmap.png)

植物叶子光照贴图设置

该选项默认是禁用的，表示将使用静态网格自己的光照贴图分辨率。

你可能会疑惑“这样有什么不好？我不就是希望正常烘焙的阴影有一个良好的光照贴图分辨率吗？”但问题是使用植物叶子工具时，它们不再是独自放置并具有自己的光照贴图的 Actor。它们是聚集在一起的实例，而这些集群会一起烘焙到单一光照贴图中。

如果你有大量实例，并继续以静态网格默认光照贴图分辨率进行构建，很可能会遇到警告“Instanced_Foliage_Actor_[X] 光照贴图过大，应缩小。”该警告明确表示光照贴图分辨率过高。应该启用上述选项，尝试更低的分辨率，比如 8 或 4，然后再继续重建。

但一种较为普遍的合理做法是执行下列操作：

·         如果希望树木/草丛随风摆动，限制静态照明在植物叶子上的使用。植物叶子摆动时看起来不自然，但阴影则不会。

·         将植物叶子的光照贴图分辨率降低至可以处理的大小。

·         禁用草上的静态照明。这是较为普遍的合理做法，因为随着关卡的发展，实例数量很可能会达到数千个，在大多数情况下会显著增加光照构建时间。

 

来自 <[*https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E9.97.B4.E6.8E.A5.E7.85.A7.E6.98.8E.E7.9A.84.E9.98.B4.E5.BD.B1.E6.8E.A5.E7.BC.9D.2F.E6.98.8E.E6.9A.97.E5.B7.AE.E5.BC.82*](https://wiki.unrealengine.com/%E4%B8%AD%E6%96%87_%E5%85%89%E7%85%A7%E7%9A%84%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3#.E9.97.B4.E6.8E.A5.E7.85.A7.E6.98.8E.E7.9A.84.E9.98.B4.E5.BD.B1.E6.8E.A5.E7.BC.9D.2F.E6.98.8E.E6.9A.97.E5.B7.AE.E5.BC.82)> 

 

 

UE Build error C4577: 'noexcept'

2019年1月30日

23:02

 

getting the following build error when trying to package game:

C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\VC\Tools\MSVC\14.14.26428\INCLUDE\vcruntime_new.h(67):

error C4577: 'noexcept' used with no exception handling mode specified; termination on exception is not guaranteed. Specify /EHsc

 

Solved:

 

add the following to your build.cs file:

 

Definitions.Add("BOOST_SYSTEM_NOEXCEPT");

So that Boost will not insert "noexcept" everywhere, that way you don't have to force enable exceptions for all modules.

 

I made it work by editing [ProjectName].Target.cs in the directory above. Adding bForceEnableExceptions = true; there fixed my build so I could use exceptions.

 

What I did was added:

bEnableExceptions =true;

Into the Build file for that module only when building for windows. This fixed the build. 

 

来自 <[*https://avi.iteye.com/blog/2424122*](https://avi.iteye.com/blog/2424122)> 
