"""
StackNav — Browser History Manager
Main Streamlit Application

Cyber-Glassmorphism UI Edition:
- 75% Live Browser Workspace with embedded viewport & cyber toolbar
- 25% Real-Time Dynamic Glassmorphic 3D Stack Memory Visualizer
"""

import html
from typing import List, Optional
from urllib.parse import urlparse
import streamlit as st

from browser_history import BrowserHistory, InvalidURLError
from components.website_viewer import render_website_viewer

# -----------------------------------------------------------------------------
# 1. Page Configuration & Cyber-Glassmorphism CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="StackNav — Cyber-Glassmorphism Dual Stack Browser",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GLASSMORPHISM_CSS = """<style>
    /* Dark Cyber-Glassmorphism Ambient Background */
    .stApp {
        background: radial-gradient(circle at 10% 15%, rgba(99, 102, 241, 0.22) 0%, transparent 45%),
                    radial-gradient(circle at 90% 20%, rgba(236, 72, 153, 0.22) 0%, transparent 45%),
                    radial-gradient(circle at 50% 85%, rgba(6, 182, 212, 0.20) 0%, transparent 50%),
                    #070b14 !important;
        color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Page container spacing */
    .block-container {
        padding-top: 60px !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }

    /* Glassmorphism Top Executive Header */
    .glass-navbar {
        padding: 150px 0 0 0;
        background: rgba(15, 23, 42, 0.70) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 2px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        padding: 12px 22px !important;
        margin-bottom: 16px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45), 0 0 15px rgba(99, 102, 241, 0.15) !important;
    }
    .brand-group {
        padding: 20px 0 0 0;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .brand-logo {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 22px;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
    }
    .brand-title {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 0%, #38bdf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
    }
    .brand-subtitle {
        font-size: 0.75rem;
        font-weight: 700;
        color: #94a3b8;
        margin: 0;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Glass Status Badges */
    .pill-group {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .glass-pill {
        font-size: 0.76rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    .pill-active {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.4);
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.25);
    }
    .pill-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 10px #10b981;
    }
    .pill-metric {
        background: rgba(139, 92, 246, 0.15);
        color: #c084fc;
        border: 1px solid rgba(192, 132, 252, 0.35);
        box-shadow: 0 0 12px rgba(139, 92, 246, 0.2);
    }
    .pill-visits {
        background: rgba(6, 182, 212, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.2);
    }
    .pill-action {
        background: rgba(30, 41, 59, 0.7);
        color: #e2e8f0;
        border: 1px solid rgba(255, 255, 255, 0.15);
        max-width: 250px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Streamlit Buttons Restyling to Vibrant Glass */
    div[data-testid="stButton"] button {
        background: rgba(30, 41, 59, 0.75) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(168, 85, 247, 0.45) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        font-weight: 700 !important;
        font-size: 0.86rem !important;
        border-radius: 10px !important;
        height: 44px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.6) 0%, rgba(168, 85, 247, 0.6) 100%) !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5) !important;
        transform: translateY(-2px) !important;
        color: #ffffff !important;
    }
    div[data-testid="stButton"] button:disabled {
        background: rgba(15, 23, 42, 0.4) !important;
        color: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.08) !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* Submit Form Button (Navigate) */
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 0.90rem !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 10px !important;
        height: 44px !important;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.45) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #0891b2 0%, #2563eb 50%, #7c3aed 100%) !important;
        box-shadow: 0 0 35px rgba(6, 182, 212, 0.75) !important;
        transform: translateY(-2px) !important;
        color: #ffffff !important;
    }

    /* Address Text Input in Glass */
    div[data-testid="stTextInput"] input {
        background: rgba(15, 23, 42, 0.85) !important;
        color: #ffffff !important;
        border: 1px solid rgba(139, 92, 246, 0.5) !important;
        border-radius: 10px !important;
        height: 44px !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.5), 0 0 10px rgba(139, 92, 246, 0.15) !important;
        font-size: 0.92rem !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5) !important;
        color: #ffffff !important;
    }

    /* Glass Visual Stack Card Styles */
    .stack-glass-chassis {
        background: rgba(15, 23, 42, 0.70);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 14px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    }
    .stack-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .stack-title-badge {
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .badge-back {
        color: #38bdf8;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }
    .badge-fwd {
        color: #34d399;
        text-shadow: 0 0 10px rgba(52, 211, 153, 0.5);
    }
    .stack-count-badge {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stack-glass-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
    }
    .stack-glass-top {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.6) 0%, rgba(88, 28, 135, 0.6) 100%);
        border: 1.5px solid #38bdf8;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
    }
    .stack-glass-top-fwd {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.6) 0%, rgba(30, 58, 138, 0.6) 100%);
        border: 1.5px solid #34d399;
        box-shadow: 0 0 20px rgba(52, 211, 153, 0.35);
    }
    .stack-idx {
        width: 22px;
        height: 22px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        background: rgba(255, 255, 255, 0.15);
        color: #ffffff;
    }
    .stack-card-info {
        flex: 1;
        overflow: hidden;
    }
    .stack-card-url {
        font-size: 0.78rem;
        font-family: ui-monospace, Menlo, monospace;
        font-weight: 700;
        color: #f8fafc;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .stack-head-tag {
        font-size: 0.68rem;
        font-weight: 800;
        color: #38bdf8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stack-empty-slot {
        background: rgba(15, 23, 42, 0.4);
        border: 1.5px dashed rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 16px 12px;
        text-align: center;
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* Active Register Crystal */
    .active-crystal {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.25) 0%, rgba(6, 182, 212, 0.25) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1.8px solid #818cf8;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 14px;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.35);
    }
    .active-crystal-url {
        font-size: 0.86rem;
        font-family: ui-monospace, Menlo, monospace;
        font-weight: 800;
        color: #38bdf8;
        word-break: break-all;
        margin-top: 4px;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }
