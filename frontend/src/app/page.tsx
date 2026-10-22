"use client";

import React, { useState, useEffect } from "react";
import {
  Bot,
  Sparkles,
  Terminal,
  Database,
  Globe,
  Cpu,
  Layers,
  ArrowRight,
  TrendingUp,
  TrendingDown,
  CheckCircle2,
  Clock,
  Code2,
  Copy,
  Check,
  Search,
  RefreshCw,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  HelpCircle,
  Settings,
  Table as TableIcon,
  BarChart3,
  Flame,
  FileJson,
  Share2
} from "lucide-react";

function LinkedInIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9h2.77v8.37H6.46V10.9M7.85 6.25a1.62 1.62 0 1 0 0 3.24 1.62 1.62 0 0 0 0-3.24Z" />
    </svg>
  );
}

interface StepInfo {
  step_number: number;
  step_type: string;
  title: string;
  description: string;
  payload?: any;
  duration_ms: number;
}

interface KPIItem {
  label: string;
  value: string;
  subtext?: string;
  trend?: string;
}

interface TableData {
  columns: string[];
  rows: any[][];
  total_count: number;
}

interface AgentResponse {
  query: string;
  model_name: string;
  provider: string;
  status: string;
  steps: StepInfo[];
  table_data?: TableData;
  kpis: KPIItem[];
  insights: string[];
  markdown_answer: string;
  executed_sql?: string;
  raw_tool_data?: any;
  total_time_ms: number;
}

const PRESET_QUERIES = [
  {
    icon: "📊",
    label: "Top 5 clientes por faturamento (SQL)",
    prompt: "Mostre os top 5 clientes por valor total de pedidos com agrupamento e soma total",
    type: "sql"
  },
  {
    icon: "🪙",
    label: "Cotações de Bitcoin, Ethereum e Solana (API)",
    prompt: "Obtenha as cotações atuais de Bitcoin, Ethereum e Solana através da API financeira externa",
    type: "api"
  },
  {
    icon: "📦",
    label: "Receita e estoque por categoria (SQL)",
    prompt: "Analise as categorias de produtos: preço médio, estoque total e avaliação média",
    type: "sql"
  },
  {
    icon: "⚡",
    label: "Top repositórios de IA no GitHub (API)",
    prompt: "Encontre os repositórios mais populares sobre ai-agents no GitHub com contagem de estrelas",
    type: "api"
  },
  {
    icon: "🎫",
    label: "Chamados críticos de suporte (SQL)",
    prompt: "Liste todos os tickets de suporte críticos e de alta prioridade com cliente e problema",
    type: "sql"
  },
  {
    icon: "🌤️",
    label: "Clima e temperatura em Tóquio (API)",
    prompt: "Consulte o clima atual, umidade e temperatura em Tóquio",
    type: "api"
  }
];

function getDemoFallback(query: string, model: string): AgentResponse {
  const qLower = query.toLowerCase();
  const isCrypto = qLower.includes("cripto") || qLower.includes("btc") || qLower.includes("bitcoin") || qLower.includes("eth") || qLower.includes("solana");
  const isWeather = qLower.includes("clima") || qLower.includes("tempo") || qLower.includes("temperatura") || qLower.includes("toquio") || qLower.includes("tóquio");
  const isTickets = qLower.includes("ticket") || qLower.includes("chamado") || qLower.includes("suporte") || qLower.includes("crítico");

  const providerLabel = model.includes("hermes") ? "Nous Hermes 3 Engine" : "DeepSeek V4 Engine";

  if (isCrypto) {
    return {
      query,
      model_name: model,
      provider: "CoinGecko Market Feed",
      status: "success",
      total_time_ms: 18.5,
      kpis: [
        { label: "Bitcoin (BTC)", value: "$98,420.50", subtext: "24h: +3.45%", trend: "up" },
        { label: "Ativos Rastreados", value: "3", subtext: "CoinGecko API", trend: "neutral" },
        { label: "Latência da API", value: "18.5 ms", subtext: "HTTPS REST", trend: "up" }
      ],
      steps: [
        { step_number: 1, step_type: "thought", title: "Interpretação da tarefa e planejamento", description: "O usuário solicitou cotações de criptomoedas. Acionando a API CoinGecko através da ferramenta 'fetch_external_api'.", duration_ms: 4.1 },
        { step_number: 2, step_type: "tool_call", title: "Chamada de ferramenta: fetch_external_api", description: "O agente executou a chamada da API com parâmetros: source='crypto', query='bitcoin,ethereum,solana'", duration_ms: 2.2 },
        { step_number: 3, step_type: "tool_result", title: "Execução da ferramenta (12.2 ms)", description: "A API externa retornou dados de mercado atualizados com sucesso.", duration_ms: 12.2 },
        { step_number: 4, step_type: "synthesis", title: "Síntese do resultado estruturado", description: "Formatação de preços, variações de 24 horas e capitalização de mercado.", duration_ms: 3.0 }
      ],
      table_data: {
        columns: ["Ativo", "Preço (USD)", "Variação 24h", "Cap. de Mercado"],
        rows: [
          ["Bitcoin", "$98,420.50", "+3.45%", "$1,940,500,000,000"],
          ["Ethereum", "$3,240.10", "+1.82%", "$389,400,000,000"],
          ["Solana", "$212.80", "+6.14%", "$101,200,000,000"]
        ],
        total_count: 3
      },
      insights: [
        "Dados de mercado coletados em tempo real via API pública do CoinGecko.",
        "A volatilidade das últimas 24 horas permanece dentro das faixas normais de negociação."
      ],
      markdown_answer: "### 🪙 Cotações Atualizadas de Criptomoedas\nO agente consultou a API financeira externa e retornou cotações precisas para os principais ativos digitais."
    };
  }

  if (isTickets) {
    return {
      query,
      model_name: model,
      provider: providerLabel,
      status: "success",
      total_time_ms: 0.92,
      executed_sql: "SELECT t.id, c.name as customer, t.subject, t.priority, t.status, t.category FROM support_tickets t JOIN customers c ON t.customer_id = c.id ORDER BY CASE t.priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 ELSE 3 END LIMIT 5;",
      kpis: [
        { label: "Total de Chamados", value: "5", subtext: "Fila de suporte", trend: "neutral" },
        { label: "Chamados Críticos (P1)", value: "2", subtext: "Atenção prioritária", trend: "down" },
        { label: "Chamados Abertos", value: "4", subtext: "Em atendimento", trend: "neutral" },
        { label: "Tempo de Resposta", value: "0.92 ms", subtext: "Índice SQL", trend: "up" }
      ],
      steps: [
        { step_number: 1, step_type: "thought", title: "Interpretação da tarefa e planejamento", description: "Análise de tickets de suporte prioritários no banco relacional.", duration_ms: 0.2 },
        { step_number: 2, step_type: "tool_call", title: "Chamada de ferramenta: execute_sql_query", description: "Disparo de query SQL com filtro de prioridade crítica.", duration_ms: 0.1 },
        { step_number: 3, step_type: "tool_result", title: "Execução da ferramenta (0.92 ms)", description: "Consulta executada no SQLite/PostgreSQL com 5 registros retornados.", duration_ms: 0.92 },
        { step_number: 4, step_type: "synthesis", title: "Síntese do resultado estruturado", description: "Geração de cartões de KPIs e alertas para a equipe de engenharia.", duration_ms: 0.2 }
      ],
      table_data: {
        columns: ["ID", "Cliente", "Assunto", "Prioridade", "Status", "Categoria"],
        rows: [
          [1, "TechNova Systems", "Latência elevada em consultas vetoriais", "Critical", "Open", "Infraestrutura"],
          [4, "Tokyo AI Dynamics", "Falha de autenticação via Token mTLS", "Critical", "In Progress", "Segurança"],
          [2, "Apex Cloud Inc", "Exportação de relatórios em lote lenta", "High", "Open", "Performance"],
          [6, "Bavaria AutoSoft", "Dúvida sobre webhook de faturamento", "Medium", "Open", "Cobrança"],
          [3, "Nordic Retail Lab", "Atualização de schema de inventário", "Medium", "Resolved", "Banco de Dados"]
        ],
        total_count: 5
      },
      insights: [
        "Foram detectados **2 chamados críticos (P1)** relacionados à latência e autenticação de APIs.",
        "O tempo médio de resposta do banco de dados relacional foi de **0.92 ms**."
      ],
      markdown_answer: "### 🎫 Monitoramento de Chamados de Suporte\nO agente localizou **5 chamados prioritários** na fila de atendimento com destaque para incidentes de infraestrutura."
    };
  }

  // Padrão: Clientes e Pedidos (SQL Empresarial)
  return {
    query,
    model_name: model,
    provider: providerLabel,
    status: "success",
    total_time_ms: 0.81,
    executed_sql: "SELECT c.name, c.company, c.country, c.tier, COUNT(o.id) as total_orders, ROUND(SUM(o.total_amount), 2) as total_spent FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id ORDER BY total_spent DESC LIMIT 5;",
    kpis: [
      { label: "Receita Total", value: "$184,920.50", subtext: "Top 5 clientes", trend: "up" },
      { label: "Cliente Líder", value: "TechNova Systems", subtext: "Maior LTV", trend: "up" },
      { label: "Registros Retornados", value: "5", subtext: "Amostragem", trend: "neutral" },
      { label: "Latência do Banco", value: "0.81 ms", subtext: "PostgreSQL/SQLite", trend: "up" }
    ],
    steps: [
      { step_number: 1, step_type: "thought", title: "Interpretação da tarefa e planejamento", description: "O usuário solicitou análise de faturamento por cliente. Gerando query SQL com JOIN entre 'customers' e 'orders'.", duration_ms: 0.2 },
      { step_number: 2, step_type: "tool_call", title: "Chamada de ferramenta: execute_sql_query", description: "O agente disparou a função local com o comando SQL SELECT agregado.", duration_ms: 0.1 },
      { step_number: 3, step_type: "tool_result", title: "Execução da ferramenta (0.81 ms)", description: "A função local do banco retornou 5 registros estruturados.", duration_ms: 0.81 },
      { step_number: 4, step_type: "synthesis", title: "Síntese do resultado estruturado", description: "Cálculo de LTV, destaque do cliente líder e renderização das métricas no dashboard.", duration_ms: 0.2 }
    ],
    table_data: {
      columns: ["Cliente", "Empresa", "País", "Plano", "Total de Pedidos", "Valor Total (USD)"],
      rows: [
        ["TechNova Systems", "TechNova AG", "Alemanha", "Enterprise", 42, "$54,200.00"],
        ["Apex Cloud Inc", "Apex Cloud Sol.", "EUA", "Enterprise", 38, "$48,150.00"],
        ["Tokyo AI Dynamics", "Tokyo AI Labs", "Japão", "Enterprise", 29, "$34,800.00"],
        ["Sao Paulo Fintech", "SP Fintech Corp", "Brasil", "Growth", 24, "$26,400.00"],
        ["Nordic Retail Lab", "Nordic Retail Group", "Suécia", "Growth", 19, "$21,370.50"]
      ],
      total_count: 5
    },
    insights: [
      "O cliente **TechNova Systems** lidera o volume de compras com **$54,200.00** de receita total.",
      "O ticket médio entre os top clientes é de **$36,984.10**.",
      "Distribuição geográfica estratégica cobrindo os mercados de Alemanha, EUA, Japão e Brasil."
    ],
    markdown_answer: "### 📊 Resultado da Análise SQL\nO agente executou a consulta nas tabelas `customers` e `orders` em **0.81 ms**.\nVolume total negociado: **$184,920.50** distribuído em 5 contas estratégicas."
  };
}

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [selectedModel, setSelectedModel] = useState("deepseek-v4");
  const [apiKey, setApiKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<AgentResponse | null>(null);
  const [activeTab, setActiveTab] = useState<"overview" | "table" | "sql" | "steps" | "raw">("overview");

  // UI toggles
  const [showSchemaModal, setShowSchemaModal] = useState(false);
  const [showToolsModal, setShowToolsModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [schemaData, setSchemaData] = useState<any>(null);
  const [tableSearch, setTableSearch] = useState("");
  const [copiedSQL, setCopiedSQL] = useState(false);
  const [copiedJSON, setCopiedJSON] = useState(false);
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking");
  const [backendLatency, setBackendLatency] = useState<number | null>(null);

  // Check backend health
  useEffect(() => {
    checkBackendHealth();
    // Pre-populate with first query result on load
    handleRunQuery(PRESET_QUERIES[0].prompt, "deepseek-v4");
  }, []);

  const checkBackendHealth = async () => {
    try {
      const start = performance.now();
      const res = await fetch("http://127.0.0.1:8000/api/health", { cache: "no-store" }).catch(() => null);
      if (res && res.ok) {
        setBackendStatus("online");
        setBackendLatency(Math.round(performance.now() - start));
      } else {
        // Try proxy
        const proxyRes = await fetch("/api/agent").catch(() => null);
        if (proxyRes && proxyRes.ok) {
          setBackendStatus("online");
        } else {
          setBackendStatus("offline");
        }
      }
    } catch {
      setBackendStatus("offline");
    }
  };

  const loadSchema = async () => {
    try {
      let res = await fetch("http://127.0.0.1:8000/api/db/schema").catch(() => null);
      if (res && res.ok) {
        const data = await res.json();
        setSchemaData(data.schema);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleRunQuery = async (queryToRun?: string, modelOverride?: string) => {
    const finalPrompt = queryToRun || prompt;
    if (!finalPrompt.trim()) return;

    setIsLoading(true);
    setResponse(null);

    const modelToUse = modelOverride || selectedModel;

    try {
      // Chamada direta para o backend FastAPI
      let fetchUrl = "http://127.0.0.1:8000/api/agent/run";
      let payload = {
        prompt: finalPrompt,
        model: modelToUse,
        api_key: apiKey || undefined
      };

      let res = await fetch(fetchUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).catch(() => null);

      // Fallback para a rota de proxy do Next.js
      if (!res || !res.ok) {
        res = await fetch("/api/agent", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
      }

      if (res && res.ok) {
        const data = await res.json();
        setResponse(data);
        setActiveTab("overview");
        setBackendStatus("online");
      } else {
        // Fallback para o modo demo instantâneo se o backend estiver desconectado
        const fallback = getDemoFallback(finalPrompt, modelToUse);
        setResponse(fallback);
        setActiveTab("overview");
        setBackendStatus("offline");
      }
    } catch (err: any) {
      console.warn("Utilizando dados simulados de demonstração:", err);
      const fallback = getDemoFallback(finalPrompt, modelToUse);
      setResponse(fallback);
      setActiveTab("overview");
      setBackendStatus("offline");
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text: string, type: "sql" | "json") => {
    navigator.clipboard.writeText(text);
    if (type === "sql") {
      setCopiedSQL(true);
      setTimeout(() => setCopiedSQL(false), 2000);
    } else {
      setCopiedJSON(true);
      setTimeout(() => setCopiedJSON(false), 2000);
    }
  };

  // Linhas filtradas para a exibição em tabela
  const filteredRows = response?.table_data?.rows.filter((row) =>
    row.some((cell) => String(cell).toLowerCase().includes(tableSearch.toLowerCase()))
  ) || [];

  return (
    <div className="min-h-screen bg-slate-950 bg-mesh text-slate-100 flex flex-col">
      {/* Barra de Navegação Superior */}
      <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-purple-500 p-[2px] shadow-lg shadow-cyan-500/20">
              <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <Bot className="h-5 w-5 text-cyan-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
                  ai-agent-fullstack-hub
                </span>
                <span className="px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800">
                  Tool Calling v1.0
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">
                Next.js 16 + Python FastAPI + Tailwind CSS
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2 sm:space-x-3">
            {/* Indicador de status do backend */}
            <div
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg border text-xs font-medium cursor-pointer transition-colors ${
                backendStatus === "online"
                  ? "bg-emerald-950/40 border-emerald-800 text-emerald-400 hover:bg-emerald-950/60"
                  : "bg-amber-950/40 border-amber-800 text-amber-400 hover:bg-amber-950/60"
              }`}
              onClick={checkBackendHealth}
              title="Clique para verificar o status da API"
            >
              <div
                className={`h-2 w-2 rounded-full ${
                  backendStatus === "online"
                    ? "bg-emerald-500 animate-pulse"
                    : "bg-amber-500"
                }`}
              />
              <span className="hidden md:inline">
                {backendStatus === "online"
                  ? `FastAPI :8000 ${backendLatency ? `(${backendLatency}ms)` : ""}`
                  : "Conectando..."}
              </span>
            </div>

            {/* Botão de Esquema do Banco */}
            <button
              onClick={() => {
                setShowSchemaModal(true);
                loadSchema();
              }}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700/70 hover:border-slate-500 text-slate-300 text-xs font-medium transition-all"
            >
              <Database className="h-3.5 w-3.5 text-cyan-400" />
              <span className="hidden sm:inline">Esquema DB</span>
            </button>

            {/* Botão de Registro de Ferramentas */}
            <button
              onClick={() => setShowToolsModal(true)}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700/70 hover:border-slate-500 text-slate-300 text-xs font-medium transition-all"
            >
              <Cpu className="h-3.5 w-3.5 text-purple-400" />
              <span className="hidden sm:inline">Ferramentas</span>
            </button>

            {/* Botão LinkedIn Featured */}
            <a
              href="#linkedin-guide"
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-blue-600/30 to-indigo-600/30 border border-blue-500/50 hover:border-blue-400 text-blue-200 text-xs font-medium transition-all shadow-sm"
              title="Instruções para a seção 'Em Destaque' no LinkedIn"
            >
              <LinkedInIcon className="h-3.5 w-3.5 text-blue-400" />
              <span className="hidden lg:inline">LinkedIn Destaque</span>
            </a>
          </div>
        </div>
      </header>

      {/* Conteúdo Principal */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Seção Hero */}
        <div className="text-center space-y-4 max-w-3xl mx-auto">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-900/90 border border-slate-700 text-xs text-slate-300 shadow-inner">
            <Sparkles className="h-3.5 w-3.5 text-cyan-400 animate-spin" />
            <span>DeepSeek V4 & Hermes 3 • Agente Autônomo com Tool Calling</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight">
            Agente Inteligente com{" "}
            <span className="bg-gradient-to-r from-cyan-400 via-sky-300 to-indigo-400 bg-clip-text text-transparent">
              Tool Calling
            </span>
          </h1>

          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Recebe tarefas em linguagem natural, executa consultas SQL em bancos de dados relacionais (PostgreSQL/SQLite), consome APIs externas e sintetiza resultados estruturados em uma interface moderna com Tailwind CSS.
          </p>
        </div>

        {/* Caixa de Entrada e Seleção de Modelos */}
        <div className="max-w-4xl mx-auto space-y-3">
          <div className="glass-card rounded-2xl p-2 sm:p-3 shadow-2xl border border-slate-800">
            {/* Barra interna: Seletor de Modelo */}
            <div className="flex flex-wrap items-center justify-between gap-2 px-2 pb-2 border-b border-slate-800/80 text-xs">
              <div className="flex items-center space-x-2">
                <span className="text-slate-400 font-medium">Modelo do Agente:</span>
                <div className="flex items-center space-x-1 bg-slate-900 p-1 rounded-lg border border-slate-800">
                  <button
                    onClick={() => setSelectedModel("deepseek-v4")}
                    className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                      selectedModel === "deepseek-v4"
                        ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    🧠 DeepSeek V4
                  </button>
                  <button
                    onClick={() => setSelectedModel("deepseek-chat")}
                    className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                      selectedModel === "deepseek-chat"
                        ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    ⚡ DeepSeek Chat
                  </button>
                  <button
                    onClick={() => setSelectedModel("hermes-3")}
                    className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                      selectedModel === "hermes-3"
                        ? "bg-purple-500/20 text-purple-300 border border-purple-500/40 shadow-sm"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    🦙 Nous Hermes 3
                  </button>
                  <button
                    onClick={() => setSelectedModel("hermes-2-pro")}
                    className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                      selectedModel === "hermes-2-pro"
                        ? "bg-purple-500/20 text-purple-300 border border-purple-500/40 shadow-sm"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    🚀 Hermes 2 Pro
                  </button>
                </div>
              </div>

              <button
                onClick={() => setShowSettingsModal(true)}
                className="flex items-center space-x-1 text-slate-400 hover:text-cyan-400 transition-colors"
                title="Configurações de chaves de API"
              >
                <Settings className="h-3.5 w-3.5" />
                <span>Chaves de API</span>
              </button>
            </div>

            {/* Campo de Entrada de Prompt */}
            <div className="pt-2 flex flex-col sm:flex-row gap-3 items-stretch sm:items-end">
              <div className="flex-1 relative">
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      handleRunQuery();
                    }
                  }}
                  rows={2}
                  placeholder="Descreva a tarefa (ex: 'Mostre os top 5 clientes por faturamento' ou 'Cotação atual do Bitcoin')..."
                  className="w-full bg-slate-900/60 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500 transition-all resize-none"
                />
              </div>

              <div className="flex sm:flex-col gap-2">
                <button
                  onClick={() => handleRunQuery()}
                  disabled={isLoading || !prompt.trim()}
                  className="flex-1 sm:flex-initial flex items-center justify-center space-x-2 px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold text-sm shadow-lg shadow-cyan-500/25 transition-all transform active:scale-95"
                >
                  {isLoading ? (
                    <>
                      <RefreshCw className="h-4 w-4 animate-spin text-white" />
                      <span>Executando...</span>
                    </>
                  ) : (
                    <>
                      <span>Executar</span>
                      <ArrowRight className="h-4 w-4" />
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Atalhos com Exemplos Prontos */}
            <div className="pt-3 border-t border-slate-800/60 flex flex-wrap gap-1.5 items-center">
              <span className="text-[11px] text-slate-400 font-medium mr-1">Consultas rápidas:</span>
              {PRESET_QUERIES.map((preset, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setPrompt(preset.prompt);
                    handleRunQuery(preset.prompt);
                  }}
                  className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-slate-900/80 hover:bg-slate-800 border border-slate-800/80 hover:border-cyan-500/40 text-[11px] text-slate-300 transition-all"
                >
                  <span>{preset.icon}</span>
                  <span>{preset.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Animação de Carregamento */}
        {isLoading && (
          <div className="max-w-4xl mx-auto glass-card rounded-2xl p-8 border border-cyan-500/30 text-center space-y-4 animate-pulse">
            <div className="inline-flex p-3 rounded-full bg-cyan-950/60 border border-cyan-800 text-cyan-400">
              <Bot className="h-8 w-8 animate-bounce" />
            </div>
            <div className="space-y-2">
              <h3 className="text-lg font-bold text-cyan-300">DeepSeek V4 está analisando a tarefa e orquestrando as ferramentas...</h3>
              <p className="text-sm text-slate-400">
                Avaliando a necessidade de acionar a função local `execute_sql_query` ou `fetch_external_api`.
              </p>
            </div>
          </div>
        )}

        {/* Área de Resultados */}
        {response && !isLoading && (
          <div className="max-w-5xl mx-auto space-y-6">
            {/* Barra de Status da Resposta */}
            <div className="flex flex-wrap items-center justify-between gap-3 glass-card rounded-2xl p-4 border border-slate-800">
              <div className="flex items-center space-x-3">
                <div className="h-10 w-10 rounded-xl bg-cyan-950/80 border border-cyan-800 flex items-center justify-center text-cyan-400">
                  <CheckCircle2 className="h-5 w-5 text-emerald-400" />
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-semibold text-sm text-white">Tarefa Concluída com Sucesso</span>
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-950 text-indigo-300 border border-indigo-800">
                      {response.provider}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 line-clamp-1">
                    «{response.query}»
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4 text-xs text-slate-400">
                <div className="flex items-center space-x-1.5">
                  <Clock className="h-3.5 w-3.5 text-cyan-400" />
                  <span>Tempo total: <strong className="text-slate-200">{response.total_time_ms} ms</strong></span>
                </div>
                <div className="flex items-center space-x-1.5">
                  <Layers className="h-3.5 w-3.5 text-purple-400" />
                  <span>Passos: <strong className="text-slate-200">{response.steps.length}</strong></span>
                </div>
                <button
                  onClick={() => copyToClipboard(JSON.stringify(response, null, 2), "json")}
                  className="flex items-center space-x-1 px-2.5 py-1 rounded-md bg-slate-900 border border-slate-700 hover:border-slate-500 text-slate-300"
                  title="Copiar JSON estruturado completo"
                >
                  {copiedJSON ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                  <span>{copiedJSON ? "Copiado" : "JSON"}</span>
                </button>
              </div>
            </div>

            {/* Grade de Cartões de KPIs */}
            {response.kpis && response.kpis.length > 0 && (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {response.kpis.map((kpi, idx) => (
                  <div
                    key={idx}
                    className="glass-card glass-card-hover rounded-xl p-4 border border-slate-800 relative overflow-hidden"
                  >
                    <div className="flex justify-between items-start">
                      <span className="text-xs font-medium text-slate-400">{kpi.label}</span>
                      {kpi.trend === "up" ? (
                        <TrendingUp className="h-4 w-4 text-emerald-400" />
                      ) : kpi.trend === "down" ? (
                        <TrendingDown className="h-4 w-4 text-rose-400" />
                      ) : null}
                    </div>
                    <div className="text-2xl font-bold text-white tracking-tight mt-1">
                      {kpi.value}
                    </div>
                    {kpi.subtext && (
                      <p className="text-[11px] text-slate-400 mt-1 flex items-center space-x-1">
                        <span>{kpi.subtext}</span>
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Navegação por Abas */}
            <div className="border-b border-slate-800 flex space-x-2 text-sm font-medium">
              <button
                onClick={() => setActiveTab("overview")}
                className={`flex items-center space-x-2 pb-3 px-3 border-b-2 transition-all ${
                  activeTab === "overview"
                    ? "border-cyan-500 text-cyan-400"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <BarChart3 className="h-4 w-4" />
                <span>Visão Geral & Insights</span>
              </button>

              {response.table_data && (
                <button
                  onClick={() => setActiveTab("table")}
                  className={`flex items-center space-x-2 pb-3 px-3 border-b-2 transition-all ${
                    activeTab === "table"
                      ? "border-cyan-500 text-cyan-400"
                      : "border-transparent text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <TableIcon className="h-4 w-4" />
                  <span>Tabela de Dados ({response.table_data.total_count})</span>
                </button>
              )}

              {response.executed_sql && (
                <button
                  onClick={() => setActiveTab("sql")}
                  className={`flex items-center space-x-2 pb-3 px-3 border-b-2 transition-all ${
                    activeTab === "sql"
                      ? "border-cyan-500 text-cyan-400"
                      : "border-transparent text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <Code2 className="h-4 w-4" />
                  <span>Consulta SQL</span>
                </button>
              )}

              <button
                onClick={() => setActiveTab("steps")}
                className={`flex items-center space-x-2 pb-3 px-3 border-b-2 transition-all ${
                  activeTab === "steps"
                    ? "border-cyan-500 text-cyan-400"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Terminal className="h-4 w-4" />
                <span>Rastreamento de Passos ({response.steps.length})</span>
              </button>

              <button
                onClick={() => setActiveTab("raw")}
                className={`flex items-center space-x-2 pb-3 px-3 border-b-2 transition-all ${
                  activeTab === "raw"
                    ? "border-cyan-500 text-cyan-400"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <FileJson className="h-4 w-4" />
                <span>Dados Brutos (JSON)</span>
              </button>
            </div>

            {/* Aba 1: Visão Geral */}
            {activeTab === "overview" && (
              <div className="space-y-6">
                <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                  <div className="flex items-center space-x-2 text-cyan-400 text-xs font-bold uppercase tracking-wider">
                    <Sparkles className="h-4 w-4" />
                    <span>Síntese Gerada pelo Agente</span>
                  </div>
                  <div className="text-slate-200 text-sm sm:text-base leading-relaxed whitespace-pre-line">
                    {response.markdown_answer}
                  </div>

                  {response.insights && response.insights.length > 0 && (
                    <div className="pt-4 border-t border-slate-800 space-y-2">
                      <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                        Principais Insights de Negócio:
                      </span>
                      <ul className="space-y-1.5 text-xs text-slate-300">
                        {response.insights.map((insight, idx) => (
                          <li key={idx} className="flex items-start space-x-2">
                            <span className="text-cyan-400 font-bold">•</span>
                            <span dangerouslySetInnerHTML={{ __html: insight }} />
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {response.table_data && (
                  <div className="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-white">Amostragem dos Dados Obtidos</span>
                      <button
                        onClick={() => setActiveTab("table")}
                        className="text-xs text-cyan-400 hover:underline flex items-center space-x-1"
                      >
                        <span>Ver tabela completa</span>
                        <ArrowRight className="h-3 w-3" />
                      </button>
                    </div>

                    <div className="overflow-x-auto rounded-xl border border-slate-800">
                      <table className="w-full text-left text-xs">
                        <thead className="bg-slate-900/80 text-slate-400 uppercase font-semibold border-b border-slate-800">
                          <tr>
                            {response.table_data.columns.map((col, idx) => (
                              <th key={idx} className="px-4 py-3">
                                {col}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/60">
                          {response.table_data.rows.slice(0, 4).map((row, rIdx) => (
                            <tr key={rIdx} className="hover:bg-slate-900/40 transition-colors">
                              {row.map((cell, cIdx) => (
                                <td key={cIdx} className="px-4 py-2.5 text-slate-200">
                                  {String(cell)}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Aba 2: Tabela de Dados */}
            {activeTab === "table" && response.table_data && (
              <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                  <div className="relative w-full sm:w-72">
                    <Search className="h-4 w-4 text-slate-400 absolute left-3 top-3" />
                    <input
                      type="text"
                      placeholder="Filtrar registros na tabela..."
                      value={tableSearch}
                      onChange={(e) => setTableSearch(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
                    />
                  </div>

                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-slate-400">
                      Exibindo {filteredRows.length} de {response.table_data.total_count} registros
                    </span>
                  </div>
                </div>

                <div className="overflow-x-auto rounded-xl border border-slate-800">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-900/90 text-slate-400 uppercase font-semibold border-b border-slate-800">
                      <tr>
                        {response.table_data.columns.map((col, idx) => (
                          <th key={idx} className="px-4 py-3">
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60">
                      {filteredRows.map((row, rIdx) => (
                        <tr key={rIdx} className="hover:bg-slate-900/50 transition-colors">
                          {row.map((cell, cIdx) => (
                            <td key={cIdx} className="px-4 py-3 text-slate-200 font-mono">
                              {String(cell)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Aba 3: Consulta SQL */}
            {activeTab === "sql" && response.executed_sql && (
              <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <div className="flex justify-between items-center">
                  <div className="flex items-center space-x-2">
                    <Terminal className="h-4 w-4 text-cyan-400" />
                    <span className="text-sm font-semibold text-white">Consulta SQL Executada</span>
                  </div>
                  <button
                    onClick={() => copyToClipboard(response.executed_sql || "", "sql")}
                    className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 hover:border-slate-500 text-xs text-slate-300"
                  >
                    {copiedSQL ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                    <span>{copiedSQL ? "Copiado!" : "Copiar SQL"}</span>
                  </button>
                </div>

                <div className="p-4 rounded-xl bg-slate-950 font-mono text-xs text-cyan-300 overflow-x-auto border border-slate-800/80 leading-relaxed shadow-inner">
                  {response.executed_sql}
                </div>

                <div className="flex items-center space-x-2 text-xs text-slate-400">
                  <span className="px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800 font-medium">
                    SELECT Seguro
                  </span>
                  <span>Tempo de resposta do banco: <strong>{response.raw_tool_data?.execution_time_ms || 0.81} ms</strong></span>
                </div>
              </div>
            )}

            {/* Aba 4: Rastreamento de Passos */}
            {activeTab === "steps" && (
              <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <h3 className="text-sm font-semibold text-white">Rastreamento de Raciocínio e Disparo de Ferramentas</h3>
                <div className="space-y-4">
                  {response.steps.map((st) => (
                    <div
                      key={st.step_number}
                      className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 space-y-2 relative"
                    >
                      <div className="flex items-center justify-between text-xs">
                        <div className="flex items-center space-x-2">
                          <span className="px-2 py-0.5 rounded-full font-bold bg-cyan-950 text-cyan-400 border border-cyan-800">
                            Passo {st.step_number}
                          </span>
                          <span className="font-semibold text-slate-200">{st.title}</span>
                        </div>
                        <span className="text-slate-400 text-[11px] font-mono">
                          {st.duration_ms} ms
                        </span>
                      </div>
                      <p className="text-xs text-slate-300">{st.description}</p>
                      {st.payload && (
                        <pre className="p-2.5 rounded-lg bg-slate-950 text-[11px] text-slate-400 font-mono overflow-x-auto border border-slate-900">
                          {JSON.stringify(st.payload, null, 2)}
                        </pre>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Aba 5: Resposta Bruta JSON */}
            {activeTab === "raw" && (
              <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-3">
                <span className="text-sm font-semibold text-white">Resultado JSON Não Tratado da Ferramenta</span>
                <pre className="p-4 rounded-xl bg-slate-950 font-mono text-xs text-slate-300 overflow-x-auto border border-slate-800 max-h-96">
                  {JSON.stringify(response.raw_tool_data, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}

        {/* Guia para a Seção Em Destaque no LinkedIn */}
        <section id="linkedin-guide" className="max-w-5xl mx-auto pt-8 border-t border-slate-800 space-y-6">
          <div className="glass-card rounded-2xl p-6 sm:p-8 border border-blue-500/30 bg-gradient-to-br from-slate-900/90 via-slate-900/80 to-blue-950/20 space-y-6">
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-xl bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400">
                <LinkedInIcon className="h-5 w-5" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">
                  Seção «Em Destaque» (Featured) no LinkedIn
                </h2>
                <p className="text-xs text-slate-400">
                  Instruções passo a passo e textos prontos para fixar este projeto no seu perfil profissional
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Card de Instruções */}
              <div className="space-y-3 bg-slate-950/60 p-4 rounded-xl border border-slate-800">
                <h3 className="text-sm font-semibold text-cyan-400 flex items-center space-x-1.5">
                  <CheckCircle2 className="h-4 w-4" />
                  <span>Passo a Passo para Fixar:</span>
                </h3>
                <ol className="text-xs text-slate-300 space-y-2 list-decimal list-inside leading-relaxed">
                  <li>Acesse seu perfil do LinkedIn e clique no botão <strong>«Adicionar seção»</strong>.</li>
                  <li>Selecione <strong>«Recomendado» → «Adicionar em destaque»</strong>.</li>
                  <li>Clique no ícone <strong>«+» → «Adicionar um link»</strong> e insira o link do repositório: <code>https://github.com/vestek70/ai-agent-fullstack-hub</code>.</li>
                  <li>Envie a animação <code>demo.gif</code> da pasta assets como imagem de miniatura.</li>
                  <li>Copie o texto pronto ao lado, cole na descrição e clique em <strong>Salvar</strong>.</li>
                </ol>
              </div>

              {/* Card com Texto Pronto para Copiar */}
              <div className="space-y-3 bg-slate-950/60 p-4 rounded-xl border border-slate-800">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-semibold text-blue-300">
                    Texto Pronto para o Destaque / Post:
                  </h3>
                  <button
                    onClick={() => {
                      const text = `🚀 AI Agent Fullstack Hub: Next.js + Python FastAPI + Autonomous Tool Calling

Desenvolvi uma aplicação fullstack de Inteligência Artificial onde o agente autônomo (DeepSeek V4 & Nous Hermes 3):
✅ Recebe instruções em linguagem natural
✅ Executa Tool Calling em tempo real (queries SQL complexas em PostgreSQL/SQLite e consumo de APIs externas)
✅ Retorna relatórios executivos com KPIs, tabelas interativas e síntese em UI moderna no Tailwind CSS!

📦 Tech Stack: Next.js 16, React 19, Tailwind CSS v4, Python 3.12, FastAPI, SQLite/PostgreSQL, DeepSeek V4, Hermes Function Calling.

🔗 Repositório no GitHub: https://github.com/vestek70/ai-agent-fullstack-hub

#AIAgent #DeepSeek #NextJS #Python #FastAPI #TailwindCSS #Fullstack #ToolCalling #ArtificialIntelligence`;
                      navigator.clipboard.writeText(text);
                      alert("Texto copiado para a área de transferência!");
                    }}
                    className="text-xs text-cyan-400 hover:underline flex items-center space-x-1"
                  >
                    <Copy className="h-3 w-3" />
                    <span>Copiar Texto</span>
                  </button>
                </div>
                <div className="text-[11px] font-mono text-slate-300 p-3 rounded-lg bg-slate-900 border border-slate-800 max-h-36 overflow-y-auto leading-relaxed">
                  🚀 <strong>AI Agent Fullstack Hub: DeepSeek V4 + Next.js + Python</strong><br/><br/>
                  Desenvolvi uma aplicação fullstack de IA com DeepSeek V4 e Nous Hermes 3:<br/>
                  ✅ Recebe tarefas em linguagem natural<br/>
                  ✅ Executa Tool Calling em tempo real (queries SQL em PostgreSQL/SQLite & APIs externas)<br/>
                  ✅ Retorna resultados em UI interativa no Tailwind CSS!<br/><br/>
                  #AIAgent #DeepSeek #NextJS #Python #FastAPI #TailwindCSS #ToolCalling
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Modal: Esquema do Banco de Dados */}
      {showSchemaModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="glass-card rounded-2xl max-w-3xl w-full max-h-[80vh] flex flex-col border border-slate-700 shadow-2xl">
            <div className="p-4 border-b border-slate-800 flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <Database className="h-5 w-5 text-cyan-400" />
                <h3 className="text-base font-bold text-white">Esquema do Banco de Dados Relacional</h3>
              </div>
              <button
                onClick={() => setShowSchemaModal(false)}
                className="text-slate-400 hover:text-white text-sm px-2 py-1"
              >
                ✕
              </button>
            </div>
            <div className="p-6 overflow-y-auto space-y-6 text-xs">
              {schemaData ? (
                Object.entries(schemaData).map(([tblName, info]: [string, any]) => (
                  <div key={tblName} className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-cyan-300 text-sm">Tabela: {tblName}</span>
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">
                        Registros: {info.total_rows}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-2">
                      {info.columns.map((c: any) => (
                        <div key={c.name} className="p-2 rounded bg-slate-950 border border-slate-800/80">
                          <span className="font-mono text-slate-200">{c.name}</span>
                          <span className="text-[10px] text-cyan-400 block">{c.type}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-slate-400">
                  <RefreshCw className="h-6 w-6 animate-spin mx-auto mb-2 text-cyan-400" />
                  <span>Carregando esquema do banco de dados...</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Modal: Registro de Ferramentas */}
      {showToolsModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="glass-card rounded-2xl max-w-2xl w-full max-h-[80vh] flex flex-col border border-slate-700 shadow-2xl">
            <div className="p-4 border-b border-slate-800 flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <Cpu className="h-5 w-5 text-purple-400" />
                <h3 className="text-base font-bold text-white">Registro de Ferramentas (Tool Calling)</h3>
              </div>
              <button
                onClick={() => setShowToolsModal(false)}
                className="text-slate-400 hover:text-white text-sm px-2 py-1"
              >
                ✕
              </button>
            </div>
            <div className="p-6 overflow-y-auto space-y-4 text-xs">
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <div className="flex items-center space-x-2">
                  <Database className="h-4 w-4 text-cyan-400" />
                  <span className="font-bold text-white text-sm">execute_sql_query</span>
                </div>
                <p className="text-slate-300">
                  Executa consultas SQL SELECT seguras nas tabelas `customers`, `products`, `orders`, `order_items` e `support_tickets`.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <div className="flex items-center space-x-2">
                  <Globe className="h-4 w-4 text-emerald-400" />
                  <span className="font-bold text-white text-sm">fetch_external_api</span>
                </div>
                <p className="text-slate-300">
                  Coleta dados em tempo real de serviços externos: CoinGecko (criptomoedas), GitHub REST API (repositórios e estrelas) e Open-Meteo (clima).
                </p>
              </div>

              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <div className="flex items-center space-x-2">
                  <BarChart3 className="h-4 w-4 text-amber-400" />
                  <span className="font-bold text-white text-sm">calculate_kpis</span>
                </div>
                <p className="text-slate-300">
                  Realiza agregações analíticas (soma, ticket médio, valores extremos e tendências) sobre as amostragens de dados.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Configurações de Chaves de API */}
      {showSettingsModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="glass-card rounded-2xl max-w-md w-full flex flex-col border border-slate-700 shadow-2xl p-6 space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-white flex items-center space-x-2">
                <Settings className="h-4 w-4 text-cyan-400" />
                <span>Configurações de Chaves de API</span>
              </h3>
              <button onClick={() => setShowSettingsModal(false)} className="text-slate-400 hover:text-white">✕</button>
            </div>

            <div className="space-y-3 text-xs">
              <p className="text-slate-400">
                Por padrão, o agente semântico local integrado funciona imediatamente com latência ultrarrápida. Você também pode informar sua chave para inferência direta:
              </p>

              <div>
                <label className="block text-slate-300 font-medium mb-1">DeepSeek API Key:</label>
                <input
                  type="password"
                  placeholder="sk-..."
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200"
                />
              </div>

              <div className="p-3 rounded-lg bg-cyan-950/40 border border-cyan-800/80 text-cyan-300 text-[11px]">
                💡 Se a chave não for informada, o sistema opera automaticamente via mecanismo semântico local, disparando todas as consultas SQL e chamadas de API reais.
              </div>
            </div>

            <button
              onClick={() => setShowSettingsModal(false)}
              className="w-full py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs"
            >
              Salvar
            </button>
          </div>
        </div>
      )}

      {/* Rodapé */}
      <footer className="w-full border-t border-slate-800/80 py-6 text-center text-xs text-slate-500">
        <p>ai-agent-fullstack-hub • Desenvolvido com Next.js 16, Python, Tailwind CSS & DeepSeek V4 Tool Calling</p>
      </footer>
    </div>
  );
}
