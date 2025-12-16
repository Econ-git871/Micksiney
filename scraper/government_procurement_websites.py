#!/usr/bin/env python3
"""
中国各级政府采购网站清单
包括：国家级、省级、副省级城市、地级市、县区级
"""

# ============================================================
# 一、国家级政府采购平台
# ============================================================
NATIONAL_PLATFORMS = {
    '中国政府采购网': {
        'url': 'https://www.ccgp.gov.cn/',
        'search_url': 'http://search.ccgp.gov.cn/bxsearch',
        'description': '财政部唯一指定政府采购信息网络发布媒体',
        'level': '国家级',
    },
    '全国公共资源交易平台': {
        'url': 'https://www.ggzy.gov.cn/',
        'search_url': 'https://deal.ggzy.gov.cn/ds/deal/dealList.jsp',
        'description': '全国公共资源交易信息汇总平台',
        'level': '国家级',
    },
    '中央政府采购网': {
        'url': 'https://www.zycg.gov.cn/',
        'description': '中央国家机关政府采购中心',
        'level': '国家级',
    },
    '中国招标投标公共服务平台': {
        'url': 'https://www.cebpubservice.com/',
        'search_url': 'https://ctbpsp.com/',
        'description': '全国招标公告公示搜索引擎',
        'level': '国家级',
    },
    '中国采购与招标网': {
        'url': 'https://www.chinabidding.com.cn/',
        'description': '综合性招投标信息平台',
        'level': '国家级',
    },
    '军队采购网': {
        'url': 'https://www.plap.mil.cn/',
        'description': '中国人民解放军采购平台',
        'level': '国家级',
    },
}