</style>
"""
st.markdown(GLASSMORPHISM_CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Session State & Callback Definitions
# -----------------------------------------------------------------------------
if "browser_history" not in st.session_state:
    st.session_state["browser_history"] = BrowserHistory()

if "url_text_field" not in st.session_state:
    st.session_state["url_text_field"] = ""

if "nav_error" not in st.session_state:
    st.session_state["nav_error"] = None

history: BrowserHistory = st.session_state["browser_history"]


def on_back_click() -> None:
    """Callback executed before rerun when Back button is clicked."""
    prev_url = st.session_state["browser_history"].back()
    st.session_state["url_text_field"] = prev_url or ""
    st.session_state["nav_error"] = None


def on_forward_click() -> None:
    """Callback executed before rerun when Forward button is clicked."""
    next_url = st.session_state["browser_history"].forward()
    st.session_state["url_text_field"] = next_url or ""
    st.session_state["nav_error"] = None


def on_home_click() -> None:
    """Callback executed before rerun when Reset button is clicked."""
    st.session_state["browser_history"] = BrowserHistory()
    st.session_state["url_text_field"] = ""
    st.session_state["nav_error"] = None


def on_navigate_submit() -> None:
    """Callback executed before rerun when URL form is submitted."""
    raw_input = st.session_state.get("url_text_field", "")
    if not raw_input or not raw_input.strip():
        st.session_state["nav_error"] = "Please enter a valid website address."
        return

    try:
        navigated_url = st.session_state["browser_history"].visit(raw_input)
        st.session_state["url_text_field"] = navigated_url
        st.session_state["nav_error"] = None
    except InvalidURLError as err:
        st.session_state["nav_error"] = str(err)


# -----------------------------------------------------------------------------
# 3. Glassmorphism Top Executive Header
# -----------------------------------------------------------------------------
current_url = history.get_current_url()
last_action = history.get_last_action()
visited_count = history.get_total_visits()

navbar_html = f"""<div class="glass-navbar">
    <div class="brand-group">
        <div class="brand-logo">🧭</div>
        <div>
            <div class="brand-title">StackNav Cyber</div>
            <div class="brand-subtitle">LIFO DUAL-STACK MEMORY ENGINE</div>
        </div>
    </div>
    <div class="pill-group">
        <span class="glass-pill pill-action" title="{html.escape(last_action)}">
            ⚡ {html.escape(last_action)}
        </span>
        <span class="glass-pill pill-metric">
            O(1) COMPLEXITY
        </span>
        <span class="glass-pill pill-visits">
            📄 SESSIONS: {visited_count}
        </span>
        <span class="glass-pill pill-active">
            <span class="pill-dot"></span>
            ENGINE ACTIVE
        </span>
    </div>
