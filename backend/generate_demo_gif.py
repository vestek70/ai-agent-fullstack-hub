"""
Gera uma animação GIF de demonstração de 10 segundos em alta resolução para ai-agent-fullstack-hub.
Destaques:
1. Entrada de instrução do usuário em linguagem natural e seleção do modelo DeepSeek V4
2. Execução autônoma de Tool Calling (consulta SQL no PostgreSQL/SQLite + APIs externas)
3. Rastreamento detalhado dos passos de raciocínio com medição de latência em milissegundos
4. Resultados na interface moderna em Tailwind: cartões de KPIs dinâmicos e tabela ordenável
5. Alternância entre abas de consulta SQL e dados ao vivo de APIs externas
"""

import os
import sys

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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

# Cores do Design System Tailwind
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

    # 1. Barra de Navegação Superior (altura: 48)
    draw_rounded_rect(draw, (0, 0, WIDTH, 46), radius=0, fill=(13, 20, 36), outline=BORDER_COLOR)

    # Ícone do Bot
    draw_rounded_rect(draw, (14, 10, 40, 36), radius=6, fill=CYAN_ACCENT)
    draw.text((21, 14), "⚡", font=font_subtitle, fill=(0, 0, 0))

    # Título & Badge
    draw.text((48, 11), "ai-agent-fullstack-hub", font=font_body_bold, fill=TEXT_WHITE)
    draw_rounded_rect(draw, (200, 12, 315, 32), radius=10, fill=(8, 47, 73), outline=(14, 116, 144))
    draw.text((208, 15), "Tool Calling v1.0", font=font_badge, fill=CYAN_LIGHT)

    # Pílula do Modelo DeepSeek V4
    draw_rounded_rect(draw, (WIDTH - 280, 11, WIDTH - 120, 33), radius=6, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((WIDTH - 272, 15), "🧠 DeepSeek V4 ▾", font=font_small, fill=TEXT_WHITE)

    # Indicador de Latência da API
    draw_rounded_rect(draw, (WIDTH - 110, 11, WIDTH - 14, 33), radius=6, fill=(6, 78, 59), outline=GREEN_ACCENT)
    draw.text((WIDTH - 102, 15), "● API: 0.8ms", font=font_badge, fill=(167, 243, 208))

    # 2. Área da Caixa de Prompt
    draw_rounded_rect(draw, (14, 54, WIDTH - 14, 112), radius=10, fill=PANEL_BG, outline=BORDER_COLOR)

    full_prompt = "Mostre os top 5 clientes por valor total de pedidos com agrupamento e soma total"
    # Efeito de digitação nos primeiros 20 frames (2 segundos)
    if frame_idx < 20:
        chars_to_show = int(len(full_prompt) * (frame_idx / 20))
        current_prompt = full_prompt[:chars_to_show] + ("|" if (frame_idx % 4 < 2) else "")
    else:
        current_prompt = full_prompt

    draw.text((28, 64), "💬 Instrução em linguagem natural para o Agente Autônomo:", font=font_small, fill=TEXT_MUTED)
    draw.text((28, 82), current_prompt, font=font_body, fill=TEXT_WHITE)

    # Botão de Executar
    btn_box = (WIDTH - 150, 68, WIDTH - 26, 102)
    btn_fill = CYAN_ACCENT if frame_idx < 22 or frame_idx > 26 else (14, 165, 233)
    draw_rounded_rect(draw, btn_box, radius=6, fill=btn_fill)
    btn_label = "Executar" if frame_idx < 22 else ("Executando..." if frame_idx < 35 else "✓ Concluído")
    draw.text((WIDTH - 138, 77), btn_label, font=font_body_bold, fill=(15, 23, 42))

    # 3. Conteúdo Dinâmico Baseado no Progresso
    # Fase A: Raciocínio & Disparo de Tool Calling (frames 22 a 44 -> 2.2s a 4.4s)
    # Fase B: Resultados Estruturados (KPIs + Tabela) (frames 45 a 75 -> 4.5s a 7.5s)
    # Fase C: Inspetor SQL & Abas de APIs Externas (frames 76 a 100 -> 7.6s a 10.0s)

    if frame_idx < 45:
        draw_rounded_rect(draw, (14, 122, WIDTH - 14, HEIGHT - 32), radius=10, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((28, 134), "⚙️ Pipeline Autônomo de Tool Calling (DeepSeek V4)", font=font_body_bold, fill=CYAN_LIGHT)

        # Passo 1: Planejamento
        s1_active = frame_idx >= 22
        s1_color = GREEN_ACCENT if frame_idx >= 30 else CYAN_ACCENT
        draw_rounded_rect(draw, (28, 164, WIDTH - 28, 224), radius=8, fill=(15, 23, 42), outline=s1_color)
        draw.text((40, 174), "1. Interpretação da tarefa e planejamento" if s1_active else "1. Aguardando instrução...", font=font_body_bold, fill=TEXT_WHITE)
        if s1_active:
            draw.text((40, 196), "💭 DeepSeek V4 determinou consulta SQL analítica nas tabelas 'customers' e 'orders' (JOIN, SUM)", font=font_small, fill=TEXT_MUTED)

        # Passo 2: Chamada de Ferramenta (SQL)
        s2_active = frame_idx >= 30
        s2_color = GREEN_ACCENT if frame_idx >= 40 else CYAN_ACCENT
        draw_rounded_rect(draw, (28, 236, WIDTH - 28, 314), radius=8, fill=(15, 23, 42), outline=s2_color if s2_active else BORDER_COLOR)
        draw.text((40, 246), "2. Chamada de função local: execute_sql_query" if s2_active else "2. Chamada de função...", font=font_body_bold, fill=TEXT_WHITE)
        if s2_active:
            draw.text((40, 268), "🛠️ SQL: SELECT c.name, c.company, c.tier, COUNT(o.id), SUM(o.total_amount) FROM customers...", font=font_code, fill=CYAN_LIGHT)
            draw.text((40, 288), "⚡ Status: Executado em 0.81 ms no SQLite/PostgreSQL | 5 registros retornados", font=font_small, fill=GREEN_ACCENT)

        # Passo 3: Síntese
        s3_active = frame_idx >= 40
        draw_rounded_rect(draw, (28, 326, WIDTH - 28, 386), radius=8, fill=(15, 23, 42), outline=CYAN_ACCENT if s3_active else BORDER_COLOR)
        draw.text((40, 336), "3. Síntese dos dados e extração de KPIs" if s3_active else "3. Síntese...", font=font_body_bold, fill=TEXT_WHITE)
        if s3_active:
            draw.text((40, 358), "✨ Agregação de métricas de LTV, geração de cartões e renderização no dashboard", font=font_small, fill=TEXT_MUTED)

    elif frame_idx < 76:
        # Fase B: Visão Rica com KPIs + Tabela de Dados
        kpis = [
            ("Receita Total", "$184,920.50", "+14.2% ↑", GREEN_ACCENT),
            ("Cliente Líder", "TechNova Systems", "Enterprise", CYAN_ACCENT),
            ("Total de Registros", "5 clientes", "Top LTV", PURPLE_ACCENT),
            ("Latência da Query", "0.81 ms", "PostgreSQL/SQLite", GREEN_ACCENT)
        ]
        card_w = (WIDTH - 28 - 3 * 10) // 4
        for i, (label, val, sub, col) in enumerate(kpis):
            x1 = 14 + i * (card_w + 10)
            x2 = x1 + card_w
            draw_rounded_rect(draw, (x1, 122, x2, 192), radius=8, fill=CARD_BG, outline=BORDER_COLOR)
            draw.text((x1 + 10, 130), label, font=font_small, fill=TEXT_MUTED)
            draw.text((x1 + 10, 146), val, font=font_kpi_val, fill=TEXT_WHITE)
            draw.text((x1 + 10, 172), sub, font=font_badge, fill=col)

        # Cabeçalho da Tabela e Abas
        draw_rounded_rect(draw, (14, 200, WIDTH - 14, HEIGHT - 32), radius=8, fill=PANEL_BG, outline=BORDER_COLOR)

        # Abas de navegação
        draw_rounded_rect(draw, (22, 208, 120, 230), radius=5, fill=CYAN_ACCENT)
        draw.text((32, 212), "📊 Tabela", font=font_small, fill=(15, 23, 42))

        draw_rounded_rect(draw, (128, 208, 230, 230), radius=5, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((138, 212), "⚡ Passos (4)", font=font_small, fill=TEXT_MUTED)

        draw_rounded_rect(draw, (238, 208, 350, 230), radius=5, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((248, 212), "🔍 Consulta SQL", font=font_small, fill=TEXT_MUTED)

        # Colunas da Tabela em Português
        draw_rounded_rect(draw, (22, 238, WIDTH - 22, 262), radius=4, fill=(15, 23, 42))
        draw.text((30, 244), "Cliente", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((190, 244), "Empresa", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((350, 244), "País", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((450, 244), "Plano", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((540, 244), "Pedidos", font=font_body_bold, fill=TEXT_MUTED)
        draw.text((630, 244), "Total (USD)", font=font_body_bold, fill=TEXT_MUTED)

        # Linhas de Dados
        table_rows = [
            ("TechNova Systems", "TechNova AG", "Alemanha", "Enterprise", "42", "$54,200.00"),
            ("Apex Cloud Inc", "Apex Cloud Sol.", "EUA", "Enterprise", "38", "$48,150.00"),
            ("Tokyo AI Dynamics", "Tokyo AI Labs", "Japão", "Enterprise", "29", "$34,800.00"),
            ("Sao Paulo Fintech", "SP Fintech Corp", "Brasil", "Growth", "24", "$26,400.00"),
            ("Nordic Retail Lab", "Nordic Retail Group", "Suécia", "Growth", "19", "$21,370.50"),
        ]

        for r_i, r_data in enumerate(table_rows):
            ry = 266 + r_i * 28
            r_bg = ROW_EVEN if r_i % 2 == 0 else ROW_ODD
            draw_rounded_rect(draw, (22, ry, WIDTH - 22, ry + 26), radius=3, fill=r_bg)
            draw.text((30, ry + 6), r_data[0], font=font_body_bold, fill=TEXT_WHITE)
            draw.text((190, ry + 6), r_data[1], font=font_small, fill=TEXT_MUTED)
            draw.text((350, ry + 6), r_data[2], font=font_small, fill=TEXT_MUTED)

            tier_col = PURPLE_ACCENT if r_data[3] == "Enterprise" else CYAN_ACCENT
            draw_rounded_rect(draw, (448, ry + 4, 520, ry + 22), radius=4, fill=(15, 23, 42), outline=tier_col)
            draw.text((454, ry + 6), r_data[3], font=font_badge, fill=tier_col)
            draw.text((550, ry + 6), r_data[4], font=font_small, fill=TEXT_WHITE)
            draw.text((630, ry + 6), r_data[5], font=font_body_bold, fill=GREEN_ACCENT)

    else:
        # Fase C: Inspetor SQL & Multi-Source Tool Calling
        draw_rounded_rect(draw, (14, 122, WIDTH - 14, HEIGHT - 32), radius=10, fill=CARD_BG, outline=BORDER_COLOR)

        # Abas de navegação
        draw_rounded_rect(draw, (22, 130, 140, 154), radius=5, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((32, 136), "📊 Tabela", font=font_small, fill=TEXT_MUTED)

        draw_rounded_rect(draw, (148, 130, 280, 154), radius=5, fill=CYAN_ACCENT)
        draw.text((158, 136), "🔍 Inspetor SQL", font=font_small, fill=(15, 23, 42))

        draw_rounded_rect(draw, (288, 130, 440, 154), radius=5, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((298, 136), "🌐 APIs Externas (Cripto/GH)", font=font_small, fill=TEXT_MUTED)

        # Caixa do Código SQL Formatado
        draw_rounded_rect(draw, (28, 166, WIDTH - 28, 280), radius=6, fill=(13, 17, 23), outline=(56, 189, 248))
        draw.text((40, 174), "-- Consulta SQL gerada autonomamente pelo DeepSeek V4", font=font_code, fill=TEXT_DIM)
        draw.text((40, 194), "SELECT c.name, c.company, c.country, c.tier,", font=font_code, fill=(244, 114, 182))
        draw.text((40, 212), "       COUNT(o.id) as total_orders, ROUND(SUM(o.total_amount), 2) as total_spent", font=font_code, fill=CYAN_LIGHT)
        draw.text((40, 230), "FROM customers c JOIN orders o ON c.id = o.customer_id", font=font_code, fill=TEXT_WHITE)
        draw.text((40, 248), "GROUP BY c.id ORDER BY total_spent DESC LIMIT 5;", font=font_code, fill=(251, 191, 36))

        # Painéis de APIs Externas
        draw_rounded_rect(draw, (28, 292, WIDTH - 28, 436), radius=6, fill=(15, 23, 42), outline=BORDER_COLOR)
        draw.text((40, 302), "⚡ Integração com APIs externas em tempo real (CoinGecko, GitHub, Open-Meteo):", font=font_body_bold, fill=CYAN_LIGHT)

        # Cripto
        draw_rounded_rect(draw, (40, 328, 260, 410), radius=6, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((52, 338), "🪙 API CoinGecko Cripto", font=font_body_bold, fill=TEXT_WHITE)
        draw.text((52, 360), "BTC: $98,420 (+3.45%)", font=font_small, fill=GREEN_ACCENT)
        draw.text((52, 380), "ETH: $3,240 (+1.82%)", font=font_small, fill=CYAN_LIGHT)

        # GitHub
        draw_rounded_rect(draw, (275, 328, 510, 410), radius=6, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((287, 338), "🐙 API GitHub Repositórios", font=font_body_bold, fill=TEXT_WHITE)
        draw.text((287, 360), "Busca: ai-agents (50+ repos)", font=font_small, fill=TEXT_MUTED)
        draw.text((287, 380), "Top Stars: 28,400 ⭐", font=font_small, fill=(251, 191, 36))

        # Clima
        draw_rounded_rect(draw, (525, 328, WIDTH - 40, 410), radius=6, fill=CARD_BG, outline=BORDER_COLOR)
        draw.text((537, 338), "🌤️ API Clima & Notícias", font=font_body_bold, fill=TEXT_WHITE)
        draw.text((537, 360), "Tóquio: 18.5°C, Limpo", font=font_small, fill=CYAN_LIGHT)
        draw.text((537, 380), "HackerNews: AI Agents Hot", font=font_small, fill=PURPLE_ACCENT)

    # 4. Rodapé e Barra de Progresso
    draw_rounded_rect(draw, (0, HEIGHT - 24, WIDTH, HEIGHT), radius=0, fill=(10, 15, 26))
    draw.text((14, HEIGHT - 18), "GitHub: github.com/vestek70/ai-agent-fullstack-hub", font=font_badge, fill=TEXT_MUTED)
    draw.text((WIDTH - 280, HEIGHT - 18), "Next.js 16 + FastAPI + DeepSeek V4 + Tailwind", font=font_badge, fill=CYAN_LIGHT)

    progress_w = int(WIDTH * t)
    draw.line([(0, HEIGHT - 2), (progress_w, HEIGHT - 2)], fill=CYAN_ACCENT, width=2)

    return img

def main():
    print(f"Gerando {TOTAL_FRAMES} quadros para o GIF de 10 segundos em Português com DeepSeek V4...")
    frames = []
    for i in range(TOTAL_FRAMES):
        f = render_frame(i)
        frames.append(f)
        if i % 20 == 0:
            print(f"Renderizado quadro {i}/{TOTAL_FRAMES}")

    print("Otimizando e salvando GIF animado...")
    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=100,
        loop=0
    )
    print(f"Sucesso: {GIF_PATH} ({os.path.getsize(GIF_PATH) / 1024:.1f} KB)")

    frames[0].save(
        PUBLIC_GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=100,
        loop=0
    )
    print(f"Copiado para o frontend público: {PUBLIC_GIF_PATH}")

if __name__ == "__main__":
    main()