# ============================================================
# 二、省级（31个省/自治区/直辖市）政府采购网
# ============================================================
PROVINCIAL_PLATFORMS = {
    # 直辖市 (4个)
    '北京市': {
        '政府采购网': 'http://www.ccgp-beijing.gov.cn/',
        '公共资源交易': 'https://ggzyfw.beijing.gov.cn/',
    },
    '天津市': {
        '政府采购网': 'http://www.ccgp-tianjin.gov.cn/',
        '公共资源交易': 'http://ggzy.zwfwb.tj.gov.cn/',
    },
    '上海市': {
        '政府采购网': 'http://www.ccgp-shanghai.gov.cn/',
        '公共资源交易': 'https://www.shggzy.com/',
    },
    '重庆市': {
        '政府采购网': 'http://www.ccgp-chongqing.gov.cn/',
        '公共资源交易': 'https://www.cqggzy.com/',
    },

    # 华北地区
    '河北省': {
        '政府采购网': 'http://www.ccgp-hebei.gov.cn/',
        '公共资源交易': 'http://www.hebpr.cn/',
    },
    '山西省': {
        '政府采购网': 'http://www.ccgp-shanxi.gov.cn/',
        '公共资源交易': 'https://prec.sxzwfw.gov.cn/',
    },
    '内蒙古自治区': {
        '政府采购网': 'http://www.ccgp-neimenggu.gov.cn/',
        '公共资源交易': 'http://ggzyjy.nmg.gov.cn/',
    },

    # 东北地区
    '辽宁省': {
        '政府采购网': 'http://www.ccgp-liaoning.gov.cn/',
        '公共资源交易': 'http://www.lnggzy.gov.cn/',
    },
    '吉林省': {
        '政府采购网': 'http://www.ccgp-jilin.gov.cn/',
        '公共资源交易': 'http://ggzyjy.jl.gov.cn/',
    },
    '黑龙江省': {
        '政府采购网': 'http://www.hljcg.gov.cn/',
        '公共资源交易': 'https://hljggzyjyw.hlj.gov.cn/',
    },

    # 华东地区
    '江苏省': {
        '政府采购网': 'http://www.ccgp-jiangsu.gov.cn/',
        '公共资源交易': 'http://jsggzy.jszwfw.gov.cn/',
    },
    '浙江省': {
        '政府采购网': 'http://www.ccgp-zhejiang.gov.cn/',
        '公共资源交易': 'http://www.zjpubservice.com/',
    },
    '安徽省': {
        '政府采购网': 'http://www.ccgp-anhui.gov.cn/',
        '公共资源交易': 'http://ggzy.ah.gov.cn/',
    },
    '福建省': {
        '政府采购网': 'http://www.ccgp-fujian.gov.cn/',
        '公共资源交易': 'https://ggzyfw.fujian.gov.cn/',
    },
    '江西省': {
        '政府采购网': 'http://www.ccgp-jiangxi.gov.cn/',
        '公共资源交易': 'http://jxsggzy.cn/',
    },
    '山东省': {
        '政府采购网': 'http://www.ccgp-shandong.gov.cn/',
        '公共资源交易': 'http://ggzyjy.shandong.gov.cn/',
    },

    # 华中地区
    '河南省': {
        '政府采购网': 'http://www.ccgp-henan.gov.cn/',
        '公共资源交易': 'https://ggzy.fgw.henan.gov.cn/',
    },
    '湖北省': {
        '政府采购网': 'http://www.ccgp-hubei.gov.cn/',
        '公共资源交易': 'http://www.hbggzyfwpt.cn/',
    },
    '湖南省': {
        '政府采购网': 'http://www.ccgp-hunan.gov.cn/',
        '公共资源交易': 'http://ggzy.hunan.gov.cn/',
    },

    # 华南地区
    '广东省': {
        '政府采购网': 'http://www.ccgp-guangdong.gov.cn/',
        '政府采购中心': 'http://gpcgd.gd.gov.cn/',
        '公共资源交易': 'http://bs.gdggzy.org.cn/',
    },
    '广西壮族自治区': {
        '政府采购网': 'http://www.ccgp-guangxi.gov.cn/',
        '公共资源交易': 'http://gxggzy.gxzf.gov.cn/',
    },
    '海南省': {
        '政府采购网': 'https://ccgp-hainan.gov.cn/',
        '公共资源交易': 'http://ggzy.hainan.gov.cn/',
    },

    # 西南地区
    '四川省': {
        '政府采购网': 'http://www.ccgp-sichuan.gov.cn/',
        '公共资源交易': 'http://ggzyjy.sc.gov.cn/',
    },
    '贵州省': {
        '政府采购网': 'http://www.ccgp-guizhou.gov.cn/',
        '公共资源交易': 'http://ggzy.guizhou.gov.cn/',
    },
    '云南省': {
        '政府采购网': 'http://www.ccgp-yunnan.gov.cn/',
        '公共资源交易': 'https://ggzy.yn.gov.cn/',
    },
    '西藏自治区': {
        '政府采购网': 'http://www.ccgp-xizang.gov.cn/',
        '公共资源交易': 'http://www.xzggzy.gov.cn/',
    },

    # 西北地区
    '陕西省': {
        '政府采购网': 'http://www.ccgp-shaanxi.gov.cn/',
        '公共资源交易': 'http://www.sxggzyjy.cn/',
    },
    '甘肃省': {
        '政府采购网': 'http://www.ccgp-gansu.gov.cn/',
        '公共资源交易': 'http://ggzy.gansu.gov.cn/',
    },
    '青海省': {
        '政府采购网': 'http://www.ccgp-qinghai.gov.cn/',
        '公共资源交易': 'http://ggzy.qinghai.gov.cn/',
    },
    '宁夏回族自治区': {
        '政府采购网': 'http://www.ccgp-ningxia.gov.cn/',
        '公共资源交易': 'http://www.nxggzyjy.org/',
    },
    '新疆维吾尔自治区': {
        '政府采购网': 'http://www.ccgp-xinjiang.gov.cn/',
        '公共资源交易': 'http://ggzy.xinjiang.gov.cn/',
    },
}