</div>"""
st.markdown(navbar_html, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. Primary 75% / 25% Grid Layout
# -----------------------------------------------------------------------------
col_browser, col_stack = st.columns([3, 1], gap="medium")


# -----------------------------------------------------------------------------
# 5. Browser Workspace (Left ~75%)
# -----------------------------------------------------------------------------
with col_browser:
    tb_c1, tb_c2, tb_c3, tb_c4, tb_c5 = st.columns([0.8, 0.8, 0.8, 6.0, 0.9], gap="small")

    with tb_c1:
        back_disabled = not history.can_go_back()
        st.button(
            "◀ Back",
            key="btn_back",
            disabled=back_disabled,
            on_click=on_back_click,
            use_container_width=True,
            help="Pop URL from Back Stack [O(1)]",
        )

    with tb_c2:
        forward_disabled = not history.can_go_forward()
        st.button(
            "Forward ▶",
            key="btn_forward",
            disabled=forward_disabled,
            on_click=on_forward_click,
            use_container_width=True,
            help="Pop URL from Forward Stack [O(1)]",
        )

    with tb_c3:
        refresh_disabled = current_url is None
        st.button(
            "⟳ Reload",
            key="btn_refresh",
            disabled=refresh_disabled,
            use_container_width=True,
            help="Reload active webpage frame",
        )

    # URL input form with on_click callback
    with tb_c4:
        with st.form(key="url_nav_form", clear_on_submit=False):
            form_col_input, form_col_go = st.columns([5.6, 1.0], gap="small")
            with form_col_input:
                st.text_input(
                    label="Destination Address",
                    placeholder="Enter website (e.g. en.wikipedia.org or example.com)",
                    label_visibility="collapsed",
                    key="url_text_field",
                )
            with form_col_go:
                st.form_submit_button(
                    "Navigate ➔",
                    on_click=on_navigate_submit,
                    use_container_width=True,
                )

    with tb_c5:
        st.button(
            "Reset ↺",
            key="btn_home",
            on_click=on_home_click,
            use_container_width=True,
            help="Reset session stacks to empty standby",
        )

    # Display Navigation Errors if any
    if st.session_state.get("nav_error"):
        st.error(f"Navigation Exception: {st.session_state['nav_error']}", icon="🚫")

    # Render Primary Browser Viewing Frame
    render_website_viewer(history.get_current_url())


# -----------------------------------------------------------------------------
# 6. Dynamic Glassmorphic 3D Stack Visualization (Right ~25%)
# -----------------------------------------------------------------------------
with col_stack:
    st.markdown(
        """<div style="margin-bottom: 10px;">
            <div style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.01em;">
                📊 STACK MEMORY TELEMETRY
            </div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 500;">
                Real-time LIFO dual-stack memory chassis
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    # Helper function to render a stack chassis cleanly in pure HTML
    def render_glass_stack_container(items: List[str], stack_type: str = "back", title: str = "Back Stack") -> str:
        is_back = (stack_type == "back")
        theme_class = "badge-back" if is_back else "badge-fwd"
        head_tag_text = "⚡ POP TARGET (NEXT BACK)" if is_back else "⚡ POP TARGET (NEXT FORWARD)"
        top_card_class = "stack-glass-top" if is_back else "stack-glass-top-fwd"
        
        cards_html = []
        if not items:
            cards_html.append(
                f'<div class="stack-empty-slot">Stack Empty (0 elements)<br><span style="font-size: 0.68rem; opacity: 0.7;">{"Pushed when visiting new URLs" if is_back else "Cleared upon visiting new URLs"}</span></div>'
            )
        else:
            for idx, u in enumerate(items):
                is_top = (idx == 0)
                card_style = top_card_class if is_top else "stack-glass-card"
                parsed = urlparse(u)
                display_str = (parsed.netloc + parsed.path) if parsed.netloc else u
                if len(display_str) > 26:
                    display_str = display_str[:23] + "..."
                
                head_badge = f'<div class="stack-head-tag">{head_tag_text}</div>' if is_top else f'<div style="font-size: 0.65rem; color: #64748b;">DEPTH -{idx}</div>'
                badge_bg = '#38bdf8' if (is_top and is_back) else ('#34d399' if is_top else 'rgba(255,255,255,0.15)')
                
                cards_html.append(f"""<div class="stack-glass-card {card_style}" title="{html.escape(u)}">
                    <div class="stack-idx" style="background: {badge_bg}; color: {'#0f172a' if is_top else '#ffffff'};">
                        {len(items) - idx}
                    </div>
                    <div class="stack-card-info">
                        {head_badge}
                        <div class="stack-card-url">{html.escape(display_str)}</div>
                    </div>
                </div>""")

        items_rendered = "".join(cards_html)
        return f"""<div class="stack-glass-chassis">
            <div class="stack-header-row">
                <span class="stack-title-badge {theme_class}">{'◀ ' if is_back else '▶ '}{title}</span>
                <span class="stack-count-badge">{len(items)} ITEMS</span>
            </div>
            {items_rendered}
        </div>"""

    # 1. Back Stack
    back_snapshot = history.get_back_stack_snapshot()
    st.markdown(render_glass_stack_container(back_snapshot, stack_type="back", title="Back Stack (LIFO)"), unsafe_allow_html=True)

    # 2. Central Active Working Register
    active_display = "NO ACTIVE WEBPAGE"
    if current_url:
        parsed_curr = urlparse(current_url)
        active_display = (parsed_curr.netloc + parsed_curr.path) if parsed_curr.netloc else current_url
        if len(active_display) > 30:
            active_display = active_display[:27] + "..."

    active_hub_html = f"""<div class="active-crystal">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <span style="font-size: 0.72rem; font-weight: 800; color: #c084fc; text-transform: uppercase; letter-spacing: 0.08em;">
                ● ACTIVE WORKING REGISTER
            </span>
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #38bdf8; box-shadow: 0 0 10px #38bdf8;"></span>
        </div>
        <div class="active-crystal-url" title="{html.escape(current_url or '')}">
            {html.escape(active_display)}
        </div>
        <div style="font-size: 0.68rem; color: #cbd5e1; margin-top: 6px; font-weight: 500;">
            Direct Register Pointer &bull; Updates Back/Forward on change
        </div>
    </div>"""
    st.markdown(active_hub_html, unsafe_allow_html=True)

    # 3. Forward Stack
    forward_snapshot = history.get_forward_stack_snapshot()
    st.markdown(render_glass_stack_container(forward_snapshot, stack_type="forward", title="Forward Stack (LIFO)"), unsafe_allow_html=True)

    # 4. Complexity bounds expander
    with st.expander("⚡ Algorithmic Bounds (O(1))", expanded=False):
        st.markdown(
            """
            | Action | ADT Operation | Complexity |
            | :--- | :--- | :--- |
            | **`visit(url)`** | Push Back + Clear Fwd | $\\mathcal{O}(1)$ |
            | **`back()`** | Pop Back + Push Fwd | $\\mathcal{O}(1)$ |
            | **`forward()`** | Pop Fwd + Push Back | $\\mathcal{O}(1)$ |
            | **`push()`** | Dynamic array append | $\\mathcal{O}(1)^*$ |
            | **`pop()`** | Dynamic array pop | $\\mathcal{O}(1)$ |
            | **`peek()`** | Direct index query | $\\mathcal{O}(1)$ |
            
            *amortized $\\mathcal{O}(1)$
            """
        )
