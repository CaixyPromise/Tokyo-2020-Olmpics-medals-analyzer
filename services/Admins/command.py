import concurrent.futures

from response.medal import MedalInsertResponse
from response.reward import MedalLogResponse
from ui.utils.functions import Ui_Function
from ui.AskUserQuestionWindow import AskUserQuestionDialog
from tkinter import messagebox
from services.Admins.Admin import AdminService
from models.competition import Competition
from models.team import NationalTeam
from models.Users import User
from tkinter.messagebox import showerror
from tkinter.filedialog import asksaveasfilename, askopenfilename
from utils.ExcelUtils import MakeTemplate, ReadTemplate
from models.enums import Column
from response.User import UserDeleteResponse, UserAddAdminResponse, UserModifyResponse
import difflib
from tkinter import StringVar

from utils.upload_file import copy_and_rename_files


class RaceButtonCommand(Ui_Function):
    question_config = {
        '比赛ID':   {'type': 'text'},
        '比赛时间': {'type': 'time'},
        '比赛大项': {'type': 'text'},
        '比赛名称': {'type': 'text'},
        '比赛地点': {'type': 'text'},
        '比赛类型': {'type': 'text'},
        '比赛状态': {'type': 'combobox', 'value': ('未开始', '已完成')},
        }

    def __init__(self, parent=None, **kwargs):
        super(RaceButtonCommand, self).__init__(parent, **kwargs)
        self.__service = AdminService()
        self.main_tree = self.part.get('tree')       # 主界面的tree
        self.treeview = self.parent.treeview         # 子界面的tree -- mannager 界面里的

    def add(self, **kwags):
        win = AskUserQuestionDialog(part_dict = self.question_config,
                                    name = '新增比赛')
        win.wait_window()
        if win.result:
            race_node = Competition(*win.result)
            # # 提交数据库
            try:
                self.__service.insert_match(race_node)
            except Exception:
                messagebox.showinfo('提示', '添加失败, 比赛ID重复')
            messagebox.showinfo('提示', '添加成功')
            self.treeview.insert_single(race_node)
            self.main_tree.update()
            self.main_tree.insert_single(race_node)
            self.main_tree.update()
        else:
            messagebox.showinfo('提示', '添加失败')
    def remove(self, **kwags):
        selection = self.treeview.get_choice_RowData('all')
        if (selection is not None):
            _id = selection[1][0]
            if (messagebox.askyesno('确认', '确定删除？')):
                self.__service.delete_match(_id)
                self.treeview.delete(selection[0])
                self.treeview.update()
                self.main_tree.delete(selection[0])
                self.main_tree.update()
        return

    def modify(self, **kwags):
        selection = self.treeview.get_choice_columnData(kwags.get('event', None))
        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data,  item = selection
            question_name = list(self.question_config.keys())[column_index]
            column = {question_name: self.question_config[question_name]}
            win = AskUserQuestionDialog(part_dict = column,
                                        name = f'修改 {question_name}')
            win.wait_window()
            if (win.result is not None):
                all_data = list(all_data)
                all_data[column_index] = win.result[0]
                selection_node = Competition(*all_data)
                self.__service.modify_match(selection_node)
                self.treeview.item(item, values = all_data)
                self.main_tree.item(item, values = all_data)

    def search(self, ):
        target_string = self.parent.search_entry.get()
        if (target_string == ''):
            showerror('错误', '请输入搜索内容')
            return
        max_similarity = 0
        most_similar_item = None

        for item in self.treeview.get_children():
            row_data = self.treeview.item(item, "values")
            for cell_data in row_data:
                similarity = difflib.SequenceMatcher(None, target_string, cell_data).ratio()
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_item = item

        if most_similar_item:
            self.treeview.selection_set(most_similar_item)
            self.treeview.see(most_similar_item)
        else:
            showerror('没有找到', '没有找到与输入相似的项')

    def manny(self, **kwags):
        file_path = askopenfilename(title = '选择 Excel 文件',
                                               filetypes = [('Excel files', '*.xlsx')]
                                               )
        if (file_path):
            columns = Column.race.value
            reader = ReadTemplate(file_path)
            data = reader.read(columns, Competition)
            self.__service.insert_matchmany(data)
            self.treeview.insert_manny(data)
            self.main_tree.update()
            self.main_tree.insert_manny(data)
            self.main_tree.update()

    def template(self):
        options = {
            'defaultextension': '.xlsx',
            'filetypes':        [('Excel files', '.xlsx'), ('All files', '.*')],
            'initialfile':      '批量添加比赛模板.xlsx',
            'title':            '选择保存位置'
            }
        filename = asksaveasfilename(**options)
        if (filename):
            writer = MakeTemplate(Column.race.value, filename)
            writer.make()


