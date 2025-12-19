#!/usr/bin/env python3
"""
中国招标网爬虫脚本
从 https://chinabidding.com.cn/search 爬取招标信息
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
import csv
import argparse
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlencode


class ChinaBiddingScraper:
    """中国招标网爬虫类"""

    BASE_URL = "https://chinabidding.com.cn"
    SEARCH_URL = "https://chinabidding.com.cn/search"

    # 模拟浏览器请求头
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://chinabidding.com.cn/",
        "Cache-Control": "max-age=0",
    }

    def __init__(self, delay: float = 1.0):
        """
        初始化爬虫

        Args:
            delay: 请求间隔时间（秒），避免被封IP
        """
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.delay = delay

    def _random_delay(self):
        """随机延迟，模拟人类行为"""
        time.sleep(self.delay + random.uniform(0.5, 1.5))

    def _make_request(self, url: str, params: dict = None, retries: int = 3) -> Optional[requests.Response]:
        """
        发送HTTP请求，带重试机制

        Args:
            url: 请求URL
            params: 查询参数
            retries: 重试次数

        Returns:
            Response对象或None
        """
        for attempt in range(retries):
            try:
                self._random_delay()
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"请求失败 (尝试 {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
        return None

    def search(self, keyword: str = "", page: int = 1, **kwargs) -> Dict:
        """
        搜索招标信息

        Args:
            keyword: 搜索关键词
            page: 页码
            **kwargs: 其他搜索参数（如 area, type, date_from, date_to 等）

        Returns:
            包含搜索结果的字典
        """
        params = {
            "keyword": keyword,
            "page": page,
            **kwargs
        }

        response = self._make_request(self.SEARCH_URL, params=params)
        if not response:
            return {"success": False, "error": "请求失败", "data": []}

        return self._parse_search_results(response.text)

    def _parse_search_results(self, html: str) -> Dict:
        """
        解析搜索结果页面

        Args:
            html: HTML内容

        Returns:
            解析后的数据字典
        """
        soup = BeautifulSoup(html, "html.parser")
        results = []

        # 常见的招标网站结果列表选择器（按优先级尝试）
        selectors = [
            ".search-result-list li",
            ".list-item",
            ".result-item",
            ".bid-list li",
            ".news-list li",
            "table.list tbody tr",
            ".content-list .item",
            "ul.list li",
        ]

        items = []
        for selector in selectors:
            items = soup.select(selector)
            if items:
                break

        # 如果没找到列表项，尝试通用解析
        if not items:
            items = soup.find_all(["li", "tr", "div"], class_=lambda x: x and ("item" in x.lower() or "list" in x.lower()))

        for item in items:
            try:
                record = self._extract_item_data(item)
                if record.get("title"):  # 只添加有标题的记录
                    results.append(record)
            except Exception as e:
                print(f"解析条目失败: {e}")
                continue

        # 提取分页信息
        pagination = self._extract_pagination(soup)

        return {
            "success": True,
            "total_pages": pagination.get("total_pages", 1),
            "current_page": pagination.get("current_page", 1),
            "total_count": pagination.get("total_count", len(results)),
            "data": results,
            "raw_html_length": len(html)
        }

    def _extract_item_data(self, item) -> Dict:
        """
        从单个列表项中提取数据

        Args:
            item: BeautifulSoup元素

        Returns:
            提取的数据字典
        """
        data = {}

        # 提取标题和链接
        title_elem = item.find(["a", "h2", "h3", "h4", ".title", "span"])
        if title_elem:
            data["title"] = title_elem.get_text(strip=True)
            if title_elem.name == "a":
                data["url"] = urljoin(self.BASE_URL, title_elem.get("href", ""))
            else:
                link = item.find("a")
                if link:
                    data["url"] = urljoin(self.BASE_URL, link.get("href", ""))

        # 提取日期
        date_patterns = ["date", "time", "publish", "发布"]
        for pattern in date_patterns:
            date_elem = item.find(class_=lambda x: x and pattern in str(x).lower())
            if date_elem:
                data["date"] = date_elem.get_text(strip=True)
                break

        if "date" not in data:
            # 尝试从文本中提取日期
            text = item.get_text()
            import re
            date_match = re.search(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}", text)
            if date_match:
                data["date"] = date_match.group()

        # 提取地区
        area_patterns = ["area", "region", "province", "city", "地区", "省份"]
        for pattern in area_patterns:
            area_elem = item.find(class_=lambda x: x and pattern in str(x).lower())
            if area_elem:
                data["area"] = area_elem.get_text(strip=True)
                break

        # 提取类型/分类
        type_patterns = ["type", "category", "class", "类型", "分类"]
        for pattern in type_patterns:
            type_elem = item.find(class_=lambda x: x and pattern in str(x).lower())
            if type_elem:
                data["type"] = type_elem.get_text(strip=True)
                break

        # 提取金额
        amount_patterns = ["amount", "price", "money", "金额", "预算"]
        for pattern in amount_patterns:
            amount_elem = item.find(class_=lambda x: x and pattern in str(x).lower())
            if amount_elem:
                data["amount"] = amount_elem.get_text(strip=True)
                break

        # 提取采购单位/发布单位
        org_patterns = ["org", "company", "unit", "单位", "采购人"]
        for pattern in org_patterns:
            org_elem = item.find(class_=lambda x: x and pattern in str(x).lower())
            if org_elem:
                data["organization"] = org_elem.get_text(strip=True)
                break

        # 提取摘要/描述
        desc_patterns = ["desc", "summary", "content", "摘要", "内容"]
        for pattern in desc_patterns:
            desc_elem = item.find(class_=lambda x: x and pattern in str(x).lower())
            if desc_elem:
                data["description"] = desc_elem.get_text(strip=True)[:500]  # 限制长度
                break

        return data

    def _extract_pagination(self, soup) -> Dict:
        """提取分页信息"""
        pagination = {}

        # 尝试找分页元素
        pager = soup.find(class_=lambda x: x and ("page" in str(x).lower() or "pager" in str(x).lower()))
        if pager:
            # 提取总页数
            last_page = pager.find_all("a")
            if last_page:
                for link in reversed(last_page):
                    text = link.get_text(strip=True)
                    if text.isdigit():
                        pagination["total_pages"] = int(text)
                        break

            # 提取当前页
            current = pager.find(class_=lambda x: x and ("active" in str(x).lower() or "current" in str(x).lower()))
            if current:
                text = current.get_text(strip=True)
                if text.isdigit():
                    pagination["current_page"] = int(text)

        # 尝试提取总条数
        total_elem = soup.find(string=lambda x: x and ("共" in str(x) or "总计" in str(x) or "条" in str(x)))
        if total_elem:
            import re
            match = re.search(r"(\d+)\s*条", str(total_elem))
            if match:
                pagination["total_count"] = int(match.group(1))

        return pagination

    def get_detail(self, url: str) -> Dict:
        """
        获取招标详情页

        Args:
            url: 详情页URL

        Returns:
            详情数据字典
        """
        response = self._make_request(url)
        if not response:
            return {"success": False, "error": "请求失败"}

        soup = BeautifulSoup(response.text, "html.parser")

        data = {"url": url}

        # 提取标题
        title = soup.find(["h1", "h2", ".title", ".article-title"])
        if title:
            data["title"] = title.get_text(strip=True)

        # 提取正文内容
        content = soup.find(class_=lambda x: x and ("content" in str(x).lower() or "article" in str(x).lower()))
        if content:
            data["content"] = content.get_text(strip=True)

        # 提取附件
        attachments = []
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            if any(ext in href.lower() for ext in [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar"]):
                attachments.append({
                    "name": link.get_text(strip=True),
                    "url": urljoin(self.BASE_URL, href)
                })
        if attachments:
            data["attachments"] = attachments

        return {"success": True, "data": data}

    def scrape_all_pages(self, keyword: str = "", max_pages: int = 10, **kwargs) -> List[Dict]:
        """
        爬取多页结果

        Args:
            keyword: 搜索关键词
            max_pages: 最大爬取页数
            **kwargs: 其他搜索参数

        Returns:
            所有结果列表
        """
        all_results = []

        for page in range(1, max_pages + 1):
            print(f"正在爬取第 {page} 页...")
            result = self.search(keyword=keyword, page=page, **kwargs)

            if not result["success"] or not result["data"]:
                print(f"第 {page} 页无数据，停止爬取")
                break

            all_results.extend(result["data"])
            print(f"  获取 {len(result['data'])} 条记录")

            # 检查是否到达最后一页
            if page >= result.get("total_pages", 1):
                print("已到达最后一页")
                break

        return all_results

    def export_to_csv(self, data: List[Dict], filename: str):
        """
        导出数据到CSV文件

        Args:
            data: 数据列表
            filename: 输出文件名
        """
        if not data:
            print("没有数据可导出")
            return

        # 获取所有字段
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = sorted(list(fieldnames))

        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"数据已导出到 {filename}")

    def export_to_json(self, data: List[Dict], filename: str):
        """
        导出数据到JSON文件

        Args:
            data: 数据列表
            filename: 输出文件名
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"数据已导出到 {filename}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="中国招标网爬虫")
    parser.add_argument("-k", "--keyword", default="", help="搜索关键词")
    parser.add_argument("-p", "--pages", type=int, default=5, help="爬取页数 (默认: 5)")
    parser.add_argument("-d", "--delay", type=float, default=1.0, help="请求间隔秒数 (默认: 1.0)")
    parser.add_argument("-o", "--output", default="bidding_results", help="输出文件名 (不含扩展名)")
    parser.add_argument("-f", "--format", choices=["csv", "json", "both"], default="both", help="输出格式")
    parser.add_argument("--area", help="地区筛选")
    parser.add_argument("--type", help="类型筛选")

    args = parser.parse_args()

    print("=" * 50)
    print("中国招标网爬虫")
    print("=" * 50)
    print(f"关键词: {args.keyword or '(无)'}")
    print(f"页数: {args.pages}")
    print(f"请求间隔: {args.delay}秒")
    print("=" * 50)

    # 创建爬虫实例
    scraper = ChinaBiddingScraper(delay=args.delay)

    # 构建额外参数
    extra_params = {}
    if args.area:
        extra_params["area"] = args.area
    if args.type:
        extra_params["type"] = args.type

    # 爬取数据
    results = scraper.scrape_all_pages(
        keyword=args.keyword,
        max_pages=args.pages,
        **extra_params
    )

    print("=" * 50)
    print(f"共获取 {len(results)} 条记录")

    if results:
        # 导出数据
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{args.output}_{timestamp}"

        if args.format in ["csv", "both"]:
            scraper.export_to_csv(results, f"{base_filename}.csv")

        if args.format in ["json", "both"]:
            scraper.export_to_json(results, f"{base_filename}.json")

        # 打印前几条结果预览
        print("\n结果预览 (前3条):")
        print("-" * 50)
        for i, item in enumerate(results[:3], 1):
            print(f"\n{i}. {item.get('title', 'N/A')}")
            for key, value in item.items():
                if key != "title":
                    print(f"   {key}: {value}")
    else:
        print("未获取到数据。可能原因：")
        print("1. 网站有反爬虫机制，需要使用代理或Selenium")
        print("2. 网页结构已更改，需要更新解析逻辑")
        print("3. 关键词没有匹配结果")


if __name__ == "__main__":
    main()
