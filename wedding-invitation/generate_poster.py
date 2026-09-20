#!/usr/bin/env python3
"""法式森系婚礼请帖长图 —— 墨绿 + 米白，全屏主图版式"""
import os
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = 750
OUT = "/workspace/wedding-invitation/invitation.png"
PDIR = "/workspace/wedding-invitation/photos"

# ===== 墨绿森系配色 =====
CREAM     = (250, 247, 240)
GREEN     = (45, 74, 50)
GREEN_MID = (74, 107, 78)
GREEN_PL  = (227, 234, 217)
GREEN_BG  = (237, 242, 230)
TEXT_DARK = (44, 58, 46)
TEXT_MID  = (94, 110, 96)
TEXT_SOFT = (147, 160, 150)
WHITE     = (255, 255, 255)
C_WHITE   = (250, 247, 240)

_FC = {}

def F(size, bold=False, serif_en=False):
    k = (size, bold, serif_en)
    if k in _FC:
        return _FC[k]
    if serif_en:
        p = ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold
             else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
    else:
        p = ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc" if bold
             else "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
    try:
        f = ImageFont.truetype(p, size, index=0) if not serif_en else ImageFont.truetype(p, size)
    except Exception:
        f = ImageFont.load_default()
    _FC[k] = f
    return f


def tsize(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]