class TeamButtonCommand(Ui_Function):
    question_config = {
        '国家代码':   {'type': 'text'},
        '国家名称': {'type': 'text'},
        '团队总人数': {'type': 'text'},
        '管理员名称': {'type': 'text'},
        '管理员联系方式': {'type': 'text'},
        '管理员身份': {'type': 'text'},
        }
    def __init__(self, parent = None, **kwargs):
        super(TeamButtonCommand, self).__init__(parent, **kwargs)
        self.__service = AdminService()
        self.main_tree = self.part.get('tree')       # 主界面的tree
        self.treeview = self.parent.treeview         # 子界面的tree -- mannager 界面里的


    def add(self, **kwags):
        # 新增队伍
        win = AskUserQuestionDialog(part_dict = self.question_config,
                                    name = '新增国家队'
                                    )
        win.wait_window()
        if win.result:
            team_node = NationalTeam(*win.result)
            # # 提交数据库
            try:
                self.__service.insert_team(team_node)
                self.__service.insert_coutryAdmin(coutryID = NationalTeam.country_code, contact = NationalTeam.manager_contact)
            except Exception:
                messagebox.showinfo('提示', '添加失败')
            messagebox.showinfo('提示', '添加成功')
            self.treeview.insert_single(team_node)
            self.main_tree.update()
            self.main_tree.insert_single(team_node)
            self.main_tree.update()
        else:
            messagebox.showinfo('提示', '添加失败')

    def remove(self, **kwags):
        selection = self.treeview.get_choice_RowData(ret_type = 'all', value_type = 'text')

        if (selection is not None):
            _id = selection[1]

            if (messagebox.askyesno('确认', '确定删除？')):
                self.__service.delete_team(_id)
                self.treeview.delete(selection[0])
                self.treeview.update()
                self.main_tree.delete(selection[0])
                self.main_tree.update()
        return

    def modify(self, **kwags):
        selection = self.treeview.get_choice_columnData(kwags.get('event', None))

        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data,  item = selection
            question_name = list(self.question_config.keys())[column_index]
            column = {question_name: self.question_config[question_name]}
            win = AskUserQuestionDialog(part_dict = column,
                                        name = f'修改 {question_name}')
            win.wait_window()
            if (win.result is not None):
                coutry_code = self.treeview.item(item, 'text')
                all_data = list(all_data)
                all_data[column_index] = win.result[0]
                all_data.insert(0, coutry_code)
                selection_node = NationalTeam(*([coutry_code] + all_data))
                self.__service.modify_team(selection_node)
                self.treeview.item(item, values = all_data)
                self.main_tree.item(item, values = all_data)

    def search(self, ):
        target_string = self.parent.search_entry.get()
        if (target_string == ''):
            showerror('错误', '请输入搜索内容')
            return
        max_similarity = 0
        most_similar_item = None

        for item in self.treeview.get_children():
            row_data = self.treeview.item(item, "values")
            for cell_data in row_data:
                similarity = difflib.SequenceMatcher(None, target_string, cell_data).ratio()
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_item = item

        if most_similar_item:
            self.treeview.selection_set(most_similar_item)
            self.treeview.see(most_similar_item)
        else:
            showerror('没有找到', '没有找到与输入相似的项')

    def manny(self, **kwags):
        file_path = askopenfilename(title = '选择 Excel 文件',
                                               filetypes = [('Excel files', '*.xlsx')]
                                               )
        if (file_path):
            columns = Column.team.value
            reader = ReadTemplate(file_path)
            data = reader.read(columns, NationalTeam)
            self.__service.insert_teammany(data)
            self.treeview.insert_manny(data)
            self.main_tree.update()
            self.main_tree.insert_manny(data)
            self.main_tree.update()

    def template(self):
        options = {
            'defaultextension': '.xlsx',
            'filetypes':        [('Excel files', '.xlsx'), ('All files', '.*')],
            'initialfile':      '批量添加国家队模板.xlsx',
            'title':            '选择保存位置'
            }
        filename = asksaveasfilename(**options)
        if (filename):
            writer = MakeTemplate(Column.team.value, filename)
            writer.make()


