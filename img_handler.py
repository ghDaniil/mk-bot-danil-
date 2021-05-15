import os
from PIL import Image ,ImageDraw,ImageFont
import requests , glob

imgs = {
    "vs":"./img/vs.png",
    "vs_gif":"./img/vs1_gif/frame_*.jpg"
}

async def vs_create(url1:str, url2:str,r1:str,r2:str):
    vs = Image.open(os.path.join(imgs["vs"]))

    size = (150,150)

    f1 = Image.open(requests.get(url1, stream=True).raw).resize(size)
    f2 = Image.open(requests.get(url2, stream=True).raw).resize(size)

    pos1 = (vs.width//2 - f1.width*2, vs.height//2 - f1.height//2)
    pos2 = (vs.width//2 + f2.width, vs.height//2 - f2.height//2)

    vs.paste(f1, pos1)
    vs.paste(f2, pos2)
    fontsize = 50
    font = ImageFont.truetype("impact.ttf", fontsize+4)
    draw_text = ImageDraw.Draw(vs)

    draw_text.text((vs.width//2 - f1.width*2, vs.height//2 - f1.height//2+f1.height),r1,font=font,fill=('#FF0000'),)
    draw_text.text((vs.width//2 + f2.width, vs.height//2 - f2.height//2+f2.height),r2,font=font,fill=('#FF0000'))

    font = ImageFont.truetype("impact.ttf", fontsize)

    draw_text.text((vs.width//2 - f1.width*2+4, vs.height//2 - f1.height//2+f1.height+4),r1,font=font,fill=('#DCDCDC'),spacing=4)
    draw_text.text((vs.width//2 + f2.width+4, vs.height//2 - f2.height//2+f2.height+4),r2,font=font,fill=('#DCDCDC'),spacing=4)


    vs.save(os.path.join("./img", "result.png"))


async def vs_create_animated(url1:str,url2:str,r1:str,r2:str):
    vs, *img = [Image.open(path) for path in glob.glob(imgs["vs_gif"])]
    
    size = (150,150)

    f1 = Image.open(requests.get(url1, stream=True).raw).resize(size)
    f2 = Image.open(requests.get(url2, stream=True).raw).resize(size)

    pos1 = (vs.width//2 - f1.width*2 - 50, vs.height//2 - f1.height//2)
    pos2 = (vs.width//2 + f2.width + 50, vs.height//2 - f2.height//2)

    vs.paste(f1, pos1)
    vs.paste(f2, pos2)
    fontsize = 51
    font = ImageFont.truetype("impact.ttf", fontsize)
    
    print(1)
    for im in img:
        draw_text = ImageDraw.Draw(im)
        im.paste(f1,pos1)
        im.paste(f2,pos2)
        draw_text.text(
            (vs.width//2 - f1.width*2 - 50, vs.height//2 - f1.height//2+f1.height),
            r1,
            font=font,
            fill=('#DCDCDC')
        )
        draw_text.text(
            (vs.width//2 + f2.width + 50, vs.height//2 - f2.height//2+f2.height),
            r2,
            font=font,
            fill=('#DCDCDC')
        )
    vs.save(fp=os.path.join("./img/result.gif"),append_images=img, save_all = True, duration= 12, loop=0 )