# ============================================================
# 三、副省级城市（15个）及计划单列市政府采购网
# ============================================================
SUB_PROVINCIAL_CITIES = {
    # 5个计划单列市
    '深圳市': {
        '政府采购网': 'https://zfcg.sz.gov.cn/',
        '公共资源交易': 'https://www.szggzy.com/',
        '类型': '计划单列市',
    },
    '大连市': {
        '政府采购网': 'http://www.ccgp-dalian.gov.cn/',
        '公共资源交易': 'http://ggzy.dl.gov.cn/',
        '类型': '计划单列市',
    },
    '青岛市': {
        '政府采购网': 'http://www.ccgp-qingdao.gov.cn/',
        '公共资源交易': 'http://ggzyjy.qingdao.gov.cn/',
        '类型': '计划单列市',
    },
    '宁波市': {
        '政府采购网': 'http://www.ccgp-ningbo.gov.cn/',
        '公共资源交易': 'http://ggzy.ningbo.gov.cn/',
        '类型': '计划单列市',
    },
    '厦门市': {
        '政府采购网': 'http://www.ccgp-xiamen.gov.cn/',
        '公共资源交易': 'https://ggzy.xm.gov.cn/',
        '类型': '计划单列市',
    },

    # 10个副省级省会城市
    '广州市': {
        '政府采购网': 'http://www.ccgp-guangzhou.gov.cn/',
        '公共资源交易': 'http://www.gzggzy.cn/',
        '类型': '副省级省会',
    },
    '武汉市': {
        '政府采购网': 'http://www.whzfcg.gov.cn/',
        '公共资源交易': 'http://ggzy.wuhan.gov.cn/',
        '类型': '副省级省会',
    },
    '南京市': {
        '政府采购网': 'http://czj.nanjing.gov.cn/ggcg/',
        '公共资源交易': 'http://ggzy.nanjing.gov.cn/',
        '类型': '副省级省会',
    },
    '成都市': {
        '政府采购网': 'http://www.cdgpb.chengdu.gov.cn/',
        '公共资源交易': 'http://www.cdggzy.com/',
        '类型': '副省级省会',
    },
    '杭州市': {
        '政府采购网': 'http://cz.hangzhou.gov.cn/col/col811644/',
        '公共资源交易': 'http://hzctc.hangzhou.gov.cn/',
        '类型': '副省级省会',
    },
    '西安市': {
        '政府采购网': 'http://zfcg.xa.gov.cn/',
        '公共资源交易': 'http://ggzy.xa.gov.cn/',
        '类型': '副省级省会',
    },
    '济南市': {
        '政府采购网': 'http://cz.jinan.gov.cn/col/col29938/',
        '公共资源交易': 'http://jnggzy.jinan.gov.cn/',
        '类型': '副省级省会',
    },
    '沈阳市': {
        '政府采购网': 'http://www.ccgp-shenyang.gov.cn/',
        '公共资源交易': 'http://ggzy.shenyang.gov.cn/',
        '类型': '副省级省会',
    },
    '长春市': {
        '政府采购网': 'http://zfcg.changchun.gov.cn/',
        '公共资源交易': 'http://ggzyjy.changchun.gov.cn/',
        '类型': '副省级省会',
    },
    '哈尔滨市': {
        '政府采购网': 'http://www.hrbcg.gov.cn/',
        '公共资源交易': 'http://ggzy.harbin.gov.cn/',
        '类型': '副省级省会',
    },
}

