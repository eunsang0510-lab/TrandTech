from PIL import Image, ImageDraw, ImageFont
import os
import math
from datetime import datetime


def get_theme_by_keywords(keywords: list) -> str:
    """키워드 기반 테마 선택"""
    keyword_str = " ".join(keywords).lower()

    if any(k in keyword_str for k in ["ai", "인공지능", "llm", "gpt", "neural", "machine learning", "딥러닝"]):
        return "ai"
    elif any(k in keyword_str for k in ["배터리", "battery", "ess", "에너지저장", "충전"]):
        return "battery"
    elif any(k in keyword_str for k in ["반도체", "chip", "semiconductor", "칩", "wafer", "팹"]):
        return "semiconductor"
    elif any(k in keyword_str for k in ["클라우드", "cloud", "서버", "server", "aws", "azure"]):
        return "cloud"
    elif any(k in keyword_str for k in ["로봇", "robot", "자동화", "automation"]):
        return "robot"
    elif any(k in keyword_str for k in ["바이오", "bio", "dna", "헬스", "health", "의료"]):
        return "bio"
    elif any(k in keyword_str for k in ["우주", "space", "위성", "satellite", "rocket"]):
        return "space"
    elif any(k in keyword_str for k in ["전기차", "ev", "자동차", "car", "vehicle", "tesla"]):
        return "ev"
    elif any(k in keyword_str for k in ["블록체인", "blockchain", "crypto", "web3", "nft"]):
        return "blockchain"
    elif any(k in keyword_str for k in ["보안", "security", "해킹", "hack", "cyber"]):
        return "security"
    else:
        return "ai"


def draw_ai_pattern(draw, width, height):
    nodes = [
        (420, 40), (500, 60), (540, 30), (460, 80),
        (580, 120), (620, 180), (640, 140), (660, 100),
        (460, 150), (540, 200), (500, 220),
        (580, 260), (640, 240), (440, 270),
        (540, 300), (620, 290)
    ]
    connections = [
        (0, 4), (1, 4), (1, 5), (4, 5), (5, 7),
        (8, 9), (9, 5), (10, 11), (11, 5),
        (13, 14), (14, 11), (14, 15), (11, 12)
    ]
    for i, j in connections:
        x1, y1 = nodes[i]
        x2, y2 = nodes[j]
        draw.line([(x1, y1), (x2, y2)], fill="#0044cc", width=1)

    bright_connections = [(0, 1), (1, 4), (4, 5), (5, 9), (9, 11), (11, 14)]
    for i, j in bright_connections:
        x1, y1 = nodes[i]
        x2, y2 = nodes[j]
        draw.line([(x1, y1), (x2, y2)], fill="#0066ff", width=2)

    for i, (x, y) in enumerate(nodes):
        if i in [1, 4, 5, 9, 11, 14]:
            draw.ellipse([x-10, y-10, x+10, y+10], fill="#003399")
            draw.ellipse([x-6, y-6, x+6, y+6], fill="#0066ff")
        else:
            draw.ellipse([x-5, y-5, x+5, y+5], fill="#0044cc")


def draw_battery_pattern(draw, width, height):
    cx, cy = 560, 160
    draw.rectangle([cx-60, cy-30, cx+60, cy+30], outline="#00cc44", width=2)
    draw.rectangle([cx+60, cy-10, cx+70, cy+10], fill="#00cc44")
    for i in range(3):
        x = cx - 45 + i * 35
        draw.rectangle([x, cy-20, x+20, cy+20], fill="#00cc44", outline="#00aa33", width=1)
        fill_h = 40 - i * 8
        draw.rectangle([x+2, cy+18-fill_h, x+18, cy+18], fill="#00ff66")

    for i in range(4):
        y = cy + 50 + i * 25
        draw.line([(cx-80, y), (cx+80, y)], fill="#00aa33", width=1)
        draw.ellipse([cx-5, y-4, cx+5, y+4], fill="#00cc44")

    draw.line([(cx, cy+30), (cx, cy+50)], fill="#00cc44", width=2)
    draw.line([(cx-80, cy+50), (cx+80, cy+50)], fill="#00cc44", width=2)

    for i in range(3):
        x = cx - 60 + i * 60
        draw.line([(x, cy+50), (x, cy+70)], fill="#00cc44", width=1)
        draw.rectangle([x-15, cy+70, x+15, cy+90], outline="#00cc44", width=1)

    import random
    for _ in range(15):
        x = random.randint(420, 680)
        y = random.randint(20, 340)
        draw.ellipse([x-1, y-1, x+1, y+1], fill="#00cc44")


