from db.DatabaseConnection import DatabaseConnection
from models.medal_Rank import Medal_Rank

class MedalRankDB(DatabaseConnection):
    def __init__(self):
        super().__init__()
        self.connect()

    def add_medal_rank(self, rank, countryname, countryid, gold, silver, bronze, count):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO medal_rank (rank, countryname, countryid, gold, silver, bronze, count) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (rank, countryname, countryid, gold, silver, bronze, count))
            self.conn.commit()
        finally:
            self.close()

    def delete_medal_rank(self, id):
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM medal_rank WHERE id = ?", (id,))
            self.conn.commit()
        finally:
            self.close()

    def update_medal_rank(self, id, new_values):
        try:
            cur = self.conn.cursor()
            query = "UPDATE medal_rank SET "
            query += ", ".join([f"{key} = ?" for key in new_values.keys()])
            query += " WHERE id = ?"
            cur.execute(query, list(new_values.values()) + [id])
            self.conn.commit()
        finally:
            self.close()

    def get_medal_rank(self, id):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM medal_rank WHERE id = ?", (id,))
            return cur.fetchone()
        finally:
            self.close()

class Medal_RankDbService(Medal_Rank_Operator):
    __tablename__ = "medal_rank"
    def __init__(self):
        super(Medal_RankDbService, self).__init__()

    # 请求全部排名
    def query_all_rank(self):
        pass

    # 请求指定国家排名信息
    def query_rank_by_cid(self, cid):
        pass

    # 新增奖牌榜信息-->新增国家获奖
    def insert_medal_rank(self):
        pass

    # 修改奖牌榜信息-->修改国家获奖
    def modify_medal_info(self):
        pass

    # 删除奖牌榜信息-->删除国家获奖
    def delete_medal_rank(self):
        pass


class AdminService:
    def __init__(self, username, userid):
        pass

    # 新增用户
    def insert_user(self):
        pass

    # 批量新增用户
    def insert_usermany(self):
        pass

    # 修改用户
    def modify_user(self):
        pass

    #  删除用户
    def delete_user(self):
        pass

    # 新增比赛
    def insert_match(self):
        pass

    # 批量新增比赛
    def insert_matchmany(self):
        pass

    # 修改比赛
    def modify_match(self):
        pass

    # 删除比赛
    def delete_match(self):
        pass

    # 新增比赛项目
    def insert_project(self):
        pass

    # 批量新增比赛项目
    def insert_projectmany(self):
        pass

    #