# 导入岗位指南（jobs 文件）

工具不抓取平台（合规考虑）。你把看中的岗位**整理成一个文件**，工具就能排序 + 生成草稿。
两种格式任选其一：

- `jobs.template.json` —— 程序友好，适合直接编辑
- `jobs.template.csv` —— 可用 Excel/WPS 打开填写（你 Excel 精通，推荐）

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | ✅ | 岗位名称 |
| `company` | 建议 | 公司名称 |
| `location` | 建议 | 城市（用于地点加分） |
| `description` | ✅✅ | **职位描述/JD 正文**，匹配主要看这里，**粘得越全越准** |
| `source` | 可选 | 来源平台：BOSS直聘 / 智联招聘 / 前程无忧 / 猎聘 / LinkedIn… |
| `salary` | 可选 | 薪资范围，如 `25-40K` |
| `url` | 可选 | 岗位链接，方便你回去投递 |
| `id` | 可选 | 不填会自动生成 |

> CSV 里若 `description` 含逗号，请用英文双引号把整段括起来（模板里已示范）。

## 怎么填

1. 在 BOSS直聘 / 智联 / LinkedIn 上看到合适岗位；
2. 把**岗位名、公司、城市、JD 正文**复制到一行（JD 直接整段粘进 `description`）；
3. 存成 `jobs.json` 或 `jobs.csv`。

## 用法

```bash
# 排序 + 写入追踪库
python -m job_assistant match --resume 你的简历.pdf --name 樊宇 --jobs jobs.json --top 10 --save

# 给最匹配的岗位生成草稿（审核后你亲自去平台发）
python -m job_assistant draft --resume 你的简历.pdf --name 樊宇 --jobs jobs.json --rank 1 --style greeting
```

## 关于"自动从平台拉取"

- **国内平台（BOSS直聘 / 智联 / 前程无忧 / 猎聘 / 拉勾）**：没有面向个人/第三方的公开岗位搜索 API，自动抓取违反其服务条款且易封号。**最实际的合规方式就是上面的手动导入**（你浏览 → 粘贴 → 工具排序/草稿）。
- **海外**：Adzuna 提供免费官方 API，可半自动拉取（见项目根 `README.md` 的 Adzuna 用法）；覆盖 gb/us/au/ca/de/fr/in/sg 等，**不含中国大陆**。
