from io import BytesIO
from django import forms
from PIL import Image, ImageDraw
from django.core.cache import cache
import requests
import random


class PlaceHolderImage(forms.Form):
    height = forms.IntegerField(min_value=1, max_value=4096)
    width = forms.IntegerField(min_value=1, max_value=4096)
    bg_color = forms.IntegerField(min_value=0, max_value=0xffffff, required=False)

    def generate(self):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        bg_color = self.cleaned_data.get('bg_color', 0)

        # 检查是否有缓存
        key = "{}.{}.{}".format(width,height,bg_color)
        content = cache.get(key)
        if content: return content

        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # 准备绘制文字
        text = '{}x{}'.format(width, height)
        tw, th = draw.textsize(text)

        # 检查文本大小够不够，不够不写字
        if tw < width and th < height:
            top = (height - th) // 2
            left = (width - tw) // 2

            r = (bg_color & 0xff0000) >> 16
            g = (bg_color & 0x00ff00) >> 8
            b = bg_color & 0x0000ff

            # 计算背景色的亮度，亮色用黑字，暗色用白字
            darkness = 255 - 0.299*r - 0.587*g - 0.114*b
            tc = (255,)*3 if darkness < 128 else (0,)*3  # RGB元组
            draw.text((left, top), text, tc)

        # 写入一个二进制文件
        content = BytesIO()
        img.save(content, 'PNG')
        content.seek(0)

        # 设置缓存。（局部性原理，最近访问的，最近还要访问。）
        cache.set(key, content, 3600)
        return content


class PixelBasedImageForm(forms.Form):
    h = forms.IntegerField(min_value=5, max_value=100)
    w = forms.IntegerField(min_value=5, max_value=100)
    cell_size = forms.IntegerField(min_value=2, max_value=50)
    color = forms.IntegerField(min_value=0, max_value=0xffffff, required=False)


class Mosaic(PixelBasedImageForm):
    def generate(self):
        h = self.cleaned_data['h']
        w = self.cleaned_data['w']
        cell_size = self.cleaned_data['cell_size']
        color = self.cleaned_data.get("color", int(random.uniform(0, 0xffffff)))

        r, g, b = (color & 0xff0000) >> 16, (color & 0x00ff00) >> 8, color & 0x0000ff

        _ = lambda: random.randint(-50, 50)
        tones = [(r+_(), g+_(), b+_()) for OvO in range(8)]

        img = Image.new('RGB',(h*(cell_size+1)+1,w*(cell_size+1)+1),color=0xffffff)
        draw = ImageDraw.Draw(img)

        for x in range(h):
            for y in range(w):
                left_top = (x * (cell_size+1)+1, y * (cell_size+1)+1)
                right_down = ((x+1) * (cell_size+1), (y+1) * (cell_size+1))
                xy = (left_top, right_down)
                fill = random.choice(tones)
                draw.rectangle(xy, fill=fill, outline=0xffffff, width=1)

        content = BytesIO()
        img.save(content, 'PNG')
        content.seek(0)

        return content


class Pixels(PixelBasedImageForm):
    def generate(self):
        h = self.cleaned_data['h']
        w = self.cleaned_data['w']
        cell_size = self.cleaned_data['cell_size']
        color = self.cleaned_data.get("color", int(random.uniform(0, 0xffffff)))

        r, g, b = (color & 0xff0000) >> 16, (color & 0x00ff00) >> 8, color & 0x0000ff

        img = Image.new('RGB',(h*(cell_size+1)+1,w*(cell_size+1)+1),color=0x999999)
        draw = ImageDraw.Draw(img)

        for x in range(h):
            for y in range(w):
                if random.random() < 0.66: continue
                left_top = (x * (cell_size+1), y * (cell_size+1))
                right_down = ((x+1) * (cell_size+1), (y+1) * (cell_size+1))
                xy = (left_top, right_down)
                draw.rectangle(xy, fill=(r, g, b))

        content = BytesIO()
        img.save(content, 'PNG')
        content.seek(0)

        return content


class HumanFace64:
    @staticmethod
    def generate():
        r = requests.get("https://thispersondoesnotexist.com/image")
        b = BytesIO(r.content)
        j = Image.open(b)
        j = j.resize((64,64))
        b.close()
        b = BytesIO()
        j.save(b, 'PNG')
        b.seek(0)
        return b