class MedalButtonCommand(Ui_Function):
    modify_config = {
        '金牌国家代码' : {'type': 'text'},
        '金牌运动员ID' : {'type': 'text'},
        '银牌国家代码' : {'type': 'text'},
        '银牌运动员ID' : {'type': 'text'},
        '铜牌国家代码' : {'type': 'text'},
        '铜牌运动员ID' : {'type': 'text'}
        }

    def __init__(self, parent = None, **kwargs):
        super(MedalButtonCommand, self).__init__(parent, **kwargs)
        self.__service = AdminService()
        self.rank_tree = self.part.get('tree')  # 主界面的tree
        self.gold_tree = self.part.get('gold_tree')  # 主界面的金牌榜
        self.treeview = self.parent.treeview  # 子界面的tree -- mannager 界面里的
        self.__gold_var = StringVar(value = '')
        self.__silver_var = StringVar(value = '')
        self.__bronze_var = StringVar(value = '')

        self.question_config = {
        '比赛ID/名称' : {'type' : 'text'},
        '金牌/国家代码': {'type':'multi-part',
                          'cols' : [
            {'type': 'text'},
            {'type': 'label', 'text': '运动员名称'},
            {'type': 'text'},
            {'type': 'button', 'text': '精彩时刻', 'command' : lambda : self.__choice__(1)}
            ]},
        '银牌/国家代码': {'type':'multi-part',
                          'cols' : [
            {'type': 'text'},
            {'type': 'label', 'text': '运动员名称'},
            {'type': 'text'},
            {'type': 'button', 'text': '精彩时刻', 'command' : lambda : self.__choice__(2)}
            ]},
        '铜牌/国家代码': {'type':'multi-part',
                          'cols' : [
            {'type': 'text'},
            {'type': 'label', 'text': '运动员名称'},
            {'type': 'text'},
            {'type': 'button', 'text': '精彩时刻', 'command' : lambda : self.__choice__(3)}
            ]},
        }
        # 把tree的国家ID分出来
        # self.getCode_from_Item()

    def getCode_from_Item(self):
        self.item_CountryDict = {}
        for rank_item, gold_item in zip(self.rank_tree.get_children(),
                                                   self.gold_tree.get_children(),

                                                   ):
            rank_data = self.rank_tree.item(rank_item, 'values')
            gold_data = self.gold_tree.item(gold_item, 'values')

            rank_country_code = rank_data[1]
            gold_country_code = gold_data[1]

            # 用于存储每个国家代码下的不同榜单信息的子字典
            if rank_country_code not in self.item_CountryDict:
                self.item_CountryDict[rank_country_code] = {}

            # 存储奖牌榜信息
            self.item_CountryDict[rank_country_code]['rank'] = {
                'item':   rank_item,
                'gold':   rank_data[2],
                'silver': rank_data[3],
                'bronze': rank_data[4],
                'count':  rank_data[5]
            }

            # 存储金牌榜信息
            self.item_CountryDict[gold_country_code]['gold'] = {
                'item':   gold_item,
                'gold':   gold_data[2],
                'silver': gold_data[3],
                'bronze': gold_data[4],
                'count':  gold_data[5]
            }
    def __choice__(self, _cls):
        file_path = askopenfilename(filetypes = [("MP4 files", "*.mp4"), ("All files", "*.*")])
        if file_path:
            if (_cls == 1):
                self.__gold_var.set(file_path)
            elif (_cls == 2):
                self.__silver_var.set(file_path)
            elif (_cls == 3):
                self.__bronze_var.set(file_path)

    def __update_rank__(self, country_code, new_gold, new_silver, new_bronze, new_count):
        # 更新奖牌榜
        self.__update_specific_rank__('rank', country_code, new_gold, new_silver, new_bronze, new_count)
        # 更新金牌榜
        self.__update_specific_rank__('gold', country_code, new_gold, new_silver, new_bronze, new_count)

    def __update_specific_rank__(self, rank_type, country_code, new_gold, new_silver, new_bronze, new_count):
        # 更新内存中的数据
        self.item_CountryDict[country_code][rank_type]['gold'] = new_gold
        self.item_CountryDict[country_code][rank_type]['silver'] = new_silver
        self.item_CountryDict[country_code][rank_type]['bronze'] = new_bronze
        self.item_CountryDict[country_code][rank_type]['count'] = new_count

        # 更新 Treeview 中的数据
        item_id = self.item_CountryDict[country_code][rank_type]['item']
        if rank_type == 'rank':
            self.rank_tree.item(item_id, values = (new_gold, new_silver, new_bronze, new_count))
        elif rank_type == 'gold':
            self.gold_tree.item(item_id, values = (new_gold, new_silver, new_bronze, new_count))

    def __get_new_medal_count(self, country_code, gold = 0, silver = 0, bronze = 0):
        if country_code in self.item_CountryDict:
            new_gold = self.item_CountryDict[country_code]['rank']['gold'] + gold
            new_silver = self.item_CountryDict[country_code]['rank']['silver'] + silver
            new_bronze = self.item_CountryDict[country_code]['rank']['bronze'] + bronze
            new_count = self.item_CountryDict[country_code]['rank']['count'] + (gold + silver + bronze)

            return new_gold, new_silver, new_bronze, new_count
        else:
            # 国家代码不存在于字典中
            return None

    def add(self, **kwags):
        win = AskUserQuestionDialog(part_dict = self.question_config,
                                    name = '新增奖牌信息'
                                    )
        win.wait_window()

        record_path = [self.__gold_var.get(), self.__silver_var.get(), self.__bronze_var.get()]

        if win.result and all(record_path):
            race_id =  win.result[0]
            gold_code, gold_player = win.result[1]
            silver_code, silver_player = win.result[2]
            bronze_code, bronze_player = win.result[3]
            try:
                m = MedalInsertResponse(race_id = race_id,
                                        gold_code = gold_code,
                                        gold_player = gold_player,
                                        silver_code = silver_code,
                                        silver_player = silver_player,
                                        bronze_code = bronze_code,
                                        bronze_player = bronze_player
                                        )
            except ValueError:
                messagebox.showinfo('提示', '添加失败, 请检查信息是否完整')
                return


            race_name = self.__service.insert_medal(m)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(copy_and_rename_files, record_path, race_id, race_name,
                                [gold_player, silver_player, bronze_player]
                                )
                # 更新金牌榜和奖牌榜
            # new_gold, new_silver, new_bronze, new_count = self.__get_new_medal_count(gold_code, gold = 1)
            # self.__update_rank__(gold_code, new_gold, new_silver, new_bronze, new_count)
            #
            # new_gold, new_silver, new_bronze, new_count = self.__get_new_medal_count(silver_code, silver = 1)
            # self.__update_rank__(silver_code, new_gold, new_silver, new_bronze, new_count)
            #
            # new_gold, new_silver, new_bronze, new_count = self.__get_new_medal_count(bronze_code, bronze = 1)
            # self.__update_rank__(bronze_code, new_gold, new_silver, new_bronze, new_count)
            self.treeview.insert_single(m)
            messagebox.showinfo('提示', '添加成功')
        else:
            messagebox.showinfo('提示', '添加失败, 请检查信息是否完整')


    def remove(self, **kwags):
        selection = self.treeview.get_choice_RowData('all')
        if (selection is not None):
            item, value = selection
            if (messagebox.askyesno('确认', '确定删除？')):
                response = MedalLogResponse(*value)
                medal_node = self.__service.delete_medal_info(response)
                self.treeview.delete(selection[0])
                self.treeview.update()
        return

    def modify(self, **kwags):
        selection = self.treeview.get_choice_columnData(kwags.get('event', None))

        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data, item = selection
            if (column_index == 0 or column_index == 1):
                showerror(title = '提示', message = '不能修改比赛ID或名称，请前往比赛管理设置')
                return
            coutry_code = self.treeview.item(item, 'text')

            question_name = list(self.modify_config.keys())[column_index - 2]
            # 生成提问窗口
            column = {question_name: self.modify_config[question_name]}
            win = AskUserQuestionDialog(part_dict = column,
                                        name = f'修改 {question_name}')
            win.wait_window()

            if win.result is not None:
                result = win.result[0]

                current_data = MedalLogResponse(*all_data)
                new_data = MedalLogResponse(*all_data)

                # 创建一个映射，将 column_index 映射到相应的属性名称
                column_to_attribute = {
                    2: "gold_country_code",
                    3: "gold_player_id",
                    4: "silver_country_code",
                    5: "silver_player_id",
                    6: "bronze_country_code",
                    7: "bronze_player_id",
                    }

                # 使用 setattr 动态设置属性
                attr_name = column_to_attribute.get(column_index)
                if attr_name:
                    setattr(new_data, attr_name, result)
                self.__service.update_medal_info(current_data, new_data)
                self.treeview.item(item, values = new_data.to_tuple())
                # self.main_tree.item(item, values = new_data)

    def search(self, ):
        target_string = self.parent.search_entry.get()
        if (target_string == ''):
            showerror('错误', '请输入搜索内容')
            return
        max_similarity = 0
        most_similar_item = None

        for item in self.treeview.get_children():
            row_data = self.treeview.item(item, "values")
            for cell_data in row_data:
                similarity = difflib.SequenceMatcher(None, target_string, cell_data).ratio()
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_item = item

        if most_similar_item:
            self.treeview.selection_set(most_similar_item)
            self.treeview.see(most_similar_item)
        else:
            showerror('没有找到', '没有找到与输入相似的项')


