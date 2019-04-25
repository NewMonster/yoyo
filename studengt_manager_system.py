"""
    案例：学生管理系统
        1.界面视图类
        2.逻辑控制类
        3.数据模型类
        建立交互：
            界面视图<---->数据模型<---->逻辑控制
"""
class StudentModel:
    """
        创建学生基本数据属性
    """
    __slots__ = ("__id","__name","__age","__score")
    def __init__(self,id=0,name="",age=0,score=0):
        """
            定义学生数据
        :param id: 学生id，type:int
        :param name: 学生姓名，type:str
        :param age: 学生年龄，type:int
        :param score: 学生成绩，type:int
        """
        self.id = id
        self.name=name
        self.age=age
        self.score=score

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,value):
        self.__name=value

    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, value):
        self.__age= value

    @property
    def score(self):
        return self.__score
    @score.setter
    def score(self, value):
        self.__score = value

class StudentManagerController:
    """
        学生核心逻辑控制器
    """
    __slots__ = ("__list_stu")
    def __init__(self):
        """
            创建学生管理器对象
        """
        self.__list_stu =[]

    @property
    def list_stu(self):
        return self.__list_stu

    def add_student(self,stu):
        """
            添加学生对象
        :param stu: 学生对象
        :return: 无
        """
        stu.id=len(self.list_stu)+1
        self.list_stu.append(stu)

    def update_id(self):
        """
            更新学生id,当发现学生序列不连续时使用
        :return: 无
        """
        for i in range(len(self.list_stu)):
            self.list_stu[i].id=i+1

    def remove_student(self,value):
        """
            移除学生病更新序号
        :param value: 需要移除学生的编号(id)，type:int
        :return: 返回删除的结果，True or False
        """
        for item in self.list_stu:
            if item.id == value:
                self.list_stu.remove(item)
                return True
        return False

    def update_student(self,stu_info):
        """
            修改学生信息
        :param stu_info: 要进行修改的学生信息
        :return: 返回修改后的结果
        """
        for item in self.list_stu:
            if item.id == stu_info.id:
                if stu_info.name!="":
                    item.name = stu_info.name
                if stu_info.age!="":
                    item.age=int(stu_info.age)
                if stu_info.score!="":
                    item.score =int(stu_info.score)
                return True
        return False

    def refer_student(self,stu_name):
        """
            根据学生姓名查询学生信息
        :param stu_name: 学生姓名,tpye:int
        :return: 无
        """
        for item in self.list_stu:
            if item.name==stu_name:
                return item
        else:
            print("系统里没有查到此学生")

    def order_by_score(self):
        """
            对学生成绩进行将序排列，不改变原列表的顺序
        :return: 返回整理完成后的列表
        """
        order_list = self.list_stu[:]
        for i in range(len(order_list)-1):
            for j in range(i+1,len(order_list)):
                if order_list[i].score < order_list[j].score:
                    order_list[i],order_list[j]=order_list[j],order_list[i]
        return order_list

class StudentManagerView:
    """
        学生管理器视图
    """
    __slots__ = ("__controller")
    def __init__(self):
        """
            创建视图数据
        """  # 创建学生管理控制对象
        self.__controller=StudentManagerController()

    @property
    def controller(self):
        return self.__controller

    def __display_menu(self):
        """
            显示菜单
        :return: 无
        """
        print("======================================================")
        print("1)添加学生")
        print("2)显示学生")
        print("3)删除学生")
        print("4)修改学生")
        print("5)按照成绩降序显示")
        print("6)学生查询(按姓名查询)")
        print("======================================================")

    def __select_menue_item(self):
        """
            选择菜单
        :return: 无
        """
        order=int(input("请选择操作："))
        if order ==1:
            self.__input_students()
        elif order==2:
            self.__output_students()
        elif order==3:
            self.__delete_students()
        elif order ==4:
            self.__modify_students()
        elif order == 5:
            new_list=self.controller.order_by_score()
            self.__print_students(new_list)
        elif order == 6:
            name=self.__find_student_by_name()
            result=self.controller.refer_student(name)
            self.__print_single_student(result)
        else:
            print("输入错误")

    def main(self):
        """
            学生管理器入口
        :return: 无
        """
        while True:
            self.__display_menu()
            self.__select_menue_item()

    def __input_students(self):
        """
            输入学生信息
        :return: 无
        """
        while True:
            stu = StudentModel()
            stu.name=input("请输入姓名：")
            stu.age=int(input("请输入年龄："))
            stu.score=int(input("请输入成绩："))
            self.__controller.add_student(stu)
            if input("按Y继续，任意键退出：") != "y":
                break

    def __output_students(self):
        """
            打印学生信息
        :return: 无
        """
        for item in self.__controller.list_stu:
            print("学生ID：",item.id,"  学生姓名:",item.name,"  学生年龄:",item.age,"  学生成绩:",item.score)

    def __delete_students(self):
        """
            获取删除学生信息的id,返回结果
        :return: 无
        """
        while True:
            id = int(input("请输入要删除学生的ID："))
            result=self.controller.remove_student(id)
            if result:
                print("删除成功")
            else:
                print("删除失败")
            self.controller.update_id()
            if input("按Y继续删除，任意键退出：")!="y":
                break

    def __modify_students(self):
        """
            修改学生信息，获取更新后的信息
        :return: 无
        """
        while True:
            stu = StudentModel()
            while True:
                stu.id = int(input("请输入要修改学生的ID："))
                if stu.id>len(self.controller.list_stu):
                    print("输入超出范围，请重试")
                else:
                    break
            stu.name=input("请输入姓名：")
            stu.age=input("请输入年龄：")
            stu.score=input("请输入成绩：")
            result=self.__controller.update_student(stu)
            if result:
                print("修改成功")
            else:
                print("修改失败")
            if input("按Y继续删除，任意键退出：")!="y":
                break

    def __find_student_by_name(self):
        """
            获取学生姓名
        :return: 返回学生姓名
        """
        name=input("请输入要查找学生的姓名：")
        return name

    def __print_single_student(self,item):
        """
            打印单个学生信息
        :param item:单个学生对象
        :return: 无
        """
        print("学生ID：", item.id, "  学生姓名:", item.name, "  学生年龄:", item.age, "  学生成绩:", item.score)

    @staticmethod
    def __print_students(list_result):
        for item in list_result:
            print("学生ID：",item.id,"  学生姓名:",item.name,"  学生年龄:",item.age,"  学生成绩:",item.score)



# 命令执行语句
view=StudentManagerView()
view.main()