def ctext(draw, text, y, font, fill, w=W):
    tw, _ = tsize(draw, text, font)
    draw.text(((w - tw) // 2, y), text, font=font, fill=fill)
    return tw


_imgs = {}

def photo(name):
    if name not in _imgs:
        _imgs[name] = Image.open(os.path.join(PDIR, name)).convert("RGB")
    return _imgs[name]


def fill_photo(name, bw, bh, focus=0.5):
    """cover 裁切到 bw x bh"""
    im = photo(name)
    sw, sh = im.size
    sc = max(bw / sw, bh / sh)
    nw, nh = int(sw * sc + 0.5), int(sh * sc + 0.5)
    im2 = im.resize((nw, nh), Image.LANCZOS)
    lf = (nw - bw) // 2
    tp = max(0, min(int((nh - bh) * focus), nh - bh))
    return im2.crop((lf, tp, lf + bw, tp + bh))


def paste_rounded(canvas, im, box, radius=14):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    if im.size != (bw, bh):
        im = im.resize((bw, bh), Image.LANCZOS)
    mask = Image.new('L', (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw, bh], radius=radius, fill=255)
    canvas.paste(im, (x0, y0), mask)
    return canvas


def shadow_rect(canvas, box, radius=14, alpha=52, blur=8, dy=7):
    x0, y0, x1, y1 = box
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [x0 + 4, y0 + dy, x1 + 4, y1 + dy], radius=radius, fill=(35, 57, 31, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.alpha_composite(canvas.convert('RGBA'), sh).convert('RGB')
    return out


def rule(draw, y, half=34, color=GREEN_MID, width=1):
    cx = W // 2
    draw.line([(cx - half, y), (cx + half, y)], fill=color, width=width)


def clock_icon(draw, cx, cy, color):
    r = 11
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    draw.line([(cx, cy), (cx, cy - 6)], fill=color, width=2)
    draw.line([(cx, cy), (cx + 5, cy + 3)], fill=color, width=2)


def pin_icon(draw, cx, cy, color):
    r = 8
    draw.ellipse([cx - r, cy - r - 4, cx + r, cy + r - 4], outline=color, width=2)
    draw.line([(cx - r * 0.72, cy + 2), (cx, cy + 12)], fill=color, width=2)
    draw.line([(cx + r * 0.72, cy + 2), (cx, cy + 12)], fill=color, width=2)
    draw.ellipse([cx - 2.6, cy - 6.6, cx + 2.6, cy - 1.4], fill=color)


def build():
    M = 46
    H = 7800
    img = Image.new('RGB', (W, H), CREAM)

    # ============================================================
    # 一、封面：全屏主图 + 文字压图上
    # ============================================================
    HERO_H = 1180
    hero = fill_photo("photo3.jpg", W, HERO_H, focus=0.30)

    # 渐暗遮罩（上轻下重）
    mask = Image.new('RGBA', (W, HERO_H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mask)
    for yy in range(HERO_H):
        t = yy / HERO_H
        if t < 0.28:
            a = int(100 * (1 - t / 0.28))
        elif t < 0.52:
            a = int(8 + 22 * (t - 0.28) / 0.24)
        else:
            a = int(30 + 168 * ((t - 0.52) / 0.48) ** 1.2)
        md.line([(0, yy), (W, yy)], fill=(16, 26, 18, a))
    hero = Image.alpha_composite(hero.convert('RGBA'), mask).convert('RGB')
    img.paste(hero, (0, 0))
    draw = ImageDraw.Draw(img)

    cx = W // 2
    hy = HERO_H - 396

    ctext(draw, "S A V E   T H E   D A T E", hy, F(18, serif_en=True), C_WHITE)
    hy += 50
    draw.line([(cx, hy), (cx, hy + 46)], fill=(230, 236, 226), width=1)
    hy += 64

    fn = F(58, bold=True)
    fa = F(36, serif_en=True)
    wl, _ = tsize(draw, "龙腾", fn)
    wr, _ = tsize(draw, "刘敏敏", fn)
    wa, _ = tsize(draw, "&", fa)
    g = 26
    sx = (W - (wl + g + wa + g + wr)) // 2
    draw.text((sx, hy), "龙腾", font=fn, fill=C_WHITE)
    draw.text((sx + wl + g, hy + 12), "&", font=fa, fill=C_WHITE)
    draw.text((sx + wl + g + wa + g, hy), "刘敏敏", font=fn, fill=C_WHITE)
    hy += 92

    ctext(draw, "我 们 结 婚 啦", hy, F(19), C_WHITE)
    hy += 56
    draw.line([(cx, hy), (cx, hy + 42)], fill=(228, 234, 224), width=1)
    hy += 58
    ctext(draw, "2 0 2 6 . 1 0 . 2 5", hy, F(19, serif_en=True), C_WHITE)

    # 下滑箭头
    ay = HERO_H - 54
    draw.line([(cx, ay), (cx, ay + 14)], fill=(232, 238, 228), width=1)
    draw.polygon([(cx - 7, ay + 13), (cx + 7, ay + 13), (cx, ay + 23)],
                 fill=(232, 238, 228))

    y = HERO_H

    # ============================================================
    # 二、倒计时（深绿块）
    # ============================================================
    CD_H = 466
    img.paste(Image.new('RGB', (W, CD_H), GREEN), (0, y))
    draw = ImageDraw.Draw(img)

    gy = y + 60
    ctext(draw, "C O U N T I N G   D O W N", gy, F(17, serif_en=True), (203, 219, 199))
    gy += 46
    ctext(draw, "期 待 重 逢", gy, F(32), C_WHITE)
    gy += 58
    rule(draw, gy, 34, (203, 219, 199))
    gy += 48

    now = datetime.datetime.now()
    target = datetime.datetime(2026, 10, 25, 11, 58, 0)
    delta = target - now
    days = max(0, delta.days)
    hours = max(0, delta.seconds // 3600)
    mins = max(0, (delta.seconds % 3600) // 60)

    bw, bh, gap = 104, 134, 17
    bx = (W - (bw * 4 + gap * 3)) // 2
    nums = [(str(days), "天"), (f"{hours:02d}", "时"),
            (f"{mins:02d}", "分"), ("00", "秒")]
    f_num = F(50, serif_en=True)
    f_unit = F(16)
    for i, (num, unit) in enumerate(nums):
        x0 = bx + i * (bw + gap)
        draw.rounded_rectangle([x0, gy, x0 + bw, gy + bh], radius=10,
                               outline=(240, 244, 236), width=1)
        nw_, _ = tsize(draw, num, f_num)
        draw.text((x0 + (bw - nw_) // 2, gy + 22), num, font=f_num, fill=C_WHITE)
        uw_, _ = tsize(draw, unit, f_unit)
        draw.text((x0 + (bw - uw_) // 2, gy + 88), unit, font=f_unit, fill=(214, 228, 208))
    gy += bh + 36
    ctext(draw, "Looking forward to seeing you", gy, F(21, serif_en=True), (210, 224, 204))

    y += CD_H

    # ============================================================
    # 三、婚礼时间
    # ============================================================
    ty = y + 68
    ctext(draw, "W E D D I N G   D A T E", ty, F(17, serif_en=True), GREEN_MID)
    ty += 46
    ctext(draw, "婚 礼 时 间", ty, F(32), GREEN)
    ty += 58
    rule(draw, ty, 34, GREEN_MID)
    ty += 52

    CARD_H = 380
    img = shadow_rect(img, (M, ty, W - M, ty + CARD_H), radius=16)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([M, ty, W - M, ty + CARD_H], radius=16, fill=WHITE)

    cy = ty + 42
    ctext(draw, "2 0 2 6", cy, F(17, serif_en=True), TEXT_SOFT)
    cy += 40

    f_m = F(38, serif_en=True)
    f_d = F(98, serif_en=True)
    wm, _ = tsize(draw, "October", f_m)
    wd, _ = tsize(draw, "25", f_d)
    g2 = 19
    s2 = (W - (wm + g2 + wd)) // 2
    draw.text((s2, cy + 28), "October", font=f_m, fill=GREEN)
    draw.text((s2 + wm + g2, cy), "25", font=f_d, fill=GREEN)
    cy += 122

    ctext(draw, "农历丙午年 九月十六 · 星期日", cy, F(18), TEXT_MID)
    cy += 48
    draw.line([(M + 58, cy), (W - M - 58, cy)], fill=(230, 234, 226), width=1)
    cy += 34

    icx = W // 2 - 88
    draw.ellipse([icx - 24, cy, icx + 24, cy + 48], fill=GREEN_PL)
    clock_icon(draw, icx, cy + 24, GREEN)
    draw.text((icx + 42, cy + 2), "C E R E M O N Y   T I M E",
              font=F(13, serif_en=True), fill=TEXT_SOFT)
    draw.text((icx + 42, cy + 22), "中午 11:58", font=F(24), fill=GREEN)

    y = ty + CARD_H + 76

    # ============================================================
    # 四、幸福瞬间（竖排大图）
    # ============================================================
    ctext(draw, "O U R   S T O R Y", y, F(17, serif_en=True), GREEN_MID)
    y += 46
    ctext(draw, "幸 福 瞬 间", y, F(32), GREEN)
    y += 58
    rule(draw, y, 34, GREEN_MID)
    y += 52

    for pname in ["photo1.jpg", "photo2.jpg", "photo4.jpg", "photo5.jpg"]:
        pw = W - 2 * M
        ph = int(pw * 4 / 3)
        img = shadow_rect(img, (M, y, W - M, y + ph), radius=14, alpha=46)
        draw = ImageDraw.Draw(img)
        img = paste_rounded(img, fill_photo(pname, pw, ph, focus=0.42),
                            (M, y, W - M, y + ph), radius=14)
        draw = ImageDraw.Draw(img)
        y += ph + 22
    y += 16

    ctext(draw, "山水一程 · 三生有幸", y, F(19), TEXT_MID)
    y += 40
    ctext(draw, "愿与君共赴白头 · 不离不弃", y, F(19), TEXT_MID)
    y += 78

    # ============================================================
    # 五、婚礼地点（浅绿底）
    # ============================================================
    VENUE_H = 556
    img.paste(Image.new('RGB', (W, VENUE_H), GREEN_BG), (0, y))
    draw = ImageDraw.Draw(img)

    vy = y + 66
    ctext(draw, "W E D D I N G   V E N U E", vy, F(17, serif_en=True), GREEN_MID)
    vy += 46
    ctext(draw, "婚 礼 地 点", vy, F(32), GREEN)
    vy += 58
    rule(draw, vy, 34, GREEN_MID)
    vy += 52

    VC_H = 340
    img = shadow_rect(img, (M, vy, W - M, vy + VC_H), radius=16, alpha=40)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([M, vy, W - M, vy + VC_H], radius=16, fill=WHITE)

    vy2 = vy + 42
    ctext(draw, "常德华邦国际大酒店", vy2, F(31), GREEN)
    vy2 += 50
    ctext(draw, "1楼 · 江南厅", vy2, F(20), TEXT_MID)
    vy2 += 50

    ab = (M + 30, vy2, W - M - 30, vy2 + 106)
    draw.rounded_rectangle(ab, radius=12, fill=GREEN_PL)
    pin_icon(draw, ab[0] + 30, ab[1] + 40, GREEN)
    draw.text((ab[0] + 54, ab[1] + 24), "湖南省常德市鼎城区", font=F(20), fill=TEXT_DARK)
    draw.text((ab[0] + 54, ab[1] + 58), "桃花源路与花溪路交汇处", font=F(20), fill=TEXT_DARK)

    y += VENUE_H

    # ============================================================
    # 六、结尾
    # ============================================================
    ey = y + 72
    ctext(draw, "2026.10.25", ey, F(17, serif_en=True), TEXT_SOFT)
    ey += 68
    ctext(draw, '" Two souls, one heart.', ey, F(23, serif_en=True), GREEN)
    ey += 42
    ctext(draw, 'Two lives, one love. "', ey, F(23, serif_en=True), GREEN)
    ey += 60
    ctext(draw, "愿我们的故事", ey, F(20), TEXT_MID)
    ey += 42
    ctext(draw, "从这一天开始，写下更长久的篇章", ey, F(20), TEXT_MID)
    ey += 66
    rule(draw, ey, 40, GREEN_MID)
    ey += 60
    ctext(draw, "诚 邀 莅 临", ey, F(32), GREEN)
    ey += 56
    ctext(draw, "龙腾 & 刘敏敏 · 敬邀", ey, F(20), TEXT_MID)
    ey += 54
    ctext(draw, "2026.10.25", ey, F(17, serif_en=True), TEXT_SOFT)

    final_h = min(ey + 110, H)
    img = img.crop((0, 0, W, final_h))
    img.save(OUT, 'PNG', quality=95)
    print(f"✅ 已生成: {OUT}")
    print(f"   尺寸: {img.size[0]} x {img.size[1]}")


if __name__ == "__main__":
    build()