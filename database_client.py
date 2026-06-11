import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseClient:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            # 使用 Railway PostgreSQL
            self.database_url = "postgresql://postgres:XQnlIaskTAaoKAMRWPvflOYLYQibhsiy@postgres.railway.internal:5432/railway"
        self._use_mock = False
        self._init_mock_data()
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = None
        try:
            conn = psycopg2.connect(self.database_url)
            yield conn
        finally:
            if conn:
                conn.close()
    
    @contextmanager
    def get_cursor(self, cursor_factory=RealDictCursor):
        """获取数据库游标的上下文管理器"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
    
    def _init_mock_data(self):
        """初始化Mock数据（数据库连接失败时使用）"""
        self._schools = [
            {"id": "school_001", "name": "清华大学", "province": "北京", "category": "理工类", "level": "985/211", "min_score": 680, "max_score": 720, "avg_score": 695, "enrollment_count": 3500, "hot_majors": ["计算机科学与技术", "电子信息工程", "自动化"], "location": "北京市海淀区"},
            {"id": "school_002", "name": "北京大学", "province": "北京", "category": "综合类", "level": "985/211", "min_score": 675, "max_score": 715, "avg_score": 690, "enrollment_count": 3800, "hot_majors": ["金融学", "法学", "数学与应用数学"], "location": "北京市海淀区"},
            {"id": "school_003", "name": "复旦大学", "province": "上海", "category": "综合类", "level": "985/211", "min_score": 660, "max_score": 690, "avg_score": 672, "enrollment_count": 3200, "hot_majors": ["新闻传播学", "经济学", "软件工程"], "location": "上海市杨浦区"},
            {"id": "school_004", "name": "上海交通大学", "province": "上海", "category": "理工类", "level": "985/211", "min_score": 658, "max_score": 685, "avg_score": 668, "enrollment_count": 4200, "hot_majors": ["机械工程", "船舶与海洋工程", "工商管理"], "location": "上海市闵行区"},
            {"id": "school_005", "name": "浙江大学", "province": "浙江", "category": "综合类", "level": "985/211", "min_score": 655, "max_score": 680, "avg_score": 665, "enrollment_count": 6000, "hot_majors": ["计算机科学与技术", "光学工程", "农学"], "location": "浙江省杭州市"},
            {"id": "school_006", "name": "南京大学", "province": "江苏", "category": "综合类", "level": "985/211", "min_score": 650, "max_score": 675, "avg_score": 660, "enrollment_count": 3300, "hot_majors": ["天文学", "大气科学", "环境科学与工程"], "location": "江苏省南京市"},
            {"id": "school_007", "name": "中国科学技术大学", "province": "安徽", "category": "理工类", "level": "985/211", "min_score": 655, "max_score": 680, "avg_score": 665, "enrollment_count": 1860, "hot_majors": ["物理学", "化学", "生物科学"], "location": "安徽省合肥市"},
            {"id": "school_008", "name": "武汉大学", "province": "湖北", "category": "综合类", "level": "985/211", "min_score": 630, "max_score": 660, "avg_score": 642, "enrollment_count": 7200, "hot_majors": ["测绘工程", "水利水电工程", "法学"], "location": "湖北省武汉市"},
            {"id": "school_009", "name": "华中科技大学", "province": "湖北", "category": "理工类", "level": "985/211", "min_score": 625, "max_score": 655, "avg_score": 637, "enrollment_count": 6200, "hot_majors": ["机械工程", "光电信息科学与工程", "公共卫生与预防医学"], "location": "湖北省武汉市"},
            {"id": "school_010", "name": "中山大学", "province": "广东", "category": "综合类", "level": "985/211", "min_score": 620, "max_score": 650, "avg_score": 632, "enrollment_count": 8000, "hot_majors": ["临床医学", "工商管理", "生态学"], "location": "广东省广州市"},
            {"id": "school_011", "name": "四川大学", "province": "四川", "category": "综合类", "level": "985/211", "min_score": 610, "max_score": 640, "avg_score": 622, "enrollment_count": 9000, "hot_majors": ["口腔医学", "高分子材料工程", "水利水电工程"], "location": "四川省成都市"},
            {"id": "school_012", "name": "西安交通大学", "province": "陕西", "category": "理工类", "level": "985/211", "min_score": 615, "max_score": 645, "avg_score": 627, "enrollment_count": 4600, "hot_majors": ["电气工程", "能源与动力工程", "管理科学与工程"], "location": "陕西省西安市"},
            {"id": "school_013", "name": "哈尔滨工业大学", "province": "黑龙江", "category": "理工类", "level": "985/211", "min_score": 620, "max_score": 650, "avg_score": 632, "enrollment_count": 4700, "hot_majors": ["航天航空工程", "机械工程", "焊接技术与工程"], "location": "黑龙江省哈尔滨市"},
            {"id": "school_014", "name": "北京航空航天大学", "province": "北京", "category": "理工类", "level": "985/211", "min_score": 625, "max_score": 655, "avg_score": 637, "enrollment_count": 3900, "hot_majors": ["航空宇航科学与技术", "仪器科学与技术"], "location": "北京市海淀区"},
            {"id": "school_015", "name": "同济大学", "province": "上海", "category": "理工类", "level": "985/211", "min_score": 615, "max_score": 645, "avg_score": 627, "enrollment_count": 4400, "hot_majors": ["土木工程", "建筑学", "城乡规划"], "location": "上海市杨浦区"}
        ]
        
        self._majors = [
            {"id": "major_001", "name": "计算机科学与技术", "category": "理工类", "degree": "工学学士", "hot_level": "热门", "avg_salary": "15K-30K", "employment_rate": "95%", "difficulty": "困难", "description": "培养系统掌握计算机硬件、软件与应用的基本理论、基本知识和基本技能与方法的高级专门科学技术人才。", "careers": ["软件工程师", "系统架构师", "数据工程师", "AI工程师"], "subjects_required": ["数学", "物理"]},
            {"id": "major_002", "name": "人工智能", "category": "理工类", "degree": "工学学士", "hot_level": "非常热门", "avg_salary": "18K-40K", "employment_rate": "98%", "difficulty": "困难", "description": "培养具备计算机、心理学和哲学等学科知识的高级复合型人才，能够研发和应用智能系统、算法和模型解决实际问题。", "careers": ["AI工程师", "算法工程师", "机器学习工程师", "数据科学家"], "subjects_required": ["数学", "物理"]},
            {"id": "major_003", "name": "数据科学与大数据技术", "category": "理工类", "degree": "理学学士", "hot_level": "非常热门", "avg_salary": "15K-35K", "employment_rate": "97%", "difficulty": "较难", "description": "培养具备数据科学基础知识和技术能力，能够进行数据采集、清洗、分析和可视化的专业人才。", "careers": ["数据分析师", "大数据工程师", "数据产品经理"], "subjects_required": ["数学", "统计"]},
            {"id": "major_004", "name": "软件工程", "category": "理工类", "degree": "工学学士", "hot_level": "热门", "avg_salary": "12K-25K", "employment_rate": "93%", "difficulty": "较难", "description": "培养能够从事软件开发、测试、维护和管理等工作的高层次、应用型软件工程技术人才。", "careers": ["软件开发工程师", "测试工程师", "项目经理"], "subjects_required": ["数学"]},
            {"id": "major_005", "name": "金融学", "category": "经管类", "degree": "经济学学士", "hot_level": "热门", "avg_salary": "10K-30K", "employment_rate": "90%", "difficulty": "中等", "description": "培养具备金融学方面的理论知识和业务技能，能在银行、证券、投资、保险及其他经济管理部门和企业从事相关工作的专门人才。", "careers": ["银行职员", "证券分析师", "金融产品经理"], "subjects_required": ["数学"]},
            {"id": "major_006", "name": "临床医学", "category": "医学类", "degree": "医学学士", "hot_level": "热门", "avg_salary": "8K-20K", "employment_rate": "98%", "difficulty": "困难", "description": "培养具备基础医学、临床医学的基本理论和医疗预防的基本技能，能在医疗卫生单位、医学科研等部门从事医疗及预防、医学科研等方面工作的医学高级专门人才。", "careers": ["临床医生", "医学研究员", "医院管理"], "subjects_required": ["生物", "化学"]},
            {"id": "major_007", "name": "口腔医学", "category": "医学类", "degree": "医学学士", "hot_level": "热门", "avg_salary": "10K-25K", "employment_rate": "98%", "difficulty": "困难", "description": "培养具备基础医学和临床医学的基本理论知识，受到口腔及颌面部疾病的诊断、治疗、预防方面的训练，具有口腔常见病、多发病的诊疗、修复和预防保健能力的医学专门人才。", "careers": ["口腔医生", "口腔医院管理", "医学研究"], "subjects_required": ["生物", "化学"]},
            {"id": "major_008", "name": "电子信息工程", "category": "理工类", "degree": "工学学士", "hot_level": "热门", "avg_salary": "10K-20K", "employment_rate": "92%", "difficulty": "较难", "description": "培养具备电子技术和信息系统的基础知识，能从事各类电子设备和信息系统的研究、设计、制造、应用和开发的高等工程技术人才。", "careers": ["电子工程师", "通信工程师", "硬件工程师"], "subjects_required": ["数学", "物理"]},
            {"id": "major_009", "name": "自动化", "category": "理工类", "degree": "工学学士", "hot_level": "热门", "avg_salary": "10K-20K", "employment_rate": "94%", "difficulty": "较难", "description": "培养具备控制理论、控制系统、信号处理等专业知识，能在工业过程控制、电气自动化、仪表智能化等领域从事系统设计、研发、运行和管理的高级工程技术人才。", "careers": ["自动化工程师", "控制工程师", "系统集成工程师"], "subjects_required": ["数学", "物理"]},
            {"id": "major_010", "name": "新能源科学与工程", "category": "理工类", "degree": "工学学士", "hot_level": "热门", "avg_salary": "10K-22K", "employment_rate": "95%", "difficulty": "较难", "description": "培养具备新能源科学与工程方面的基础知识，能够在太阳能、风能、生物质能等新能源领域从事技术研发、工程设计和项目管理的高级工程技术人才。", "careers": ["新能源工程师", "光伏工程师", "风电工程师"], "subjects_required": ["数学", "物理", "化学"]},
            {"id": "major_011", "name": "法学", "category": "法学类", "degree": "法学学士", "hot_level": "热门", "avg_salary": "8K-18K", "employment_rate": "85%", "difficulty": "较难", "description": "培养系统掌握法学知识，熟悉我国法律和党的相关政策，能在国家机关、企事业单位和社会团体从事法律工作的高级专门人才。", "careers": ["律师", "法官", "检察官", "法务人员"], "subjects_required": []},
            {"id": "major_012", "name": "物联网工程", "category": "理工类", "degree": "工学学士", "hot_level": "热门", "avg_salary": "10K-22K", "employment_rate": "94%", "difficulty": "较难", "description": "培养掌握物联网相关理论、方法和技能，能够在智能家居、智能交通、智能电网、智慧城市等领域从事物联网系统设计、研发、应用和管理的复合型高级工程技术人才。", "careers": ["物联网工程师", "嵌入式工程师", "系统架构师"], "subjects_required": ["数学", "物理"]},
            {"id": "major_013", "name": "生物医学工程", "category": "理工类", "degree": "工学学士", "hot_level": "热门", "avg_salary": "10K-22K", "employment_rate": "93%", "difficulty": "较难", "description": "培养具备生命科学、电子技术、计算机技术和信息科学的基础理论知识，能在生物医学工程领域从事科学研究、技术开发等工作的复合型高级工程技术人才。", "careers": ["医疗器械工程师", "生物工程师", "医学影像工程师"], "subjects_required": ["生物", "化学", "物理"]},
            {"id": "major_014", "name": "电子商务", "category": "经管类", "degree": "管理学学士", "hot_level": "热门", "avg_salary": "8K-20K", "employment_rate": "91%", "difficulty": "中等", "description": "培养具备管理、经济、法律、现代商务等方面的基础知识，能够在各类企事业及政府部门从事电子商务运作与管理的高级应用型人才。", "careers": ["电商运营", "平台管理", "网络营销"], "subjects_required": []},
            {"id": "major_015", "name": "机械工程", "category": "理工类", "degree": "工学学士", "hot_level": "一般", "avg_salary": "8K-18K", "employment_rate": "92%", "difficulty": "中等", "description": "培养具备机械设计、制造、自动化等基础知识，能在机械工程领域从事设计、制造、技术开发、运行管理的高级工程技术人才。", "careers": ["机械工程师", "工艺工程师", "设备工程师"], "subjects_required": ["数学", "物理"]}
        ]
        
        self._favorites = []
        self._major_score_lines = [
            {"id": "score_001", "school_id": "school_001", "major_id": "major_001", "year": 2024, "score": 685, "batch": "本科一批", "province": "全国"},
            {"id": "score_002", "school_id": "school_001", "major_id": "major_001", "year": 2023, "score": 680, "batch": "本科一批", "province": "全国"},
            {"id": "score_003", "school_id": "school_001", "major_id": "major_001", "year": 2022, "score": 678, "batch": "本科一批", "province": "全国"},
            {"id": "score_004", "school_id": "school_001", "major_id": "major_002", "year": 2024, "score": 688, "batch": "本科一批", "province": "全国"},
            {"id": "score_005", "school_id": "school_001", "major_id": "major_002", "year": 2023, "score": 682, "batch": "本科一批", "province": "全国"},
            {"id": "score_006", "school_id": "school_002", "major_id": "major_005", "year": 2024, "score": 680, "batch": "本科一批", "province": "全国"},
            {"id": "score_007", "school_id": "school_002", "major_id": "major_005", "year": 2023, "score": 676, "batch": "本科一批", "province": "全国"},
            {"id": "score_008", "school_id": "school_002", "major_id": "major_011", "year": 2024, "score": 675, "batch": "本科一批", "province": "全国"},
            {"id": "score_009", "school_id": "school_003", "major_id": "major_004", "year": 2024, "score": 662, "batch": "本科一批", "province": "全国"},
            {"id": "score_010", "school_id": "school_003", "major_id": "major_004", "year": 2023, "score": 658, "batch": "本科一批", "province": "全国"}
        ]
    
    # ========== 学校操作 ==========
    
    async def get_schools(self, province: Optional[str] = None, category: Optional[str] = None, min_score: Optional[int] = None, max_score: Optional[int] = None, limit: int = 50) -> List[Dict]:
        """获取学校列表"""
        try:
            with self.get_cursor() as cursor:
                query = "SELECT * FROM schools WHERE 1=1"
                params = []
                if province:
                    query += " AND province = %s"
                    params.append(province)
                if category:
                    query += " AND category = %s"
                    params.append(category)
                if min_score:
                    query += " AND min_score >= %s"
                    params.append(min_score)
                if max_score:
                    query += " AND max_score <= %s"
                    params.append(max_score)
                query += f" LIMIT {limit}"
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            schools = self._schools.copy()
            if province:
                schools = [s for s in schools if s['province'] == province]
            if category:
                schools = [s for s in schools if s['category'] == category]
            if min_score:
                schools = [s for s in schools if s['min_score'] >= min_score]
            if max_score:
                schools = [s for s in schools if s['max_score'] <= max_score]
            return schools[:limit]
    
    async def get_school_by_id(self, school_id: str) -> Optional[Dict]:
        """根据ID获取学校"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT * FROM schools WHERE id = %s", (school_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            for school in self._schools:
                if school['id'] == school_id:
                    return school
            return None
    
    async def get_provinces(self) -> List[str]:
        """获取所有省份"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT DISTINCT province FROM schools ORDER BY province")
                return [row['province'] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            return list(set([s['province'] for s in self._schools]))
    
    # ========== 专业操作 ==========
    
    async def get_majors(self, category: Optional[str] = None, hot_level: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """获取专业列表"""
        try:
            with self.get_cursor() as cursor:
                query = "SELECT * FROM majors WHERE 1=1"
                params = []
                if category:
                    query += " AND category = %s"
                    params.append(category)
                if hot_level:
                    query += " AND hot_level = %s"
                    params.append(hot_level)
                query += f" LIMIT {limit}"
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            majors = self._majors.copy()
            if category:
                majors = [m for m in majors if m['category'] == category]
            if hot_level:
                majors = [m for m in majors if m['hot_level'] == hot_level]
            return majors[:limit]
    
    async def get_major_by_id(self, major_id: str) -> Optional[Dict]:
        """根据ID获取专业"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT * FROM majors WHERE id = %s", (major_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            for major in self._majors:
                if major['id'] == major_id:
                    return major
            return None
    
    async def get_major_categories(self) -> List[str]:
        """获取所有专业类别"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT DISTINCT category FROM majors ORDER BY category")
                return [row['category'] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            return list(set([m['category'] for m in self._majors]))
    
    async def get_school_majors(self, school_id: str) -> List[Dict]:
        """获取学校的所有专业"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    SELECT m.* FROM majors m
                    INNER JOIN school_majors sm ON m.id = sm.major_id
                    WHERE sm.school_id = %s
                """, (school_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            return self._majors[:4]  # 返回前4个专业作为示例
    
    async def get_major_score_lines(self, major_id: str, school_id: Optional[str] = None) -> List[Dict]:
        """获取专业的分数线"""
        try:
            with self.get_cursor() as cursor:
                if school_id:
                    cursor.execute("""
                        SELECT * FROM major_score_lines 
                        WHERE major_id = %s AND school_id = %s
                        ORDER BY year DESC
                    """, (major_id, school_id))
                else:
                    cursor.execute("""
                        SELECT * FROM major_score_lines 
                        WHERE major_id = %s
                        ORDER BY year DESC
                    """, (major_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            return [s for s in self._major_score_lines if s['major_id'] == major_id][:3]
    
    # ========== 收藏操作 ==========
    
    async def add_favorite(self, item: Dict[str, Any]) -> Dict:
        """添加收藏"""
        from datetime import datetime
        import uuid
        
        favorite = {
            "id": str(uuid.uuid4()),
            "user_id": item.get('user_id', 'anonymous'),
            "item_id": item['item_id'],
            "item_type": item['item_type'],
            "item_name": item['item_name'],
            "created_at": datetime.now().isoformat()
        }
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO favorites (id, user_id, item_id, item_type, item_name, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (favorite['id'], favorite['user_id'], favorite['item_id'], 
                      favorite['item_type'], favorite['item_name'], favorite['created_at']))
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            self._favorites.append(favorite)
        
        return favorite
    
    async def get_favorites(self, user_id: str) -> List[Dict]:
        """获取用户收藏"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT * FROM favorites WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            return [f for f in self._favorites if f.get('user_id') == user_id]
    
    async def remove_favorite(self, favorite_id: str) -> bool:
        """删除收藏"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("DELETE FROM favorites WHERE id = %s", (favorite_id,))
            return True
        except Exception as e:
            print(f"Database error, using mock data: {e}")
            self._favorites = [f for f in self._favorites if f['id'] != favorite_id]
            return True
    
    # ========== 数据库初始化 ==========
    
    async def init_database(self):
        """初始化数据库表结构"""
        try:
            with self.get_cursor() as cursor:
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
                        hot_majors TEXT[],
                        location VARCHAR(200)
                    )
                """)
                
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
                        careers TEXT[],
                        subjects_required TEXT[]
                    )
                """)
                
                # 创建学校专业关联表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS school_majors (
                        school_id VARCHAR(50),
                        major_id VARCHAR(50),
                        PRIMARY KEY (school_id, major_id)
                    )
                """)
                
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
                
                print("Database tables initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise e