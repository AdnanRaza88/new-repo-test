NEUMORPHIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --bg: #E4EBF5;
    --surface: #E4EBF5;
    --shadow-light: #FFFFFF;
    --shadow-dark: #B8C4D8;
    --accent: #4A7FE5;
    --accent-soft: #6B9AF5;
    --text-primary: #2D3748;
    --text-secondary: #5A6B82;
    --text-muted: #8FA3BF;
    --success: #38C97A;
    --warning: #F5A623;
    --danger: #E05D5D;
    --grade-a: #38C97A;
    --grade-b: #4A7FE5;
    --grade-c: #F5A623;
    --grade-f: #E05D5D;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text-primary) !important;
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Main container */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Sidebar neumorphic */
[data-testid="stSidebar"] {
    background: var(--bg) !important;
    border-right: none !important;
    box-shadow: 4px 0 15px rgba(184, 196, 216, 0.5) !important;
}

[data-testid="stSidebar"] > div {
    background: var(--bg) !important;
}

/* Neumorphic card */
.neu-card {
    background: var(--surface);
    border-radius: 20px;
    box-shadow: 8px 8px 20px var(--shadow-dark), -8px -8px 20px var(--shadow-light);
    padding: 24px;
    margin-bottom: 20px;
}

.neu-card-inset {
    background: var(--surface);
    border-radius: 16px;
    box-shadow: inset 4px 4px 10px var(--shadow-dark), inset -4px -4px 10px var(--shadow-light);
    padding: 20px;
    margin-bottom: 16px;
}

/* Stat card */
.stat-card {
    background: var(--surface);
    border-radius: 18px;
    box-shadow: 6px 6px 16px var(--shadow-dark), -6px -6px 16px var(--shadow-light);
    padding: 20px 24px;
    text-align: center;
    transition: box-shadow 0.2s ease;
}

.stat-card:hover {
    box-shadow: 4px 4px 10px var(--shadow-dark), -4px -4px 10px var(--shadow-light);
}

.stat-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1.1;
}

.stat-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* Page title */
.page-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.page-subtitle {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 28px;
}

/* Grade badge */
.grade-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 30px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
}

.grade-a { background: rgba(56,201,122,0.15); color: var(--grade-a); }
.grade-b { background: rgba(74,127,229,0.15); color: var(--grade-b); }
.grade-c { background: rgba(245,166,35,0.15); color: var(--grade-c); }
.grade-f { background: rgba(224,93,93,0.15); color: var(--grade-f); }

/* Streamlit widget overrides */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: var(--bg) !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: inset 3px 3px 8px var(--shadow-dark), inset -3px -3px 8px var(--shadow-light) !important;
    color: var(--text-primary) !important;
    padding: 10px 14px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    box-shadow: inset 4px 4px 10px var(--shadow-dark), inset -2px -2px 8px var(--shadow-light), 0 0 0 2px rgba(74,127,229,0.3) !important;
    outline: none !important;
}

/* Buttons */
.stButton > button {
    background: var(--bg) !important;
    color: var(--text-primary) !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 5px 5px 12px var(--shadow-dark), -5px -5px 12px var(--shadow-light) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 10px 24px !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    box-shadow: 3px 3px 8px var(--shadow-dark), -3px -3px 8px var(--shadow-light) !important;
    color: var(--accent) !important;
}

.stButton > button:active {
    box-shadow: inset 3px 3px 8px var(--shadow-dark), inset -3px -3px 8px var(--shadow-light) !important;
}

/* Primary button variant */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), var(--accent-soft)) !important;
    color: white !important;
    box-shadow: 5px 5px 12px var(--shadow-dark), -2px -2px 8px rgba(255,255,255,0.8) !important;
}

/* Sidebar nav item */
.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 6px;
    cursor: pointer;
    font-weight: 500;
    color: var(--text-secondary);
    transition: all 0.2s ease;
}

.nav-item.active {
    background: var(--bg);
    box-shadow: 4px 4px 10px var(--shadow-dark), -4px -4px 10px var(--shadow-light);
    color: var(--accent);
}

/* Progress bar */
.progress-bar-container {
    background: var(--bg);
    border-radius: 30px;
    box-shadow: inset 2px 2px 6px var(--shadow-dark), inset -2px -2px 6px var(--shadow-light);
    height: 10px;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 30px;
    background: linear-gradient(90deg, var(--accent), var(--accent-soft));
    transition: width 0.4s ease;
}

/* AI response box */
.ai-response {
    background: var(--surface);
    border-radius: 18px;
    box-shadow: 6px 6px 16px var(--shadow-dark), -6px -6px 16px var(--shadow-light);
    padding: 28px;
    border-left: 4px solid var(--accent);
    margin-top: 16px;
}

.ai-response h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--accent);
    margin-bottom: 16px;
}

/* Divider */
.neu-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--shadow-dark), transparent);
    margin: 20px 0;
    border: none;
}

/* Alert boxes */
.alert-success {
    background: rgba(56,201,122,0.1);
    border-left: 4px solid var(--success);
    border-radius: 12px;
    padding: 14px 18px;
    color: #1a7a47;
    font-weight: 500;
}

.alert-error {
    background: rgba(224,93,93,0.1);
    border-left: 4px solid var(--danger);
    border-radius: 12px;
    padding: 14px 18px;
    color: #8b2020;
    font-weight: 500;
}

/* Sidebar branding */
.sidebar-brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
    padding: 16px 8px 8px;
    text-align: center;
}

.sidebar-tagline {
    font-size: 0.72rem;
    color: var(--text-muted);
    text-align: center;
    margin-bottom: 24px;
    letter-spacing: 0.05em;
}

/* Connection status dot */
.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}

.status-online { background: var(--success); }
.status-offline { background: var(--danger); }

/* Stacked metric row */
.metric-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}

.metric-item {
    flex: 1;
    min-width: 130px;
}

/* Table styling */
.stDataFrame {
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 6px 6px 16px var(--shadow-dark), -6px -6px 16px var(--shadow-light) !important;
}
</style>
"""