# ============================================================
# 四、重点地级市政府采购网（经济发达城市）
# ============================================================
MAJOR_PREFECTURE_CITIES = {
    # 江苏省
    '苏州市': {
        '政府采购网': 'http://www.szzfcg.cn/',
        '公共资源交易': 'http://ggzy.suzhou.gov.cn/',
        '省份': '江苏省',
    },
    '无锡市': {
        '政府采购网': 'http://cz.wuxi.gov.cn/',
        '公共资源交易': 'https://ggzyjy.wuxi.gov.cn/',
        '省份': '江苏省',
    },
    '常州市': {
        '政府采购网': 'http://czj.changzhou.gov.cn/',
        '公共资源交易': 'http://ggzyjy.changzhou.gov.cn/',
        '省份': '江苏省',
    },
    '南通市': {
        '政府采购网': 'http://zfcg.nantong.gov.cn/',
        '公共资源交易': 'http://ggzy.nantong.gov.cn/',
        '省份': '江苏省',
    },
    '徐州市': {
        '政府采购网': 'http://www.xzzfcg.gov.cn/',
        '公共资源交易': 'http://ggzyjy.xz.gov.cn/',
        '省份': '江苏省',
    },

    # 浙江省
    '温州市': {
        '政府采购网': 'http://cz.wenzhou.gov.cn/',
        '公共资源交易': 'https://ggzyjy-eweb.wenzhou.gov.cn/',
        '省份': '浙江省',
    },
    '绍兴市': {
        '政府采购网': 'http://zfcg.sx.gov.cn/',
        '公共资源交易': 'http://ggzy.sx.gov.cn/',
        '省份': '浙江省',
    },
    '嘉兴市': {
        '政府采购网': 'http://zfcg.jiaxing.gov.cn/',
        '公共资源交易': 'http://ggzy.jiaxing.gov.cn/',
        '省份': '浙江省',
    },
    '金华市': {
        '政府采购网': 'http://cz.jinhua.gov.cn/',
        '公共资源交易': 'http://ggzy.jinhua.gov.cn/',
        '省份': '浙江省',
    },
    '台州市': {
        '政府采购网': 'http://zfcg.taizhou.gov.cn/',
        '公共资源交易': 'http://ggzy.taizhou.gov.cn/',
        '省份': '浙江省',
    },

    # 广东省
    '佛山市': {
        '政府采购网': 'http://www.fszfcg.gov.cn/',
        '公共资源交易': 'http://ggzy.foshan.gov.cn/',
        '省份': '广东省',
    },
    '东莞市': {
        '政府采购网': 'http://dgzfcg.dg.gov.cn/',
        '公共资源交易': 'http://ggzy.dg.gov.cn/',
        '省份': '广东省',
    },
    '珠海市': {
        '政府采购网': 'http://zfcg.zhuhai.gov.cn/',
        '公共资源交易': 'http://ggzy.zhuhai.gov.cn/',
        '省份': '广东省',
    },
    '中山市': {
        '政府采购网': 'http://zfcg.zs.gov.cn/',
        '公共资源交易': 'http://ggzy.zs.gov.cn/',
        '省份': '广东省',
    },
    '惠州市': {
        '政府采购网': 'http://zfcg.huizhou.gov.cn/',
        '公共资源交易': 'http://ggzy.huizhou.gov.cn/',
        '省份': '广东省',
    },

    # 山东省
    '烟台市': {
        '政府采购网': 'http://zfcg.yantai.gov.cn/',
        '公共资源交易': 'http://ggzy.yantai.gov.cn/',
        '省份': '山东省',
    },
    '潍坊市': {
        '政府采购网': 'http://zfcg.weifang.gov.cn/',
        '公共资源交易': 'http://ggzy.weifang.gov.cn/',
        '省份': '山东省',
    },
    '临沂市': {
        '政府采购网': 'http://zfcg.linyi.gov.cn/',
        '公共资源交易': 'http://ggzy.linyi.gov.cn/',
        '省份': '山东省',
    },

    # 四川省
    '绵阳市': {
        '政府采购网': 'http://zfcg.my.gov.cn/',
        '公共资源交易': 'http://ggzy.my.gov.cn/',
        '省份': '四川省',
    },
    '德阳市': {
        '政府采购网': 'http://cz.deyang.gov.cn/',
        '公共资源交易': 'http://ggzy.deyang.gov.cn/',
        '省份': '四川省',
    },

    # 湖北省
    '宜昌市': {
        '政府采购网': 'http://zfcg.yichang.gov.cn/',
        '公共资源交易': 'http://ggzy.yichang.gov.cn/',
        '省份': '湖北省',
    },
    '襄阳市': {
        '政府采购网': 'http://zfcg.xiangyang.gov.cn/',
        '公共资源交易': 'http://ggzy.xiangyang.gov.cn/',
        '省份': '湖北省',
    },

    # 湖南省
    '长沙市': {
        '政府采购网': 'http://zfcg.changsha.gov.cn/',
        '公共资源交易': 'http://ggzy.changsha.gov.cn/',
        '省份': '湖南省',
    },
    '株洲市': {
        '政府采购网': 'http://zfcg.zhuzhou.gov.cn/',
        '公共资源交易': 'http://ggzy.zhuzhou.gov.cn/',
        '省份': '湖南省',
    },

    # 河南省
    '郑州市': {
        '政府采购网': 'http://www.zzzfcg.gov.cn/',
        '公共资源交易': 'http://ggzy.zhengzhou.gov.cn/',
        '省份': '河南省',
    },
    '洛阳市': {
        '政府采购网': 'http://zfcg.ly.gov.cn/',
        '公共资源交易': 'http://ggzy.ly.gov.cn/',
        '省份': '河南省',
    },

    # 安徽省
    '合肥市': {
        '政府采购网': 'http://zfcg.hefei.gov.cn/',
        '公共资源交易': 'http://ggzy.hefei.gov.cn/',
        '省份': '安徽省',
    },
    '芜湖市': {
        '政府采购网': 'http://zfcg.wuhu.gov.cn/',
        '公共资源交易': 'http://ggzy.wuhu.gov.cn/',
        '省份': '安徽省',
    },

    # 福建省
    '泉州市': {
        '政府采购网': 'http://zfcg.quanzhou.gov.cn/',
        '公共资源交易': 'http://ggzy.quanzhou.gov.cn/',
        '省份': '福建省',
    },
    '漳州市': {
        '政府采购网': 'http://zfcg.zhangzhou.gov.cn/',
        '公共资源交易': 'http://ggzy.zhangzhou.gov.cn/',
        '省份': '福建省',
    },

    # 江西省
    '南昌市': {
        '政府采购网': 'http://zfcg.nc.gov.cn/',
        '公共资源交易': 'http://ggzy.nc.gov.cn/',
        '省份': '江西省',
    },

    # 陕西省
    '咸阳市': {
        '政府采购网': 'http://zfcg.xianyang.gov.cn/',
        '公共资源交易': 'http://ggzy.xianyang.gov.cn/',
        '省份': '陕西省',
    },

    # 广西壮族自治区
    '南宁市': {
        '政府采购网': 'http://zfcg.nanning.gov.cn/',
        '公共资源交易': 'http://ggzy.nanning.gov.cn/',
        '省份': '广西壮族自治区',
    },
    '柳州市': {
        '政府采购网': 'http://zfcg.liuzhou.gov.cn/',
        '公共资源交易': 'http://ggzy.liuzhou.gov.cn/',
        '省份': '广西壮族自治区',
    },

    # 贵州省
    '贵阳市': {
        '政府采购网': 'http://zfcg.guiyang.gov.cn/',
        '公共资源交易': 'http://ggzy.guiyang.gov.cn/',
        '省份': '贵州省',
    },

    # 云南省
    '昆明市': {
        '政府采购网': 'http://zfcg.km.gov.cn/',
        '公共资源交易': 'http://ggzy.km.gov.cn/',
        '省份': '云南省',
    },

    # 海南省
    '海口市': {
        '政府采购网': 'http://zfcg.haikou.gov.cn/',
        '公共资源交易': 'http://ggzy.haikou.gov.cn/',
        '省份': '海南省',
    },
    '三亚市': {
        '政府采购网': 'http://zfcg.sanya.gov.cn/',
        '公共资源交易': 'http://ggzy.sanya.gov.cn/',
        '省份': '海南省',
    },
}