def draw_semiconductor_pattern(draw, width, height):
    cx, cy = 550, 170
    draw.rectangle([cx-55, cy-55, cx+55, cy+55], outline="#cc6600", width=2)
    draw.rectangle([cx-40, cy-40, cx+40, cy+40], outline="#aa4400", width=1)

    for i in range(6):
        y = cy - 35 + i * 14
        draw.line([(cx-55, y), (cx-75, y)], fill="#cc6600", width=1)
        draw.line([(cx+55, y), (cx+75, y)], fill="#cc6600", width=1)

    for i in range(4):
        x = cx - 30 + i * 20
        draw.line([(x, cy-55), (x, cy-70)], fill="#cc6600", width=1)
        draw.line([(x, cy+55), (x, cy+70)], fill="#cc6600", width=1)

    for i in range(3):
        for j in range(3):
            x = cx - 25 + i * 25
            y = cy - 25 + j * 25
            draw.rectangle([x-8, y-8, x+8, y+8], fill="#cc6600", outline="#ff8800", width=1)

    import random
    for i in range(20):
        x = random.randint(420, 680)
        y = random.randint(20, 320)
        draw.line([(x, y), (x+random.randint(5, 20), y)], fill="#cc4400", width=1)


def draw_cloud_pattern(draw, width, height):
    cx, cy = 550, 120

    def draw_cloud(cx, cy, size):
        draw.ellipse([cx-size, cy-size//2, cx+size, cy+size//2], outline="#00aacc", width=2)
        draw.ellipse([cx-size//2-10, cy-size*2//3, cx+size//2+10, cy+size//3], outline="#0088aa", width=1)
        draw.ellipse([cx-size*2//3, cy-size//3, cx+size//3, cy+size*2//3], outline="#0088aa", width=1)

    draw_cloud(cx, cy, 50)

    servers = [(470, 200), (550, 220), (630, 200)]
    for sx, sy in servers:
        draw.line([(cx, cy+25), (sx, sy-15)], fill="#00aacc", width=1)
        draw.rectangle([sx-25, sy-15, sx+25, sy+15], outline="#00aacc", width=1)
        for k in range(3):
            draw.line([(sx-20, sy-8+k*8), (sx+20, sy-8+k*8)], fill="#006688", width=1)
        draw.ellipse([sx+15, sy-10, sx+20, sy-5], fill="#00cc88")

    for i in range(3):
        for j in range(2):
            x = 430 + i * 80
            y = 260 + j * 30
            draw.rectangle([x-20, y-8, x+20, y+8], outline="#00aacc", width=1)


def draw_robot_pattern(draw, width, height):
    cx, cy = 550, 150
    draw.rectangle([cx-25, cy-45, cx+25, cy-15], outline="#cc00aa", width=2)
    draw.ellipse([cx-10, cy-38, cx, cy-28], fill="#cc00aa")
    draw.ellipse([cx, cy-38, cx+10, cy-28], fill="#cc00aa")
    draw.rectangle([cx-30, cy-15, cx+30, cy+30], outline="#cc00aa", width=2)

    for i in range(3):
        draw.line([(cx-25, cy-5+i*12), (cx+25, cy-5+i*12)], fill="#aa0088", width=1)

    draw.line([(cx-30, cy-5), (cx-55, cy-20)], fill="#cc00aa", width=2)
    draw.line([(cx-55, cy-20), (cx-70, cy+10)], fill="#cc00aa", width=2)
    draw.ellipse([cx-75, cy+5, cx-60, cy+20], fill="#cc00aa")

    draw.line([(cx+30, cy-5), (cx+55, cy-20)], fill="#cc00aa", width=2)
    draw.line([(cx+55, cy-20), (cx+70, cy+10)], fill="#cc00aa", width=2)
    draw.ellipse([cx+60, cy+5, cx+75, cy+20], fill="#cc00aa")

    draw.line([(cx-15, cy+30), (cx-15, cy+60)], fill="#cc00aa", width=2)
    draw.line([(cx+15, cy+30), (cx+15, cy+60)], fill="#cc00aa", width=2)
    draw.line([(cx-15, cy+60), (cx-25, cy+85)], fill="#cc00aa", width=2)
    draw.line([(cx+15, cy+60), (cx+25, cy+85)], fill="#cc00aa", width=2)

    for i in range(8):
        angle = i * 45
        x = cx + 100 * math.cos(math.radians(angle))
        y = cy + 100 * math.sin(math.radians(angle))
        draw.ellipse([x-2, y-2, x+2, y+2], fill="#cc00aa")


def draw_bio_pattern(draw, width, height):
    cx = 540
    for i in range(20):
        t = i / 19
        y = 30 + t * 300
        x1 = cx - 40 * math.sin(t * math.pi * 3)
        x2 = cx + 40 * math.sin(t * math.pi * 3)

        if i > 0:
            t_prev = (i-1) / 19
            y_prev = 30 + t_prev * 300
            x1_prev = cx - 40 * math.sin(t_prev * math.pi * 3)
            x2_prev = cx + 40 * math.sin(t_prev * math.pi * 3)
            draw.line([(x1_prev, y_prev), (x1, y)], fill="#00cc88", width=2)
            draw.line([(x2_prev, y_prev), (x2, y)], fill="#00aa66", width=2)

        if i % 3 == 0:
            draw.line([(x1, y), (x2, y)], fill="#00cc88", width=1)
            draw.ellipse([x1-3, y-3, x1+3, y+3], fill="#00ff88")
            draw.ellipse([x2-3, y-3, x2+3, y+3], fill="#00ff88")


def draw_space_pattern(draw, width, height):
    cx, cy = 560, 170
    draw.ellipse([cx-40, cy-40, cx+40, cy+40], outline="#6600ff", width=2)
    draw.ellipse([cx-25, cy-25, cx+25, cy+25], outline="#4400cc", width=1)
    draw.ellipse([cx-10, cy-10, cx+10, cy+10], fill="#6600ff", outline="#8844ff", width=1)
    draw.ellipse([cx-70, cy-20, cx+70, cy+20], outline="#6600ff", width=1)

    import random
    for _ in range(30):
        x = random.randint(420, 680)
        y = random.randint(20, 320)
        size = random.randint(1, 3)
        draw.ellipse([x-size, y-size, x+size, y+size], fill="#8844ff")

    draw.ellipse([cx+65, cy-5, cx+80, cy+10], fill="#6600ff")
    draw.ellipse([cx-80, cy-8, cx-60, cy+8], fill="#4400cc")

    for angle in range(0, 360, 30):
        x = cx + 90 * math.cos(math.radians(angle))
        y = cy + 25 * math.sin(math.radians(angle))
        draw.ellipse([x-1, y-1, x+1, y+1], fill="#6600ff")


def draw_ev_pattern(draw, width, height):
    cx, cy = 540, 160
    body_points = [
        (cx-80, cy), (cx-60, cy-30), (cx-20, cy-40),
        (cx+20, cy-40), (cx+60, cy-30), (cx+80, cy),
        (cx+80, cy+20), (cx-80, cy+20)
    ]
    draw.polygon(body_points, outline="#ffcc00", width=2)
    draw.ellipse([cx-60, cy+15, cx-30, cy+45], outline="#ffcc00", width=2)
    draw.ellipse([cx-50, cy+25, cx-40, cy+35], fill="#ffcc00", outline="#ffaa00", width=1)
    draw.ellipse([cx+30, cy+15, cx+60, cy+45], outline="#ffcc00", width=2)
    draw.ellipse([cx+40, cy+25, cx+50, cy+35], fill="#ffcc00", outline="#ffaa00", width=1)
    draw.line([(cx, cy-40), (cx, cy-65)], fill="#ffcc00", width=2)
    draw.line([(cx-30, cy-65), (cx+30, cy-65)], fill="#ffcc00", width=2)
    draw.ellipse([cx-5, cy-70, cx+5, cy-60], fill="#ffcc00")

    for i in range(5):
        y = cy + 60 + i * 20
        draw.line([(cx-80, y), (cx+80, y)], fill="#aa8800", width=1)


def draw_blockchain_pattern(draw, width, height):
    blocks = [
        (480, 100), (570, 100), (660, 100),
        (480, 190), (570, 190), (660, 190),
        (480, 280), (570, 280), (660, 280)
    ]
    for bx, by in blocks:
        draw.rectangle([bx-25, by-18, bx+25, by+18], outline="#ff6600", width=1)
        draw.rectangle([bx-20, by-13, bx+20, by+13], outline="#cc4400", width=1)
        draw.ellipse([bx-4, by-4, bx+4, by+4], fill="#ff6600", outline="#ff8800", width=1)

    connections = [
        (0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8),
        (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8)
    ]
    for i, j in connections:
        x1, y1 = blocks[i]
        x2, y2 = blocks[j]
        draw.line([(x1, y1), (x2, y2)], fill="#ff4400", width=1)


def draw_security_pattern(draw, width, height):
    cx, cy = 550, 160
    draw.rectangle([cx-35, cy-25, cx+35, cy+35], outline="#ff3366", width=2)
    draw.rectangle([cx-25, cy-10, cx+25, cy+25], fill="#ff3366", outline="#cc0033", width=1)
    draw.arc([cx-14, cy-45, cx+14, cy-15], start=180, end=0, fill="#ff3366", width=2)
    draw.ellipse([cx-5, cy, cx+5, cy+15], fill="#ffffff", outline="#cc0033", width=1)

    for r in [60, 90, 120]:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline="#cc0033", width=1)

    for angle in range(0, 360, 45):
        x = cx + 130 * math.cos(math.radians(angle))
        y = cy + 130 * math.sin(math.radians(angle))
        draw.ellipse([x-3, y-3, x+3, y+3], fill="#ff3366")
        draw.line([(cx, cy), (x, y)], fill="#330011", width=1)


THEME_COLORS = {
    "ai": "#0066ff",
    "battery": "#00cc44",
    "semiconductor": "#cc6600",
    "cloud": "#00aacc",
    "robot": "#cc00aa",
    "bio": "#00cc88",
    "space": "#6600ff",
    "ev": "#ffcc00",
    "blockchain": "#ff6600",
    "security": "#ff3366",
}

THEME_DRAW = {
    "ai": draw_ai_pattern,
    "battery": draw_battery_pattern,
    "semiconductor": draw_semiconductor_pattern,
    "cloud": draw_cloud_pattern,
    "robot": draw_robot_pattern,
    "bio": draw_bio_pattern,
    "space": draw_space_pattern,
    "ev": draw_ev_pattern,
    "blockchain": draw_blockchain_pattern,
    "security": draw_security_pattern,
}


def generate_og_image(title: str, date: str = None,
                      output_path: str = None,
                      keywords: list = None) -> str:
    if not date:
        date = datetime.now().strftime("%Y.%m.%d")
    if not output_path:
        os.makedirs("og_images", exist_ok=True)
        output_path = f"og_images/og-{date}.png"

    # 제목 영어만 추출
    title_en = ''.join(c for c in title if c.isascii()).strip()
    if len(title_en) < 10:
        title_en = "Today's Tech Trend Analysis"
    title = title_en

    # 키워드 기반 테마 선택
    theme = get_theme_by_keywords(keywords or [])
    color = THEME_COLORS[theme]
    draw_fn = THEME_DRAW[theme]

    width, height = 1200, 630
    img = Image.new("RGB", (width, height), color="#0a0a14")
    draw = ImageDraw.Draw(img)

    # 배경 그라디언트
    for y in range(height):
        ratio = y / height
        r = int(10 + ratio * 10)
        g = int(10 + ratio * 8)
        b = int(20 + ratio * 20)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 테마별 패턴
    draw_fn(draw, width, height)

    # 좌측 사이드바
    draw.rectangle([0, 0, 6, height], fill=color)

    # 폰트
    try:
        font_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)
        font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 52)
        font_date = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
        font_tag = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
    except:
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_date = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    # 블로그 이름 배지
    draw.rounded_rectangle([28, 28, 280, 72], radius=22, fill=color)
    draw.text((48, 38), "Tech Trend Daily", font=font_badge, fill="#ffffff")

    # 날짜
    draw.text((width - 220, 38), f"{date}", font=font_date, fill="#6688aa")

    # 구분선
    draw.rectangle([28, 88, 580, 91], fill="#1a2a4a")

    # 제목 줄바꿈
    max_width = 560
    words = title.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font_title)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    lines = lines[:3]

    y_pos = 108
    for line in lines:
        draw.text((30, y_pos + 2), line, font=font_title, fill="#000033")
        draw.text((28, y_pos), line, font=font_title, fill="#ffffff")
        y_pos += 66

    # 하단 구분선
    draw.rectangle([28, height - 110, 580, height - 107], fill="#1a2a4a")

    # 태그 (영어로만)
    tags = ["AI", "Tech Trend", "Stock Analysis", "Silicon Valley", "Global Tech"]
    tag_colors = ["#0066ff", "#6600cc", "#cc3300", "#006633", "#cc6600"]
    x_pos = 28
    for i, tag in enumerate(tags):
        bbox = draw.textbbox((0, 0), f"# {tag}", font=font_tag)
        tag_width = bbox[2] - bbox[0] + 22
        draw.rounded_rectangle(
            [x_pos, height - 90, x_pos + tag_width, height - 62],
            radius=12, fill=tag_colors[i % len(tag_colors)]
        )
        draw.text((x_pos + 11, height - 87), f"# {tag}",
                  font=font_tag, fill="#ffffff")
        x_pos += tag_width + 10

    # URL
    draw.text((28, height - 48),
              "eunsang0510-lab.github.io", font=font_date, fill="#445566")

    img.save(output_path, "PNG", quality=95)
    print(f"✅ OG 이미지 생성 완료: {output_path} (테마: {theme})")
    return output_path


if __name__ == "__main__":
    test_cases = [
        (["AI", "머신러닝"], "AI Revolution: Machine Learning Trends 2026"),
        (["배터리", "ESS"], "Battery Tech: ESS Innovation Insights"),
        (["반도체", "칩"], "Semiconductor Chip Design Future"),
        (["클라우드", "서버"], "Cloud Computing Server Architecture"),
        (["우주", "위성"], "Space Tech: Satellite Innovation"),
    ]
    for keywords, title in test_cases:
        generate_og_image(
            title=title,
            date=datetime.now().strftime("%Y.%m.%d"),
            keywords=keywords
        )