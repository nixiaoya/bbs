#coding=utf-8

from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
import math
import StringIO

from users.models import *

#--------session 处理--------
def setSession(request,user):
    Sessionkey = "user_session_key"
    user.set_login()
    if Sessionkey in request.session:
        if request.session[Sessionkey] != user.id:
            request.session.flush()
    request.session[Sessionkey] = user.id

def getSession(request):
    Sessionkey = "user_session_key"
    if Sessionkey not in request.session:
        return Anonymouse()
    else:
        username = request.session[Sessionkey]
        return User.objects.get(id=username)

def delSession(request):
    Sessionkey = "user_session_key"
    user = getSession(request)
    user.set_logout()
    del request.session[Sessionkey]

class captcha(object):
    def __init__(self,size=(160,60),font_size=40):
        '''
        @todo: 生成验证码图片
        @param size: 图片的大小，格式（宽，高），默认为(120, 30)
        @param chars: 允许的字符集合，格式字符串
        @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
        @param mode: 图片模式，默认为RGB
        @param bg_color: 背景颜色，默认为白色
        @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
        @param font_size: 验证码字体大小
        @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
        @param mix: 重合像素大小
        @param length: 验证码字符个数
        @param draw_lines: 是否划干扰线
        @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有
        效
        @param draw_points: 是否画干扰点
        @param point_chance: 干扰点出现的概率，大小范围[0, 100]
        @return: [0]: PIL Image实例
        @return: [1]: 验证码图片中的字符串
        '''
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.img_type = "GIF"
        self.mode = "RGBA"
        self.bg_color = (255,255,255)
        self.fg_color = (71,101,160)
        self.font_type = "monaco.ttf"
        self.font_size = font_size
        self.mix = 15
        self.length = 4
        self.draw_lines = True
        self.n_line = (2,4)
        self.draw_points = True
        self.point_chance = 20
        self.font = ImageFont.truetype(self.font_type, self.font_size)
        _letter_cases = "abcdefghjkmnpqrstuvwxy" # 小写字母，去除可能干扰的i，l，o，z
        _upper_cases = _letter_cases.upper() # 大写字母
        _numbers = ''.join(map(str, range(1, 10))) # 数字
        self.chars = ''.join(( _upper_cases, _numbers))

    def __rndColor(self):
        '''
        生成随机背景颜色
        '''
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    def __rndColor2(self):
        '''
        生成随机前景颜色
        '''
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def rotate(self):
        rot = self.img.rotate(random.randint(-5,5),expand=0)
        default_bg = Image.new("RGBA",self.size,self.bg_color)
        self.img = Image.composite(rot,default_bg,rot)
        #重建画布后，需要重建画笔
        self.draw = ImageDraw.Draw(self.img)

    def create_oval(self, h=0, k=0):
        '''
        画椭圆，生成曲线(提供中心点坐标，默认原点)
        '''
        a = random.randint(40,self.width/2)
        b = random.randint(10,self.height/2)
        color = self.__rndColor2()
        for t in range(-180,180):
            rad = math.pi*t/180
            x = h + a * math.cos(rad)
            y = k + a * math.sin(rad)
            self.draw.point((x,y), fill=color)

    def create_lines(self):
        '''
        绘制干扰线
        '''
        line_num = random.randint(self.n_line[0],self.n_line[1]) # 干扰线条数
        for i in range(line_num):

            #起始点(横向/纵向)
            begin1 = (random.randint(0, self.width / 5), random.randint(0, self.height))
            begin2 = (random.randint(0, self.width), random.randint(0, self.height/5))

            #结束点(横向/纵向)
            end1 = (random.randint(self.width*4/5, self.width), random.randint(0, self.height))
            end2 = (random.randint(0, self.width), random.randint(self.height*4/5, self.height))

            self.draw.line([begin1, end1], fill=self.__rndColor2(), width=1)
            self.draw.line([begin2, end2], fill=self.__rndColor2(), width=1)
            self.create_oval(random.randint(-self.width,self.width),random.randint(-self.height,self.height))

    def create_points(self):
        '''
        绘制干扰点
        '''
        chance = min(100, max(0, int(self.point_chance))) # 大小限制在[0, 100]

        for w in xrange(self.width):
            for h in xrange(self.height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    self.draw.point((w, h), fill=self.__rndColor())

    def create_strs(self):
        '''
        绘制验证码字符
        生成给定长度的字符串，返回列表格式
        '''
        c_chars = random.sample(self.chars, self.length)

        per_length = self.width/self.length
        count = 0
        for x in c_chars:
            w_tmp = count*per_length
            if count == 0:
                w = random.randint(w_tmp,w_tmp + self.mix)
            elif count == self.length:
                w = random.randint(w_tmp - self.mix, w_tmp)
            else:
                w = random.randint(w_tmp - self.mix, w_tmp + self.mix)
            h = (self.height - self.font_size)/4

            self.draw.text((w,h), x, font=self.font, fill=self.__rndColor2())
            self.rotate()

            count += 1
        
        self.strs = ''.join(c_chars)

    def gen_img(self):
        self.img = Image.new(self.mode, self.size, self.bg_color) #创建图形
        self.draw = ImageDraw.Draw(self.img)  #创建画笔
        self.create_strs()  
        if self.draw_points:
            self.create_points()
        if self.draw_lines:
            self.create_lines()
        
        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,
                0,
                0,
                0,
                1 - float(random.randint(1, 10)) / 100,
                float(random.randint(1, 2)) / 500,
                0.001,
                float(random.randint(1, 2)) / 500
        ]

        self.img = self.img.filter(ImageFilter.DETAIL) # 滤镜，边界加强（阈值更大）
