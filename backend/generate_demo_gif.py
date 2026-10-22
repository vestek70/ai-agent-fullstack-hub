"""
Generates a polished 10-second GIF animation demo for ai-agent-fullstack-hub.
Showcases:
1. User prompt entry & model selection (Gemini / Hermes)
2. Tool Calling execution (SQL query to PostgreSQL/SQLite + External API)
3. Step-by-step reasoning trace with latencies
4. Interactive Tailwind UI results: dynamic KPI cards & sortable data table
5. Tab switching to SQL inspection & live API feed
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)
GIF_PATH = os.path.join(OUTPUT_DIR, "demo.gif")
PUBLIC_GIF_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "demo.gif")

WIDTH = 800
HEIGHT = 480
FPS = 10
TOTAL_SECONDS = 10
TOTAL_FRAMES = FPS * TOTAL_SECONDS

# Colors
BG_DARK = (10, 15, 29)          # slate-950
PANEL_BG = (17, 24, 39)         # slate-900
BORDER_COLOR = (30, 41, 59)     # slate-800
CYAN_ACCENT = (6, 182, 212)     # cyan-500
CYAN_LIGHT = (103, 232, 249)    # cyan-300
PURPLE_ACCENT = (147, 51, 234)  # purple-600
GREEN_ACCENT = (34, 197, 94)    # emerald-500
TEXT_WHITE = (248, 250, 252)    # slate-50
TEXT_MUTED = (148, 163, 184)    # slate-400
TEXT_DIM = (100, 116, 139)      # slate-500
CARD_BG = (23, 32, 51)
ROW_EVEN = (19, 27, 44)
ROW_ODD = (24, 34, 55)

def get_font(size, bold=False):
    # Try system fonts
    font_names = ["segoeui.ttf", "arial.ttf", "calibri.ttf", "DejaVuSans.ttf"]
    if bold:
        font_names = ["segouib.ttf", "arialbd.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"]
    
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()

font_title = get_font(18, bold=True)
font_subtitle = get_font(12, bold=False)
font_body = get_font(13, bold=False)
font_body_bold = get_font(13, bold=True)
font_small = get_font(11, bold=False)
font_code = get_font(11, bold=False)
font_kpi_val = get_font(20, bold=True)
font_badge = get_font(10, bold=True)

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def render_frame(frame_idx: int) -> Image.Image:
    t = frame_idx / TOTAL_FRAMES  # 0.0 to 1.0
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    # 1. Top Navbar (height: 48)
    draw_rounded_rect(draw, (0, 0, WIDTH, 46), radius=0, fill=(13, 20, 36), outline=BORDER_COLOR)
    
    # Logo icon
    draw_rounded_rect(draw, (14, 10, 40, 36), radius=6, fill=CYAN_ACCENT)
    draw.text((21, 14), "⚡", font=font_subtitle, fill=(0, 0, 0))
    
    # Title & Badge
    draw.text((48, 11), "ai-agent-fullstack-hub", font=font_body_bold, fill=TEXT_WHITE)
    draw_rounded_rect(draw, (200, 12, 305, 32), radius=10, fill=(8, 47, 73), outline=(14, 116, 144))
    draw.text((208, 15), "Tool Calling v1.0", font=font_badge, fill=CYAN_LIGHT)
    
    # Model Selector Pill
    draw_rounded_rect(draw, (WIDTH - 270, 11, WIDTH - 120, 33), radius=6, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((WIDTH - 262, 15), "🤖 Gemini 1.5 Pro ▾", font=font_small, fill=TEXT_WHITE)
    
    # Latency badge
    draw_rounded_rect(draw, (WIDTH - 110, 11, WIDTH - 14, 33), radius=6, fill=(6, 78, 59), outline=GREEN_ACCENT)
    draw.text((WIDTH - 102, 15), "● API: 0.8ms", font=font_badge, fill=(167, 243, 208))

    # 2. Main Prompt Box Area (y: 56 to 110)
    draw_rounded_rect(draw, (14, 54, WIDTH - 14, 112), radius=10, fill=PANEL_BG, outline=BORDER_COLOR)
    
    full_prompt = "Покажи топ-5 клиентов по сумме заказов с группировкой и общей суммой"
    # Typing effect for first 20 frames (2 seconds)
    if frame_idx < 20:
        chars_to_show = int(len(full_prompt) * (frame_idx / 20))
        current_prompt = full_prompt[:chars_to_show] + ("|" if (frame_idx % 4 < 2) else "")
    else:
        current_prompt = full_prompt

    draw.text((28, 64), "💬 Промпт для автономного агента:", font=font_small, fill=TEXT_MUTED)
    draw.text((28, 82), current_prompt, font=font_body, fill=TEXT_WHITE)

    # Run button (pulsing when clicked at frame 20-25)
    btn_box = (WIDTH - 150, 68, WIDTH - 26, 102)
    btn_fill = CYAN_ACCENT if frame_idx < 22 or frame_idx > 26 else (14, 165, 233)
    draw_rounded_rect(draw, btn_box, radius=6, fill=btn_fill)
    btn_label = "Запустить" if frame_idx < 22 else ("Выполняется..." if frame_idx < 35 else "✓ Готово")
    draw.text((WIDTH - 138, 77), btn_label, font=font_body_bold, fill=(15, 23, 42))

    # 3. Dynamic content based on progress
    # Phase A: Thought & Tool Call Execution (frames 22 to 44 -> 2.2s to 4.4s)
    # Phase B: Results (KPIs + Table) (frames 45 to 75 -> 4.5s to 7.5s)
    # Phase C: SQL Inspector & API results tab (frames 76 to 100 -> 7.6s to 10.0s)

    if frame_idx < 45:
        # Execution Trace view
        draw_rounded_rect(draw, (14, 122, WIDTH - 14, HEIGHT - 32), radius=10, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((28, 134), "⚙️ Автономный конвейер вызова инструментов (Tool Calling)", font=font_body_bold, fill=CYAN_LIGHT)
        
        # Step 1: Planning
        s1_active = frame_idx >= 22
        s1_color = GREEN_ACCENT if frame_idx >= 30 else CYAN_ACCENT
        draw_rounded_rect(draw, (28, 164, WIDTH - 28, 224), radius=8, fill=(15, 23, 42), outline=s1_color)
        draw.text((40, 174), "1. Интерпретация задачи и планирование" if s1_active else "1. Ожидание...", font=font_body_bold, fill=TEXT_WHITE)
        if s1_active:
            draw.text((40, 196), "💭 Агент определил необходимость SQL агрегации по таблицам customers & orders (JOIN, SUM)", font=font_small, fill=TEXT_MUTED)

        # Step 2: Function Calling (SQL)
        s2_active = frame_idx >= 30
        s2_color = GREEN_ACCENT if frame_idx >= 40 else CYAN_ACCENT
        draw_rounded_rect(draw, (28, 236, WIDTH - 28, 314), radius=8, fill=(15, 23, 42), outline=s2_color if s2_active else BORDER_COLOR)
        draw.text((40, 246), "2. Вызов локальной функции: execute_sql_query" if s2_active else "2. Вызов функции...", font=font_body_bold, fill=TEXT_WHITE)
        if s2_active:
            draw.text((40, 268), "🛠️ SQL: SELECT c.name, c.company, c.tier, COUNT(o.id), SUM(o.total_amount) FROM customers...", font=font_code, fill=CYAN_LIGHT)
            draw.text((40, 288), "⚡ Статус: Выполнен за 0.81 мс в SQLite/PostgreSQL | 5 записей возвращено", font=font_small, fill=GREEN_ACCENT)

        # Step 3: Synthesis
        s3_active = frame_idx >= 40
        draw_rounded_rect(draw, (28, 326, WIDTH - 28, 386), radius=8, fill=(15, 23, 42), outline=CYAN_ACCENT if s3_active else BORDER_COLOR)
        draw.text((40, 336), "3. Синтез данных и извлечение KPI" if s3_active else "3. Синтез...", font=font_body_bold, fill=TEXT_WHITE)
        if s3_active:
            draw.text((40, 358), "✨ Формирование KPI карточек, таблицы и инсайтов для интерактивного интерфейса", font=font_small, fill=TEXT_MUTED)

    elif frame_idx < 76:
        # Phase B: Rich Results View (KPIs + Data Table)
        # 4 KPI Cards (y: 122 to 192)
        kpis = [
            ("Совокупная сумма", "$184,920.50", "+14.2% ↑", GREEN_ACCENT),
            ("Лидер по заказам", "TechNova Systems", "Enterprise", CYAN_ACCENT),
            ("Записей в выборке", "5 клиентов", "Top LTV", PURPLE_ACCENT),
            ("Задержка выполнения", "0.81 мс", "PostgreSQL/SQLite", GREEN_ACCENT)
        ]
        card_w = (WIDTH - 28 - 3 * 10) // 4
        for i, (label, val, sub, col) in enumerate(kpis):
            x1 = 14 + i * (card_w + 10)
            x2 = x1 + card_w
            draw_rounded_rect(draw, (x1, 122, x2, 192), radius=8, fill=CARD_BG, outline=BORDER_COLOR)
            draw.text((x1 + 10, 130), label, font=font_small, fill=TEXT_MUTED)
            draw.text((x1 + 10, 146), val, font=font_kpi_val, fill=TEXT_WHITE)
            draw.text((x1 + 10, 172), sub, font=font_badge, fill=col)

        # Table Header & Controls (y: 202)
        draw_rounded_rect(draw, (14, 200, WIDTH - 14, HEIGHT - 32), radius=8, fill=PANEL_BG, outline=BORDER_COLOR)
        
        # Tabs bar
        draw_rounded_rect(draw, (22, 208, 120, 230), radius=5, fill=CYAN_ACCENT)
        draw.text((32, 212), "📊 Таблица", font=font_small, fill=(15, 23, 42))
        
        draw_rounded_rect(draw, (128, 208, 230, 230), radius=5, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((138, 212), "⚡ Шаги агента (4)", font=font_small, fill=TEXT_MUTED)
        
        draw_rounded_rect(draw, (238, 208, 330, 230), radius=5, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((248, 212), "🔍 SQL запрос", font=font_small, fill=TEXT_MUTED)

        # Table Columns
        draw_rounded_rect(draw, (22, 238, WIDTH - 22, 262), radius=4, fill=(15, 23, 42))
        draw.text((30, 244), "Клиент", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((190, 244), "Компания", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((350, 244), "Страна", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((450, 244), "Тариф", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((540, 244), "Заказов", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((630, 244), "Сумма (USD)", font=font_body_bold, fill=TEXT_MUTED)

        # Rows
        table_rows = [
            ("TechNova Systems", "TechNova AG", "Германия", "Enterprise", "42", "$54,200.00"),
            ("Apex Cloud Inc", "Apex Cloud Sol.", "США", "Enterprise", "38", "$48,150.00"),
            ("Tokyo AI Dynamics", "Tokyo AI Labs", "Япония", "Enterprise", "29", "$34,800.00"),
            ("Sao Paulo Fintech", "SP Fintech Corp", "Бразилия", "Growth", "24", "$26,400.00"),
            ("Nordic Retail Lab", "Nordic Retail Group", "Швеция", "Growth", "19", "$21,370.50"),
        ]

        for r_i, r_data in enumerate(table_rows):
            ry = 266 + r_i * 28
            r_bg = ROW_EVEN if r_i % 2 == 0 else ROW_ODD
            draw_rounded_rect(draw, (22, ry, WIDTH - 22, ry + 26), radius=3, fill=r_bg)
            draw.text((30, ry + 6), r_data[0], font=font_body_bold, fill=TEXT_WHITE)
            draw.text((190, ry + 6), r_data[1], font=font_small, fill=TEXT_MUTED)
            draw.text((350, ry + 6), r_data[2], font=font_small, fill=TEXT_MUTED)
            # Tier pill
            tier_col = PURPLE_ACCENT if r_data[3] == "Enterprise" else CYAN_ACCENT
            draw_rounded_rect(draw, (448, ry + 4, 520, ry + 22), radius=4, fill=(15, 23, 42), outline=tier_col)
            draw.text((454, ry + 6), r_data[3], font=font_badge, fill=tier_col)
            draw.text((550, ry + 6), r_data[4], font=font_small, fill=TEXT_WHITE)
            draw.text((630, ry + 6), r_data[5], font=font_body_bold, fill=GREEN_ACCENT)

    else:
        # Phase C: SQL Inspector & Multi-Source Tool Calling View (frames 76 to 100)
        draw_rounded_rect(draw, (14, 122, WIDTH - 14, HEIGHT - 32), radius=10, fill=CARD_BG, outline=BORDER_COLOR)
        
        # Tabs bar (Active: SQL Inspector)
        draw_rounded_rect(draw, (22, 130, 140, 154), radius=5, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((32, 136), "📊 Таблица", font=font_small, fill=TEXT_MUTED)
        
        draw_rounded_rect(draw, (148, 130, 270, 154), radius=5, fill=CYAN_ACCENT)
        draw.text((158, 136), "🔍 SQL Инспектор", font=font_small, fill=(15, 23, 42))

        draw_rounded_rect(draw, (278, 130, 420, 154), radius=5, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((288, 136), "🌐 Внешние API (Crypto/GH)", font=font_small, fill=TEXT_MUTED)

        # SQL Box
        draw_rounded_rect(draw, (28, 166, WIDTH - 28, 280), radius=6, fill=(13, 17, 23), outline=(56, 189, 248))
        draw.text((40, 174), "-- Автоматически сгенерированный SQL-запрос агентом", font=font_code, fill=TEXT_DIM)
        draw.text((40, 194), "SELECT c.name, c.company, c.country, c.tier,", font=font_code, fill=(244, 114, 182))
        draw.text((40, 212), "       COUNT(o.id) as total_orders, ROUND(SUM(o.total_amount), 2) as total_spent", font=font_code, fill=CYAN_LIGHT)
        draw.text((40, 230), "FROM customers c JOIN orders o ON c.id = o.customer_id", font=font_code, fill=TEXT_WHITE)
        draw.text((40, 248), "GROUP BY c.id ORDER BY total_spent DESC LIMIT 5;", font=font_code, fill=(251, 191, 36))

        # Split Card: External API demonstration preview
        draw_rounded_rect(draw, (28, 292, WIDTH - 28, 436), radius=6, fill=(15, 23, 42), outline=BORDER_COLOR)
        draw.text((40, 302), "⚡ Поддержка внешних API (CoinGecko, GitHub, Open-Meteo, HackerNews):", font=font_body_bold, fill=CYAN_LIGHT)
        
        # Crypto rates pill
        draw_rounded_rect(draw, (40, 328, 260, 410), radius=6, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((52, 338), "🪙 Live Crypto Tool", font=font_body_bold, fill=TEXT_WHITE)
        draw.text((52, 360), "BTC: $98,420 (+3.45%)", font=font_small, fill=GREEN_ACCENT)
        draw.text((52, 380), "ETH: $3,240 (+1.82%)", font=font_small, fill=CYAN_LIGHT)

        # GitHub Repo Tool pill
        draw_rounded_rect(draw, (275, 328, 510, 410), radius=6, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((287, 338), "🐙 GitHub Search Tool", font=font_body_bold, fill=TEXT_WHITE)
        draw.text((287, 360), "Topic: ai-agents (50+ repos)", font=font_small, fill=TEXT_MUTED)
        draw.text((287, 380), "Top Stars: 28,400 ⭐", font=font_small, fill=(251, 191, 36))

        # Weather / News pill
        draw_rounded_rect(draw, (525, 328, WIDTH - 40, 410), radius=6, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((537, 338), "🌤️ Meteo & News Tool", font=font_body_bold, fill=TEXT_WHITE)
        draw.text((537, 360), "Tokyo: 18.5°C, Clear", font=font_small, fill=CYAN_LIGHT)
        draw.text((537, 380), "HackerNews: AI Agents Hot", font=font_small, fill=PURPLE_ACCENT)

    # 4. Footer Progress Bar & Status (y: HEIGHT - 24)
    draw_rounded_rect(draw, (0, HEIGHT - 24, WIDTH, HEIGHT), radius=0, fill=(10, 15, 26))
    draw.text((14, HEIGHT - 18), "GitHub: github.com/vestek70/ai-agent-fullstack-hub", font=font_badge, fill=TEXT_MUTED)
    draw.text((WIDTH - 240, HEIGHT - 18), "Next.js 16 + FastAPI + Tailwind CSS", font=font_badge, fill=CYAN_LIGHT)
    
    # Progress line at very bottom
    progress_w = int(WIDTH * t)
    draw.line([(0, HEIGHT - 2), (progress_w, HEIGHT - 2)], fill=CYAN_ACCENT, width=2)

    return img

def main():
    print(f"Generating {TOTAL_FRAMES} frames for 10-second GIF demo...")
    frames = []
    for i in range(TOTAL_FRAMES):
        f = render_frame(i)
        frames.append(f)
        if i % 20 == 0:
            print(f"Rendered frame {i}/{TOTAL_FRAMES}")

    print("Optimizing and saving animated GIF...")
    # Save GIF with 100ms per frame (10 fps = 10000ms = 10 seconds total loop)
    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=100,
        loop=0
    )
    print(f"Successfully generated: {GIF_PATH} ({os.path.getsize(GIF_PATH) / 1024:.1f} KB)")

    # Also copy to frontend public directory
    frames[0].save(
        PUBLIC_GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=100,
        loop=0
    )
    print(f"Also saved to public: {PUBLIC_GIF_PATH}")

if __name__ == "__main__":
    main()