# ============================================================
# 五、示例县区级政府采购网（部分重点县区）
# ============================================================
COUNTY_LEVEL_EXAMPLES = {
    # 浙江省
    '安吉县': {
        '政府采购网': 'https://www.anji.gov.cn/',
        '省份': '浙江省',
        '地级市': '湖州市',
    },
    '义乌市': {
        '政府采购网': 'http://zfcg.yw.gov.cn/',
        '省份': '浙江省',
        '地级市': '金华市',
    },
    '慈溪市': {
        '政府采购网': 'http://zfcg.cixi.gov.cn/',
        '省份': '浙江省',
        '地级市': '宁波市',
    },

    # 江苏省
    '昆山市': {
        '政府采购网': 'http://zfcg.ks.gov.cn/',
        '省份': '江苏省',
        '地级市': '苏州市',
    },
    '江阴市': {
        '政府采购网': 'http://zfcg.jiangyin.gov.cn/',
        '省份': '江苏省',
        '地级市': '无锡市',
    },
    '张家港市': {
        '政府采购网': 'http://zfcg.zjg.gov.cn/',
        '省份': '江苏省',
        '地级市': '苏州市',
    },

    # 广东省
    '顺德区': {
        '政府采购网': 'http://zfcg.shunde.gov.cn/',
        '省份': '广东省',
        '地级市': '佛山市',
    },
    '南海区': {
        '政府采购网': 'http://zfcg.nanhai.gov.cn/',
        '省份': '广东省',
        '地级市': '佛山市',
    },

    # 山东省
    '龙口市': {
        '政府采购网': 'http://zfcg.longkou.gov.cn/',
        '省份': '山东省',
        '地级市': '烟台市',
    },

    # 福建省
    '晋江市': {
        '政府采购网': 'http://zfcg.jinjiang.gov.cn/',
        '省份': '福建省',
        '地级市': '泉州市',
    },
}

