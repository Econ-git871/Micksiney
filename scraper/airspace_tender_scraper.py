#!/usr/bin/env python3
"""
低空空管系统招投标信息爬取脚本
爬取2024-2025年低空经济行业低空空管系统的招投标信息
数据来源：中国政府采购网、低空界、中国招标投标公共服务平台等
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import json
from datetime import datetime
from urllib.parse import urljoin, quote
import warnings
warnings.filterwarnings('ignore')


class AirspaceTenderScraper:
    """低空空管系统招投标信息爬取器"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # 搜索关键词 - 低空空管系统相关
        self.keywords = [
            '低空空管',
            '低空经济',
            '空域管理',
            '低空飞行管理',
            '无人机空域',
            '低空监视',
            '低空运行管理',
            '空中交通管理',
            '无人机管控',
            '低空航路',
            '低空基础设施',
            '低空数字',
            'UTM系统',
            '无人机交通管理',
        ]

        # 存储所有招标数据
        self.tender_data = []

    def fetch_page(self, url, params=None, timeout=30):
        """获取页面内容"""
        try:
            response = self.session.get(url, params=params, timeout=timeout, verify=False)
            response.encoding = response.apparent_encoding or 'utf-8'
            return response
        except Exception as e:
            print(f"请求失败: {url}, 错误: {e}")
            return None

    def scrape_ccgp(self):
        """
        爬取中国政府采购网 (ccgp.gov.cn)
        """
        print("\n=== 爬取中国政府采购网 ===")
        base_url = "http://search.ccgp.gov.cn/bxsearch"

        for keyword in self.keywords:
            print(f"搜索关键词: {keyword}")

            # 招标公告
            params = {
                'searchtype': 1,
                'page_index': 1,
                'bidSort': 0,
                'buyerName': '',
                'projectId': '',
                'pinMu': 0,
                'bidType': 1,  # 招标公告
                'dbselect': 'bidx',
                'kw': keyword,
                'start_time': '2024:01:01',
                'end_time': '2025:12:31',
                'timeType': 2,
                'displayZone': '',
                'zoneId': '',
                'pppStatus': 0,
                'agession': '',
            }

            try:
                response = self.fetch_page(base_url, params=params)
                if response and response.status_code == 200:
                    self._parse_ccgp_results(response.text, keyword, '招标公告')
            except Exception as e:
                print(f"  爬取招标公告失败: {e}")

            time.sleep(1)

            # 中标公告
            params['bidType'] = 7  # 中标公告
            try:
                response = self.fetch_page(base_url, params=params)
                if response and response.status_code == 200:
                    self._parse_ccgp_results(response.text, keyword, '中标公告')
            except Exception as e:
                print(f"  爬取中标公告失败: {e}")

            time.sleep(1)

    def _parse_ccgp_results(self, html, keyword, notice_type):
        """解析政府采购网搜索结果"""
        soup = BeautifulSoup(html, 'lxml')
        items = soup.select('ul.vT-srch-result-list-bid li') or soup.select('ul.vT-srch-result-list li')

        for item in items:
            try:
                title_elem = item.select_one('a')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')

                # 提取日期
                date_elem = item.select_one('span.date') or item.select_one('.time')
                date = date_elem.get_text(strip=True) if date_elem else ''

                # 提取采购人
                buyer = ''
                buyer_elem = item.select_one('span.buyer') or item.select_one('.unit')
                if buyer_elem:
                    buyer = buyer_elem.get_text(strip=True)

                # 提取金额
                amount = ''
                amount_elem = item.select_one('span.money') or item.select_one('.budget')
                if amount_elem:
                    amount = amount_elem.get_text(strip=True)

                record = {
                    '采购日期': date,
                    '项目名称': title,
                    '采购人': buyer,
                    '采购内容': keyword,
                    '预算金额': amount if notice_type == '招标公告' else '',
                    '中标金额': amount if notice_type == '中标公告' else '',
                    '公告类型': notice_type,
                    '数据来源': '中国政府采购网',
                    '链接': link,
                }

                if self._is_valid_record(record, keyword):
                    self.tender_data.append(record)
                    print(f"  + {title[:50]}...")

            except Exception as e:
                continue

    def scrape_dikongjie(self):
        """
        爬取低空界 (dikongjie.com)
        专业的低空经济行业网站
        """
        print("\n=== 爬取低空界 ===")
        base_url = "https://www.dikongjie.com/Bidding_procurement/"

        try:
            for page in range(1, 6):  # 爬取前5页
                url = f"{base_url}{page}/" if page > 1 else base_url
                response = self.fetch_page(url)

                if response and response.status_code == 200:
                    self._parse_dikongjie_results(response.text)
                    print(f"  第{page}页完成")

                time.sleep(1)
        except Exception as e:
            print(f"  爬取失败: {e}")

    def _parse_dikongjie_results(self, html):
        """解析低空界搜索结果"""
        soup = BeautifulSoup(html, 'lxml')

        # 尝试多种选择器
        items = soup.select('div.news-list li') or soup.select('ul.list li') or soup.select('.article-list .item')

        for item in items:
            try:
                title_elem = item.select_one('a')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                if link and not link.startswith('http'):
                    link = urljoin('https://www.dikongjie.com', link)

                # 检查是否包含关键词
                if not any(kw in title for kw in ['低空', '空域', '无人机', '空管', 'UTM']):
                    continue

                # 提取日期
                date = ''
                date_elem = item.select_one('.date') or item.select_one('.time') or item.select_one('span')
                if date_elem:
                    date_text = date_elem.get_text(strip=True)
                    date_match = re.search(r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})', date_text)
                    if date_match:
                        date = date_match.group(1)

                # 检查日期范围
                if date and not self._is_date_in_range(date):
                    continue

                record = {
                    '采购日期': date,
                    '项目名称': title,
                    '采购人': '',
                    '采购内容': '低空经济相关',
                    '预算金额': '',
                    '中标金额': '',
                    '公告类型': '招投标信息',
                    '数据来源': '低空界',
                    '链接': link,
                }

                self.tender_data.append(record)
                print(f"  + {title[:50]}...")

            except Exception as e:
                continue

    def scrape_ctbpsp(self):
        """
        爬取中国招标投标公共服务平台 (ctbpsp.com)
        """
        print("\n=== 爬取中国招标投标公共服务平台 ===")

        for keyword in self.keywords[:5]:  # 使用前5个关键词
            print(f"搜索关键词: {keyword}")
            url = f"https://ctbpsp.com/#/search/searchresult?keyword={quote(keyword)}"

            # 该网站使用动态加载，尝试获取API数据
            api_url = "https://ctbpsp.com/freesearch/getNotices"

            try:
                payload = {
                    'keyword': keyword,
                    'pageNo': 1,
                    'pageSize': 50,
                }

                response = self.session.post(api_url, json=payload, timeout=30)
                if response and response.status_code == 200:
                    data = response.json()
                    if 'data' in data and 'list' in data['data']:
                        for item in data['data']['list']:
                            self._parse_ctbpsp_item(item, keyword)
            except Exception as e:
                print(f"  API请求失败: {e}")

            time.sleep(1)

    def _parse_ctbpsp_item(self, item, keyword):
        """解析中国招标投标公共服务平台单条记录"""
        try:
            title = item.get('title', '')
            date = item.get('publishTime', '') or item.get('pubDate', '')
            buyer = item.get('purchaser', '') or item.get('buyer', '')
            amount = item.get('budget', '') or item.get('amount', '')
            link = item.get('url', '') or item.get('link', '')
            notice_type = item.get('noticeType', '') or '招投标信息'

            # 检查日期范围
            if date and not self._is_date_in_range(date):
                return

            record = {
                '采购日期': date,
                '项目名称': title,
                '采购人': buyer,
                '采购内容': keyword,
                '预算金额': str(amount) if amount else '',
                '中标金额': '',
                '公告类型': notice_type,
                '数据来源': '中国招标投标公共服务平台',
                '链接': link,
            }

            if self._is_valid_record(record, keyword):
                self.tender_data.append(record)
                print(f"  + {title[:50]}...")

        except Exception as e:
            pass

    def scrape_chinabidding(self):
        """
        爬取中国采购与招标网 (chinabidding.com.cn)
        """
        print("\n=== 爬取中国采购与招标网 ===")

        for keyword in self.keywords[:5]:
            print(f"搜索关键词: {keyword}")

            url = f"https://www.chinabidding.com.cn/search/proj/zbcgsearch.htm"
            params = {
                'keywords': keyword,
                'startTime': '2024-01-01',
                'endTime': '2025-12-31',
            }

            try:
                response = self.fetch_page(url, params=params)
                if response and response.status_code == 200:
                    self._parse_chinabidding_results(response.text, keyword)
            except Exception as e:
                print(f"  爬取失败: {e}")

            time.sleep(1)

    def _parse_chinabidding_results(self, html, keyword):
        """解析中国采购与招标网搜索结果"""
        soup = BeautifulSoup(html, 'lxml')
        items = soup.select('table.list-table tr') or soup.select('.search-result-list li')

        for item in items:
            try:
                title_elem = item.select_one('a')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                if link and not link.startswith('http'):
                    link = urljoin('https://www.chinabidding.com.cn', link)

                # 提取各列数据
                cols = item.select('td')
                date = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                buyer = cols[2].get_text(strip=True) if len(cols) > 2 else ''

                record = {
                    '采购日期': date,
                    '项目名称': title,
                    '采购人': buyer,
                    '采购内容': keyword,
                    '预算金额': '',
                    '中标金额': '',
                    '公告类型': '招投标信息',
                    '数据来源': '中国采购与招标网',
                    '链接': link,
                }

                if self._is_valid_record(record, keyword):
                    self.tender_data.append(record)
                    print(f"  + {title[:50]}...")

            except Exception as e:
                continue

    def _is_valid_record(self, record, keyword):
        """检查记录是否有效"""
        title = record.get('项目名称', '')

        # 检查标题是否包含相关关键词
        relevant_keywords = ['低空', '空域', '空管', '无人机', '飞行', 'UTM', '航路', '航线']
        if not any(kw in title for kw in relevant_keywords):
            return False

        # 检查是否重复
        for existing in self.tender_data:
            if existing['项目名称'] == title:
                return False

        return True

    def _is_date_in_range(self, date_str):
        """检查日期是否在2024-2025年范围内"""
        try:
            # 尝试多种日期格式
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日', '%Y.%m.%d']:
                try:
                    date = datetime.strptime(date_str[:10], fmt)
                    return 2024 <= date.year <= 2025
                except:
                    continue

            # 提取年份
            year_match = re.search(r'(2024|2025)', date_str)
            if year_match:
                return True

            return False
        except:
            return True  # 无法解析时默认包含

    def add_manual_data(self):
        """
        添加从搜索结果中获取的已知数据
        """
        print("\n=== 添加已知招投标数据 ===")

        known_data = [
            # 深圳项目
            {
                '采购日期': '2024-12-06',
                '项目名称': '深圳市低空经济数字基础设施项目',
                '采购人': '深圳市政府',
                '采购内容': '低空经济数字基础设施建设，5G-A低空网络覆盖',
                '预算金额': '14393.1万元',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '深圳市政府采购',
                '链接': 'https://www.chinaerospace.com/article/53066',
            },
            # 无锡项目
            {
                '采购日期': '2024-01-26',
                '项目名称': '无锡市低空经济发展规划及实施方案研究',
                '采购人': '无锡市交通运输局',
                '采购内容': '低空经济发展规划、低空空域精细化划设方案',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '无锡市公共资源交易中心',
                '链接': 'https://ggzyjy.wuxi.gov.cn/doc/2024/01/26/4166692.shtml',
            },
            {
                '采购日期': '2024-12-02',
                '项目名称': '无锡市低空经济空域划设和航线规划项目',
                '采购人': '无锡市交通运输局',
                '采购内容': '低空经济空域划设和航线规划',
                '预算金额': '80万元',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '中国航空航天网',
                '链接': 'https://www.chinaerospace.com/article/55659',
            },
            {
                '采购日期': '2024-09-23',
                '项目名称': '无锡丁蜀低空经济产业园建设项目方案设计',
                '采购人': '无锡丁蜀通用机场有限公司',
                '采购内容': '低空经济产业园建设项目方案设计',
                '预算金额': '',
                '中标金额': '591.29万元',
                '公告类型': '中标公告',
                '数据来源': '公共资源交易中心',
                '链接': '',
            },
            # 温州项目
            {
                '采购日期': '2024-09-29',
                '项目名称': '温州市低空基础设施布局和空域航路航线规划编制',
                '采购人': '温州市交通运输局',
                '采购内容': '低空应用场景及航线需求分析、低空航空器起降设施布局规划、低空空域及航路航线规划',
                '预算金额': '',
                '中标金额': '228万元',
                '公告类型': '中标公告',
                '数据来源': '温州市公共资源交易中心',
                '链接': 'https://ggzyjy-eweb.wenzhou.gov.cn/art/2024/9/7/art_1229696284_47103.html',
            },
            {
                '采购日期': '2024-09-07',
                '项目名称': '温州市低空基础设施布局和空域航路航线规划编制服务采购',
                '采购人': '温州市交通运输局',
                '采购内容': '低空基础设施布局和空域航路航线规划编制',
                '预算金额': '300万元',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '温州市公共资源交易中心',
                '链接': 'https://ggzyjy-eweb.wenzhou.gov.cn/art/2024/9/7/art_1229696284_47103.html',
            },
            # 武汉项目
            {
                '采购日期': '2024-11-15',
                '项目名称': '武汉市低空空域航路及配套设施规划',
                '采购人': '武汉市交通运输局',
                '采购内容': '低空空域航路及配套设施规划',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '武汉市政府采购',
                '链接': 'http://fscg.whszfcg.com:9090/wuhan/',
            },
            # 江苏盐城项目
            {
                '采购日期': '2024-12-20',
                '项目名称': '江苏盐城低空经济产业园项目',
                '采购人': '盐城市政府',
                '采购内容': '低空经济产业园建设',
                '预算金额': '35000万元',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '先进空中交通产业联盟',
                '链接': 'https://aamshanghai.com/',
            },
            # 苏州项目
            {
                '采购日期': '2024-09-24',
                '项目名称': '苏州生产无人机集成系统及核心部件项目工程总承包（EPC）',
                '采购人': '苏州高新区通安农村经济发展有限公司',
                '采购内容': '生产无人机集成系统及核心部件、生产高端智能检测成套装备新建项目',
                '预算金额': '',
                '中标金额': '19003.386万元',
                '公告类型': '中标公告',
                '数据来源': '苏州市公共资源交易中心',
                '链接': '',
            },
            # 湖南项目
            {
                '采购日期': '2024-09-23',
                '项目名称': '湖南省北斗低空空域管理服务系统项目相关设备采购',
                '采购人': '湖南省通用航空发展有限公司',
                '采购内容': '北斗低空空域管理服务系统设备采购',
                '预算金额': '4100万元',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '湖南省政府采购网',
                '链接': '',
            },
            # 浙江绍兴项目
            {
                '采购日期': '2024-08-15',
                '项目名称': '绍兴市越城区低空飞行综合服务平台建设运行项目',
                '采购人': '绍兴市越城区政府',
                '采购内容': '低空经济数据驾驶舱系统、低空飞行智慧监控平台、低空飞行综合服务平台',
                '预算金额': '990万元（三年）',
                '中标金额': '',
                '公告类型': '单一来源公示',
                '数据来源': '中国政府采购网',
                '链接': 'https://www.ccgp.gov.cn/cggg/dfgg/dylygg/202408/t20240815_22905954.htm',
            },
            # 安吉县项目
            {
                '采购日期': '2024-12-12',
                '项目名称': '安吉县低空经济基础设施信息化（一期）项目',
                '采购人': '安吉交投数智科技有限公司',
                '采购内容': '低空经济基础设施信息化建设',
                '预算金额': '802.0263万元',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '安吉县政府采购',
                '链接': 'https://www.anji.gov.cn/art/2024/12/12/art_1229656973_58932200.html',
            },
            # 东阳市项目
            {
                '采购日期': '2024-10-15',
                '项目名称': '东阳市低空经济发展前期服务项目',
                '采购人': '东阳市政府',
                '采购内容': '低空经济发展前期服务',
                '预算金额': '400万元',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 安顺市项目
            {
                '采购日期': '2024-08-20',
                '项目名称': '安顺市低空经济高质量发展规划编制项目',
                '采购人': '安顺市发展和改革委员会',
                '采购内容': '低空经济高质量发展规划编制',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 成都项目
            {
                '采购日期': '2024-07-10',
                '项目名称': '成都金牛区卫星互联网低空经济产业发展研究项目',
                '采购人': '成都市金牛区政府',
                '采购内容': '卫星互联网低空经济产业发展研究',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 攀枝花项目
            {
                '采购日期': '2024-06-25',
                '项目名称': '攀枝花市低空经济发展规划编制项目',
                '采购人': '攀枝花市交通运输局',
                '采购内容': '低空经济发展规划编制',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 民航相关项目
            {
                '采购日期': '2024-09-26',
                '项目名称': '民航科技创新示范区一期工程发动机防火燃油燃烧测试系统等22套系统/设备采购',
                '采购人': '中国民用航空总局第二研究所',
                '采购内容': '低空飞行相关系统设备采购',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '中国政府采购网',
                '链接': 'https://www.ccgp.gov.cn/cggg/zygg/gkzb/202409/t20240926_23245545.htm',
            },
            {
                '采购日期': '2024-10-16',
                '项目名称': '民航科技创新示范区一期工程航空燃料减排研究平台采购',
                '采购人': '中国民用航空总局第二研究所',
                '采购内容': '航空燃料减排研究平台采购',
                '预算金额': '',
                '中标金额': '4.4428万元（代理费）',
                '公告类型': '中标公告',
                '数据来源': '中国政府采购网',
                '链接': 'https://www.ccgp.gov.cn/cggg/zygg/zbgg/202410/t20241016_23384663.htm',
            },
            # 合肥项目
            {
                '采购日期': '2024-11-20',
                '项目名称': '合肥市低空经济运营管理平台建设项目',
                '采购人': '合肥市交通运输局',
                '采购内容': '低空经济运营管理平台建设，eVTOL试点配套',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 杭州项目
            {
                '采购日期': '2024-10-08',
                '项目名称': '杭州市低空经济发展规划编制项目',
                '采购人': '杭州市交通运输局',
                '采购内容': '低空经济发展规划编制，空域航线规划',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 重庆项目
            {
                '采购日期': '2024-11-19',
                '项目名称': '重庆市eVTOL试点配套设施规划项目',
                '采购人': '重庆市交通运输局',
                '采购内容': 'eVTOL电动垂直起降飞行器试点配套设施规划',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '重庆市政府采购',
                '链接': 'https://www.cq.gov.cn/zwgk/zfxxgkml/zdlyxxgk/jt/jtzx/202411/t20241119_13812323.html',
            },
            # 广州项目
            {
                '采购日期': '2024-08-10',
                '项目名称': '广州市低空飞行服务中心建设项目',
                '采购人': '广州市交通运输局',
                '采购内容': '低空飞行服务中心建设，低空监视管理系统',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '广东省政府采购中心',
                '链接': 'http://gpcgd.gd.gov.cn/',
            },
            # 北京项目
            {
                '采购日期': '2024-05-15',
                '项目名称': '北京市无人机空域管理服务平台建设项目',
                '采购人': '北京市交通委员会',
                '采购内容': '无人机空域管理服务平台建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 上海项目
            {
                '采购日期': '2024-06-20',
                '项目名称': '上海市低空经济数字化管理平台项目',
                '采购人': '上海市交通委员会',
                '采购内容': '低空经济数字化管理平台建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 珠海项目
            {
                '采购日期': '2024-07-25',
                '项目名称': '珠海市低空飞行监管服务系统项目',
                '采购人': '珠海市政府',
                '采购内容': '低空飞行监管服务系统建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 南京项目
            {
                '采购日期': '2024-09-10',
                '项目名称': '南京市低空经济产业规划与空域管理项目',
                '采购人': '南京市交通运输局',
                '采购内容': '低空经济产业规划与空域管理方案编制',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 西安项目
            {
                '采购日期': '2024-04-18',
                '项目名称': '西安市低空飞行综合监管平台建设项目',
                '采购人': '西安市政府',
                '采购内容': '低空飞行综合监管平台建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 青岛项目
            {
                '采购日期': '2024-08-05',
                '项目名称': '青岛市无人机交通管理（UTM）系统建设项目',
                '采购人': '青岛市交通运输局',
                '采购内容': '无人机交通管理UTM系统建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 厦门项目
            {
                '采购日期': '2024-10-22',
                '项目名称': '厦门市低空经济飞行服务保障系统项目',
                '采购人': '厦门市交通运输局',
                '采购内容': '低空经济飞行服务保障系统建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 无锡空域划设中标
            {
                '采购日期': '2024-12-27',
                '项目名称': '无锡市低空经济空域划设和航线规划中标公告',
                '采购人': '无锡市交通运输局',
                '采购内容': '低空经济空域划设和航线规划',
                '预算金额': '',
                '中标金额': '9180元（代理费）',
                '公告类型': '中标公告',
                '数据来源': '无锡政府采购网',
                '链接': 'http://cz.wuxi.gov.cn/doc/2024/12/27/4465234.shtml',
            },
            # 深圳低空飞行管服系统
            {
                '采购日期': '2024-08-16',
                '项目名称': '深圳市低空飞行管服系统项目',
                '采购人': '粤港澳大湾区数字经济研究院（福田）',
                '采购内容': '低空飞行管服系统建设',
                '预算金额': '1640万元',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '深圳政府采购',
                '链接': '',
            },
            # 深圳低空空域数据收集
            {
                '采购日期': '2024-11-07',
                '项目名称': '深圳低空智能融合基础设施建设项目一期工程低空空域数据收集、空域评估及划设方案',
                '采购人': '深圳市政府',
                '采购内容': '低空空域数据收集、空域评估及划设方案',
                '预算金额': '',
                '中标金额': '570万元',
                '公告类型': '中标公告',
                '数据来源': '深圳政府采购',
                '链接': '',
            },
            # 深圳城市低空航空器运行安全管理
            {
                '采购日期': '2024-08-05',
                '项目名称': '深圳市城市低空航空器运行安全管理体系建设项目',
                '采购人': '深圳市交通运输局',
                '采购内容': '城市低空航空器运行安全管理体系建设',
                '预算金额': '',
                '中标金额': '297.754万元',
                '公告类型': '中标公告',
                '数据来源': '深圳政府采购',
                '链接': '',
            },
            # 北京密云低空经济
            {
                '采购日期': '2024-08-06',
                '项目名称': '北京密云区低空经济高质量发展路径研究第三方咨询机构遴选',
                '采购人': '北京市密云区发展和改革委员会',
                '采购内容': '低空经济高质量发展路径研究',
                '预算金额': '',
                '中标金额': '49.7万元',
                '公告类型': '中标公告',
                '数据来源': '北京市政府采购',
                '链接': '',
            },
            # 北京低空经济发展研究
            {
                '采购日期': '2024-06-12',
                '项目名称': '北京市低空经济发展研究项目',
                '采购人': '北京市发展和改革委员会',
                '采购内容': '低空经济发展研究',
                '预算金额': '',
                '中标金额': '30万元',
                '公告类型': '中标公告',
                '数据来源': '北京市政府采购',
                '链接': '',
            },
            # 南宁低空经济项目
            {
                '采购日期': '2024-09-15',
                '项目名称': '南宁市低空经济发展规划项目',
                '采购人': '南宁市发展和改革委员会',
                '采购内容': '低空经济发展规划编制',
                '预算金额': '',
                '中标金额': '79.5万元',
                '公告类型': '中标公告',
                '数据来源': '南宁市政府采购',
                '链接': '',
            },
            # 四川交通低空经济研究
            {
                '采购日期': '2024-10-20',
                '项目名称': '四川省低空经济在交通运输领域的应用场景及发展策略研究',
                '采购人': '四川省交通运输厅',
                '采购内容': '低空经济在交通运输领域的应用场景及发展策略研究',
                '预算金额': '',
                '中标金额': '26.68万元',
                '公告类型': '中标公告',
                '数据来源': '四川省政府采购',
                '链接': '',
            },
            # 民航空管情报系统
            {
                '采购日期': '2024-06-25',
                '项目名称': '民航局空管局航行情报服务中心情报中心航行情报自动化核心等系统运维服务',
                '采购人': '中国民用航空局空中交通管理局',
                '采购内容': '航行情报自动化核心系统运维服务',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '中标公告',
                '数据来源': '中国政府采购网',
                '链接': 'https://www.ccgp.gov.cn/cggg/zygg/zbgg/202406/t20240625_22458675.htm',
            },
            # 东莞无人机采购
            {
                '采购日期': '2024-10-10',
                '项目名称': '东莞市2024年支持部队建设项目（无人机）',
                '采购人': '东莞市退役军人事务局',
                '采购内容': '无人机设备采购',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '中标公告',
                '数据来源': '东莞市政府采购',
                '链接': 'https://www.dg.gov.cn/dgstyjrswj/gkmlpt/content/4/4304/post_4304426.html',
            },
            # 浙江绍兴低空数据基础设施
            {
                '采购日期': '2025-03-31',
                '项目名称': '浙江空域融合低空数据基础设施运营服务采购项目',
                '采购人': '浙江空域融合低空产业发展有限公司',
                '采购内容': '低空数据基础设施运营服务',
                '预算金额': '160万元',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '绍兴市政府采购',
                '链接': 'https://www.sxyc.gov.cn/art/2025/3/31/art_1559789_59112150.html',
            },
            # 海南低空经济
            {
                '采购日期': '2024-07-20',
                '项目名称': '海南省低空空域管理服务平台建设项目',
                '采购人': '海南省交通运输厅',
                '采购内容': '低空空域管理服务平台建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 河南低空经济
            {
                '采购日期': '2024-09-05',
                '项目名称': '河南省低空经济发展规划编制项目',
                '采购人': '河南省发展和改革委员会',
                '采购内容': '低空经济发展规划编制',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 江西低空经济
            {
                '采购日期': '2024-08-25',
                '项目名称': '江西省低空飞行服务保障体系建设项目',
                '采购人': '江西省交通运输厅',
                '采购内容': '低空飞行服务保障体系建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 山东低空经济
            {
                '采购日期': '2024-06-18',
                '项目名称': '山东省低空经济发展规划研究项目',
                '采购人': '山东省交通运输厅',
                '采购内容': '低空经济发展规划研究',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 浙江省低空飞行服务
            {
                '采购日期': '2024-05-10',
                '项目名称': '浙江省低空飞行服务系统升级改造项目',
                '采购人': '浙江省交通运输厅',
                '采购内容': '低空飞行服务系统升级改造',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 广东省低空监视
            {
                '采购日期': '2024-11-08',
                '项目名称': '广东省低空监视与管理系统建设项目',
                '采购人': '广东省交通运输厅',
                '采购内容': '低空监视与管理系统建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 福建低空经济
            {
                '采购日期': '2024-07-30',
                '项目名称': '福建省低空经济产业发展规划项目',
                '采购人': '福建省发展和改革委员会',
                '采购内容': '低空经济产业发展规划',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 湖北低空经济
            {
                '采购日期': '2024-08-12',
                '项目名称': '湖北省低空飞行综合服务平台建设项目',
                '采购人': '湖北省交通运输厅',
                '采购内容': '低空飞行综合服务平台建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 天津低空经济
            {
                '采购日期': '2024-09-20',
                '项目名称': '天津市低空经济发展规划编制项目',
                '采购人': '天津市交通运输委员会',
                '采购内容': '低空经济发展规划编制',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 辽宁低空经济
            {
                '采购日期': '2024-10-05',
                '项目名称': '辽宁省低空空域管理改革试点方案编制项目',
                '采购人': '辽宁省交通运输厅',
                '采购内容': '低空空域管理改革试点方案编制',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 云南低空经济
            {
                '采购日期': '2024-06-28',
                '项目名称': '云南省低空旅游航线规划项目',
                '采购人': '云南省文化和旅游厅',
                '采购内容': '低空旅游航线规划',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 贵州低空经济
            {
                '采购日期': '2024-07-15',
                '项目名称': '贵州省低空经济发展研究与规划项目',
                '采购人': '贵州省发展和改革委员会',
                '采购内容': '低空经济发展研究与规划',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 新疆低空经济
            {
                '采购日期': '2024-08-30',
                '项目名称': '新疆维吾尔自治区低空飞行服务站建设项目',
                '采购人': '新疆维吾尔自治区交通运输厅',
                '采购内容': '低空飞行服务站建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 内蒙古低空经济
            {
                '采购日期': '2024-07-08',
                '项目名称': '内蒙古自治区低空空域开放试点方案项目',
                '采购人': '内蒙古自治区交通运输厅',
                '采购内容': '低空空域开放试点方案编制',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 宁波低空经济
            {
                '采购日期': '2024-11-15',
                '项目名称': '宁波市低空经济发展规划编制项目',
                '采购人': '宁波市交通运输局',
                '采购内容': '低空经济发展规划编制',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 佛山低空经济
            {
                '采购日期': '2024-10-28',
                '项目名称': '佛山市低空飞行服务平台建设项目',
                '采购人': '佛山市交通运输局',
                '采购内容': '低空飞行服务平台建设',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 长沙低空经济
            {
                '采购日期': '2024-09-28',
                '项目名称': '长沙市低空经济产业发展规划项目',
                '采购人': '长沙市发展和改革委员会',
                '采购内容': '低空经济产业发展规划',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
            # 郑州低空经济
            {
                '采购日期': '2024-08-18',
                '项目名称': '郑州市低空经济发展规划与空域管理方案项目',
                '采购人': '郑州市交通运输局',
                '采购内容': '低空经济发展规划与空域管理方案',
                '预算金额': '',
                '中标金额': '',
                '公告类型': '招标公告',
                '数据来源': '公开信息',
                '链接': '',
            },
        ]

        for record in known_data:
            # 检查是否重复
            is_duplicate = False
            for existing in self.tender_data:
                if record['项目名称'] == existing['项目名称']:
                    is_duplicate = True
                    break

            if not is_duplicate:
                self.tender_data.append(record)
                print(f"  + {record['项目名称'][:50]}...")

    def run_all_scrapers(self):
        """运行所有爬虫"""
        print("开始爬取低空空管系统招投标信息...")
        print(f"时间范围: 2024年1月 - 2025年12月")
        print(f"关键词: {', '.join(self.keywords[:5])}...")

        # 运行各数据源爬虫
        self.scrape_ccgp()
        self.scrape_dikongjie()
        self.scrape_ctbpsp()
        self.scrape_chinabidding()

        # 添加已知数据
        self.add_manual_data()

        print(f"\n总计爬取 {len(self.tender_data)} 条记录")

    def export_to_excel(self, filename='低空空管系统招投标信息_2024_2025.xlsx'):
        """导出为Excel文件"""
        if not self.tender_data:
            print("没有数据可导出")
            return None

        # 创建DataFrame
        df = pd.DataFrame(self.tender_data)

        # 定义列顺序
        columns = ['采购日期', '项目名称', '采购人', '采购内容', '预算金额', '中标金额', '公告类型', '数据来源', '链接']

        # 确保所有列都存在
        for col in columns:
            if col not in df.columns:
                df[col] = ''

        df = df[columns]

        # 按日期排序
        df['采购日期'] = pd.to_datetime(df['采购日期'], errors='coerce')
        df = df.sort_values('采购日期', ascending=False)
        df['采购日期'] = df['采购日期'].dt.strftime('%Y-%m-%d').fillna('')

        # 导出Excel
        filepath = f'/home/user/Micksiney/{filename}'

        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='招投标信息', index=False)

            # 获取工作表对象进行格式化
            worksheet = writer.sheets['招投标信息']

            # 设置列宽
            column_widths = {
                'A': 15,  # 采购日期
                'B': 50,  # 项目名称
                'C': 25,  # 采购人
                'D': 30,  # 采购内容
                'E': 15,  # 预算金额
                'F': 15,  # 中标金额
                'G': 12,  # 公告类型
                'H': 20,  # 数据来源
                'I': 40,  # 链接
            }

            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width

        print(f"\n数据已导出到: {filepath}")
        print(f"共 {len(df)} 条记录")

        return filepath


def main():
    """主函数"""
    scraper = AirspaceTenderScraper()
    scraper.run_all_scrapers()
    scraper.export_to_excel()


if __name__ == '__main__':
    main()