class AdminButtonCommand(Ui_Function):
    question_config = {
        '管理员账号': {'type': 'text'},
        '管理员名称': {'type': 'text'},
        '管理员联系方式': {'type': 'text'},
        }

    def __init__(self, parent = None, **kwargs):
        super(AdminButtonCommand, self).__init__(parent, **kwargs)
        self.__service = AdminService()
        self.main_tree = self.part.get('tree')       # 主界面的tree
        self.treeview = self.parent.treeview         # 子界面的tree -- mannager 界面里的

    def add(self, **kwags):
        win = AskUserQuestionDialog(part_dict = self.question_config,
                                    name = '新增管理员用户'
                                    )
        win.wait_window()
        if win.result:
            username, public_userid, user_contact = win.result
            user_node = User(group_id = 'Admin',
                             username = username,
                             password_hash = '123456',
                             role = 0,
                             public_userid = public_userid,
                             user_contact = user_contact,
                             )
            # # 提交数据库
            try:
                self.__service.insert_Adminuser(user_node)
            except Exception:
                messagebox.showinfo('提示', '添加失败, ID重复')
            messagebox.showinfo('提示', '添加成功')
            self.treeview.insert_single(user_node)
            self.main_tree.update()
            self.main_tree.insert_single(user_node)
            self.main_tree.update()
        else:
            messagebox.showinfo('提示', '添加失败')

    def remove(self, **kwags):
        selection = self.treeview.get_choice_RowData('all')
        if (selection is not None):
            _id = selection[1][0]

            if (messagebox.askyesno('确认', '确定删除？')):
                self.__service.delete_admin(UserDeleteResponse(_id))
                self.treeview.delete(selection[0])
                self.treeview.update()
                self.main_tree.delete(selection[0])
                self.main_tree.update()
        return

    def modify(self, **kwags):
        selection = self.treeview.get_choice_columnData(kwags.get('event', None))

        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data,  item = selection
            if (column_index == 0):
                showerror('不可修改', '不可修改 用户账号')
                return
            question_name = list(self.question_config.keys())[column_index]
            column = {question_name: self.question_config[question_name]}
            win = AskUserQuestionDialog(part_dict = column,
                                        name = f'修改 {question_name}')
            win.wait_window()
            if (win.result is not None):
                before = all_data
                index = before[column_index]
                all_data = list(all_data)
                all_data[column_index] = win.result[0]
                selection_node = UserModifyResponse(public_userid = all_data[0],
                                                    username = all_data[1],
                                                    user_contact = all_data[2],)
                self.__service.modify_admin(selection_node)
                self.treeview.item(item, values = all_data)
                self.main_tree.item(item, values = all_data)

    def search(self, ):
        target_string = self.parent.search_entry.get()
        if (target_string == ''):
            showerror('错误', '请输入搜索内容')
            return
        max_similarity = 0
        most_similar_item = None

        for item in self.treeview.get_children():
            row_data = self.treeview.item(item, "values")
            for cell_data in row_data:
                similarity = difflib.SequenceMatcher(None, target_string, cell_data).ratio()
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_item = item

        if most_similar_item:
            self.treeview.selection_set(most_similar_item)
            self.treeview.see(most_similar_item)
        else:
            showerror('没有找到', '没有找到与输入相似的项')

    def manny(self, **kwags):
        file_path = askopenfilename(title = '选择 Excel 文件',
                                               filetypes = [('Excel files', '*.xlsx')]
                                               )
        if (file_path):
            columns = Column.admin.value
            reader = ReadTemplate(file_path)
            data = reader.read(columns, UserAddAdminResponse)
            self.__service.insert_mannyAdmin(data)
            self.treeview.insert_manny(data)
            self.main_tree.update()
            self.main_tree.insert_manny(data)
            self.main_tree.update()

    def template(self):
        options = {
            'defaultextension': '.xlsx',
            'filetypes':        [('Excel files', '.xlsx'), ('All files', '.*')],
            'initialfile':      '批量添加管理员模板.xlsx',
            'title':            '选择保存位置'
            }
        filename = asksaveasfilename(**options)
        if (filename):
            writer = MakeTemplate(Column.admin.value, filename)
            writer.make()
