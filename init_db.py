#!/usr/bin/env python3
"""初始化 PostgreSQL 数据库表"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "postgresql://postgres:XQnlIaskTAaoKAMRWPvflOYLYQibhsiy@acela.proxy.rlwy.net:52707/railway"

def create_tables():
    """创建所有数据库表"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        # 创建学校表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schools (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                province VARCHAR(50),
                category VARCHAR(50),
                level VARCHAR(50),
                min_score INTEGER,
                max_score INTEGER,
                avg_score INTEGER,
                enrollment_count INTEGER,
                hot_majors TEXT,
                location VARCHAR(200)
            )
        """)
        print("✓ schools 表创建成功")
        
        # 创建专业表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS majors (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                category VARCHAR(50),
                degree VARCHAR(50),
                hot_level VARCHAR(50),
                avg_salary VARCHAR(50),
                employment_rate VARCHAR(10),
                difficulty VARCHAR(50),
                description TEXT,
                careers TEXT,
                subjects_required TEXT
            )
        """)
        print("✓ majors 表创建成功")
        
        # 创建学校专业关联表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS school_majors (
                id SERIAL PRIMARY KEY,
                school_id VARCHAR(50),
                major_id VARCHAR(50)
            )
        """)
        print("✓ school_majors 表创建成功")
        
        # 创建专业分数线表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS major_score_lines (
                id SERIAL PRIMARY KEY,
                school_id VARCHAR(50),
                major_id VARCHAR(50),
                year INTEGER,
                score INTEGER,
                batch VARCHAR(50),
                province VARCHAR(50)
            )
        """)
        print("✓ major_score_lines 表创建成功")
        
        # 创建收藏表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id VARCHAR(50) PRIMARY KEY,
                user_id VARCHAR(50),
                item_id VARCHAR(50),
                item_type VARCHAR(50),
                item_name VARCHAR(200),
                created_at TIMESTAMP
            )
        """)
        print("✓ favorites 表创建成功")
        
        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(50) PRIMARY KEY,
                openid VARCHAR(100),
                score INTEGER,
                category VARCHAR(50),
                province VARCHAR(50),
                created_at TIMESTAMP
            )
        """)
        print("✓ users 表创建成功")
        
        conn.commit()
        print("\n所有表创建完成！")
        
    except Exception as e:
        conn.rollback()
        print(f"创建表失败: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def insert_sample_data():
    """插入示例数据"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        # 插入学校数据
        schools = [
            ("school_001", "清华大学", "北京", "理工类", "985/211", 680, 720, 695, 3500, "计算机科学与技术、电子信息工程、自动化", "北京市海淀区"),
            ("school_002", "北京大学", "北京", "综合类", "985/211", 675, 715, 690, 3800, "金融学、法学、数学与应用数学", "北京市海淀区"),
            ("school_003", "复旦大学", "上海", "综合类", "985/211", 660, 690, 672, 3200, "新闻传播学、经济学、软件工程", "上海市杨浦区"),
            ("school_004", "上海交通大学", "上海", "理工类", "985/211", 658, 685, 668, 4200, "机械工程、船舶与海洋工程、工商管理", "上海市闵行区"),
            ("school_005", "浙江大学", "浙江", "综合类", "985/211", 655, 680, 665, 6000, "计算机科学与技术、光学工程、农学", "浙江省杭州市"),
            ("school_006", "南京大学", "江苏", "综合类", "985/211", 650, 675, 660, 3300, "天文学、大气科学、环境科学与工程", "江苏省南京市"),
            ("school_007", "中国科学技术大学", "安徽", "理工类", "985/211", 655, 680, 665, 1860, "物理学、化学、生物科学", "安徽省合肥市"),
            ("school_008", "武汉大学", "湖北", "综合类", "985/211", 630, 660, 642, 7200, "测绘工程、水利水电工程、法学", "湖北省武汉市"),
            ("school_009", "华中科技大学", "湖北", "理工类", "985/211", 625, 655, 637, 6200, "机械工程、光电信息科学与工程、公共卫生与预防医学", "湖北省武汉市"),
            ("school_010", "中山大学", "广东", "综合类", "985/211", 620, 650, 632, 8000, "临床医学、工商管理、生态学", "广东省广州市"),
            ("school_011", "四川大学", "四川", "综合类", "985/211", 610, 640, 622, 9000, "口腔医学、高分子材料工程、水利水电工程", "四川省成都市"),
            ("school_012", "西安交通大学", "陕西", "理工类", "985/211", 615, 645, 627, 4600, "电气工程、能源与动力工程、管理科学与工程", "陕西省西安市"),
            ("school_013", "哈尔滨工业大学", "黑龙江", "理工类", "985/211", 620, 650, 632, 4700, "航天航空工程、机械工程、焊接技术与工程", "黑龙江省哈尔滨市"),
            ("school_014", "北京航空航天大学", "北京", "理工类", "985/211", 625, 655, 637, 3900, "航空宇航科学与技术、仪器科学与技术", "北京市海淀区"),
            ("school_015", "同济大学", "上海", "理工类", "985/211", 615, 645, 627, 4400, "土木工程、建筑学、城乡规划", "上海市杨浦区")
        ]
        
        for school in schools:
            cursor.execute("""
                INSERT INTO schools (id, name, province, category, level, min_score, max_score, avg_score, enrollment_count, hot_majors, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, school)
        print(f"✓ 插入了 {len(schools)} 所学校")
        
        # 插入专业数据
        majors = [
            ("major_001", "计算机科学与技术", "理工类", "工学学士", "热门", "15K-30K", "95%", "困难", "培养系统掌握计算机硬件、软件与应用的基本理论、基本知识和基本技能与方法的高级专门科学技术人才。", "软件工程师、系统架构师、数据工程师、AI工程师", "数学、物理"),
            ("major_002", "人工智能", "理工类", "工学学士", "非常热门", "18K-40K", "98%", "困难", "培养具备计算机、心理学和哲学等学科知识的高级复合型人才，能够研发和应用智能系统、算法和模型解决实际问题。", "AI工程师、算法工程师、机器学习工程师、数据科学家", "数学、物理"),
            ("major_003", "数据科学与大数据技术", "理工类", "理学学士", "非常热门", "15K-35K", "97%", "较难", "培养具备数据科学基础知识和技术能力，能够进行数据采集、清洗、分析和可视化的专业人才。", "数据分析师、大数据工程师、数据产品经理", "数学、统计"),
            ("major_004", "软件工程", "理工类", "工学学士", "热门", "12K-25K", "93%", "较难", "培养能够从事软件开发、测试、维护和管理等工作的高层次、应用型软件工程技术人才。", "软件开发工程师、测试工程师、项目经理", "数学"),
            ("major_005", "金融学", "经管类", "经济学学士", "热门", "10K-30K", "90%", "中等", "培养具备金融学方面的理论知识和业务技能，能在银行、证券、投资、保险及其他经济管理部门和企业从事相关工作的专门人才。", "银行职员、证券分析师、金融产品经理", "数学"),
            ("major_006", "临床医学", "医学类", "医学学士", "热门", "8K-20K", "98%", "困难", "培养具备基础医学、临床医学的基本理论和医疗预防的基本技能，能在医疗卫生单位、医学科研等部门从事医疗及预防、医学科研等方面工作的医学高级专门人才。", "临床医生、医学研究员、医院管理", "生物、化学"),
            ("major_007", "口腔医学", "医学类", "医学学士", "热门", "10K-25K", "98%", "困难", "培养具备基础医学和临床医学的基本理论知识，受到口腔及颌面部疾病的诊断、治疗、预防方面的训练，具有口腔常见病、多发病的诊疗、修复和预防保健能力的医学专门人才。", "口腔医生、口腔医院管理、医学研究", "生物、化学"),
            ("major_008", "电子信息工程", "理工类", "工学学士", "热门", "10K-20K", "92%", "较难", "培养具备电子技术和信息系统的基础知识，能从事各类电子设备和信息系统的研究、设计、制造、应用和开发的高等工程技术人才。", "电子工程师、通信工程师、硬件工程师", "数学、物理"),
            ("major_009", "自动化", "理工类", "工学学士", "热门", "10K-20K", "94%", "较难", "培养具备控制理论、控制系统、信号处理等专业知识，能在工业过程控制、电气自动化、仪表智能化等领域从事系统设计、研发、运行和管理的高级工程技术人才。", "自动化工程师、控制工程师、系统集成工程师", "数学、物理"),
            ("major_010", "新能源科学与工程", "理工类", "工学学士", "热门", "10K-22K", "95%", "较难", "培养具备新能源科学与工程方面的基础知识，能够在太阳能、风能、生物质能等新能源领域从事技术研发、工程设计和项目管理的高级工程技术人才。", "新能源工程师、光伏工程师、风电工程师", "数学、物理、化学"),
            ("major_011", "法学", "法学类", "法学学士", "热门", "8K-18K", "85%", "较难", "培养系统掌握法学知识，熟悉我国法律和党的相关政策，能在国家机关、企事业单位和社会团体从事法律工作的高级专门人才。", "律师、法官、检察官、法务人员", ""),
            ("major_012", "物联网工程", "理工类", "工学学士", "热门", "10K-22K", "94%", "较难", "培养掌握物联网相关理论、方法和技能，能够在智能家居、智能交通、智能电网、智慧城市等领域从事物联网系统设计、研发、应用和管理的复合型高级工程技术人才。", "物联网工程师、嵌入式工程师、系统架构师", "数学、物理"),
            ("major_013", "生物医学工程", "理工类", "工学学士", "热门", "10K-22K", "93%", "较难", "培养具备生命科学、电子技术、计算机技术和信息科学的基础理论知识，能在生物医学工程领域从事科学研究、技术开发等工作的复合型高级工程技术人才。", "医疗器械工程师、生物工程师、医学影像工程师", "生物、化学、物理"),
            ("major_014", "电子商务", "经管类", "管理学学士", "热门", "8K-20K", "91%", "中等", "培养具备管理、经济、法律、现代商务等方面的基础知识，能够在各类企事业及政府部门从事电子商务运作与管理的高级应用型人才。", "电商运营、平台管理、网络营销", ""),
            ("major_015", "机械工程", "理工类", "工学学士", "一般", "8K-18K", "92%", "中等", "培养具备机械设计、制造、自动化等基础知识，能在机械工程领域从事设计、制造、技术开发、运行管理的高级工程技术人才。", "机械工程师、工艺工程师、设备工程师", "数学、物理")
        ]
        
        for major in majors:
            cursor.execute("""
                INSERT INTO majors (id, name, category, degree, hot_level, avg_salary, employment_rate, difficulty, description, careers, subjects_required)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, major)
        print(f"✓ 插入了 {len(majors)} 个专业")
        
        # 插入分数线数据
        score_lines = [
            ("school_001", "major_001", 2024, 685, "本科一批", "全国"),
            ("school_001", "major_001", 2023, 680, "本科一批", "全国"),
            ("school_001", "major_001", 2022, 678, "本科一批", "全国"),
            ("school_001", "major_002", 2024, 688, "本科一批", "全国"),
            ("school_001", "major_002", 2023, 682, "本科一批", "全国"),
            ("school_002", "major_005", 2024, 680, "本科一批", "全国"),
            ("school_002", "major_005", 2023, 676, "本科一批", "全国"),
            ("school_002", "major_011", 2024, 675, "本科一批", "全国"),
            ("school_003", "major_004", 2024, 662, "本科一批", "全国"),
            ("school_003", "major_004", 2023, 658, "本科一批", "全国"),
            ("school_004", "major_008", 2024, 660, "本科一批", "全国"),
            ("school_004", "major_008", 2023, 656, "本科一批", "全国"),
            ("school_005", "major_001", 2024, 658, "本科一批", "全国"),
            ("school_005", "major_001", 2023, 654, "本科一批", "全国"),
            ("school_006", "major_003", 2024, 652, "本科一批", "全国"),
            ("school_006", "major_003", 2023, 648, "本科一批", "全国"),
        ]
        
        for line in score_lines:
            cursor.execute("""
                INSERT INTO major_score_lines (school_id, major_id, year, score, batch, province)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, line)
        print(f"✓ 插入了 {len(score_lines)} 条分数线")
        
        conn.commit()
        print("\n所有数据插入完成！")
        
    except Exception as e:
        conn.rollback()
        print(f"插入数据失败: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("开始初始化数据库...")
    print("=" * 50)
    create_tables()
    print("=" * 50)
    insert_sample_data()
    print("=" * 50)
    print("数据库初始化完成！")