# ============================================================
# 六、行业专业招投标平台
# ============================================================
INDUSTRY_PLATFORMS = {
    '低空经济行业': {
        '低空界': 'https://www.dikongjie.com/Bidding_procurement/',
        '中国航空航天网': 'https://www.chinaerospace.com/',
        '先进空中交通产业联盟': 'https://aamshanghai.com/',
    },
    '民航行业': {
        '中国民航网': 'http://www.caacnews.com.cn/',
        '民航资源网': 'http://www.carnoc.com/',
    },
    '通用航空': {
        '中国通用航空网': 'http://www.tyhk.com.cn/',
        '通航在线': 'http://www.tonghangzaixian.com/',
    },
}


# ============================================================
# 统计汇总
# ============================================================
def get_statistics():
    """获取网站统计信息"""
    stats = {
        '国家级平台': len(NATIONAL_PLATFORMS),
        '省级平台（31省市自治区）': len(PROVINCIAL_PLATFORMS),
        '副省级城市及计划单列市': len(SUB_PROVINCIAL_CITIES),
        '重点地级市': len(MAJOR_PREFECTURE_CITIES),
        '示例县区级': len(COUNTY_LEVEL_EXAMPLES),
        '行业专业平台': sum(len(v) for v in INDUSTRY_PLATFORMS.values()),
    }

    total = sum(stats.values())
    stats['总计'] = total

    return stats


def get_all_urls():
    """获取所有网站URL列表"""
    urls = []

    # 国家级
    for name, info in NATIONAL_PLATFORMS.items():
        urls.append({
            '级别': '国家级',
            '名称': name,
            '网址': info.get('url', ''),
            '搜索网址': info.get('search_url', ''),
        })

    # 省级
    for province, platforms in PROVINCIAL_PLATFORMS.items():
        for platform_type, url in platforms.items():
            urls.append({
                '级别': '省级',
                '省份': province,
                '类型': platform_type,
                '网址': url,
            })

    # 副省级城市
    for city, platforms in SUB_PROVINCIAL_CITIES.items():
        for key, value in platforms.items():
            if key != '类型':
                urls.append({
                    '级别': '副省级城市',
                    '城市': city,
                    '类型': key,
                    '网址': value,
                    '城市类型': platforms.get('类型', ''),
                })

    # 地级市
    for city, platforms in MAJOR_PREFECTURE_CITIES.items():
        for key, value in platforms.items():
            if key != '省份':
                urls.append({
                    '级别': '地级市',
                    '城市': city,
                    '类型': key,
                    '网址': value,
                    '省份': platforms.get('省份', ''),
                })

    # 县区级
    for county, info in COUNTY_LEVEL_EXAMPLES.items():
        urls.append({
            '级别': '县区级',
            '县区': county,
            '网址': info.get('政府采购网', ''),
            '省份': info.get('省份', ''),
            '地级市': info.get('地级市', ''),
        })

    return urls


def export_to_excel(filename='政府采购网站清单.xlsx'):
    """导出网站清单到Excel"""
    import pandas as pd

    urls = get_all_urls()
    df = pd.DataFrame(urls)

    filepath = f'/home/user/Micksiney/{filename}'
    df.to_excel(filepath, index=False, sheet_name='政府采购网站清单')

    print(f"网站清单已导出到: {filepath}")
    return filepath


if __name__ == '__main__':
    # 打印统计信息
    stats = get_statistics()
    print("\n=== 中国各级政府采购网站统计 ===")
    for key, value in stats.items():
        print(f"{key}: {value}")

    # 导出到Excel
    export_to_excel()
