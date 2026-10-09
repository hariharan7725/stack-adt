"""
Website Viewer Component for StackNav.

Renders a vibrant cyber-glassmorphism browser viewing frame with iframe-based rendering,
empty states, security header guidance (X-Frame-Options / CSP limitations),
and direct 'Open in New Tab' fallbacks.
"""

from typing import Optional
from urllib.parse import urlparse
import streamlit as st
import streamlit.components.v1 as components


KNOWN_RESTRICTED_DOMAINS = {
    "google.com",
    "www.google.com",
    "github.com",
    "www.github.com",
    "youtube.com",
    "www.youtube.com",
    "facebook.com",
    "www.facebook.com",
    "twitter.com",
    "x.com",
    "linkedin.com",
    "www.linkedin.com",
    "reddit.com",
    "www.reddit.com",
    "amazon.com",
    "www.amazon.com",
    "netflix.com",
    "www.netflix.com",
}


def is_known_restricted_domain(url: str) -> bool:
    """Check if the URL belongs to a major domain known to block iframe embedding."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        return domain in KNOWN_RESTRICTED_DOMAINS or any(
            domain.endswith("." + restricted) for restricted in KNOWN_RESTRICTED_DOMAINS
        )
    except Exception:
        return False


def render_website_viewer(current_url: Optional[str]) -> None:
    """Render the primary browser workspace viewing area."""
    if not current_url:
        _render_empty_state()
        return

    _render_active_browser_frame(current_url)


def _render_empty_state() -> None:
    """Render vibrant cyber-glassmorphism empty state when no URL is active."""
    st.markdown(
        """<div style="
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 92, 246, 0.35);
            border-radius: 16px;
            padding: 44px 28px;
            text-align: center;
            margin-top: 14px;
            box-shadow: 0 10px 35px -5px rgba(0, 0, 0, 0.5), 0 0 20px rgba(99, 102, 241, 0.15);
        ">
            <div style="
                width: 68px;
                height: 68px;
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(236, 72, 153, 0.3) 100%);
                border: 1px solid rgba(236, 72, 153, 0.5);
                border-radius: 20px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 32px;
                margin-bottom: 16px;
                box-shadow: 0 0 25px rgba(236, 72, 153, 0.35);
            ">🧭</div>
            <h3 style="color: #f8fafc; margin: 0 0 8px 0; font-weight: 800; font-size: 1.35rem; letter-spacing: -0.01em;">
                Navigation Engine Standby
            </h3>
            <p style="margin: 0 auto 22px auto; max-width: 520px; font-size: 0.9rem; color: #94a3b8; line-height: 1.6;">
                The dual-stack memory engine is initialized. Enter any address in the glowing address bar above
                or test one of the embed-verified endpoints below to witness real-time LIFO stack allocation.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div style="margin-top: 18px; margin-bottom: 8px;">
            <span style="font-size: 0.8rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.08em; text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);">
                ⚡ FAST-LAUNCH VERIFIED ENDPOINTS
            </span>
        </div>""",
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    sample_sites = [
        ("Example Domain", "https://example.com"),
        ("Wikipedia: Stack ADT", "https://en.m.wikipedia.org/wiki/Stack_(abstract_data_type)"),
        ("W3C Architecture", "https://www.w3.org"),
    ]

    def _on_visit_sample(target_url: str) -> None:
        if "browser_history" in st.session_state:
            try:
                nav_url = st.session_state["browser_history"].visit(target_url)
                st.session_state["url_text_field"] = nav_url
                st.session_state["nav_error"] = None
            except Exception as err:
                st.session_state["nav_error"] = str(err)

    for i, (title, sample_url) in enumerate(sample_sites):
        with cols[i]:
            st.button(
                f"🚀 {title}",
                key=f"quick_sample_{i}",
                on_click=_on_visit_sample,
                args=(sample_url,),
                use_container_width=True,
            )


def _render_active_browser_frame(url: str) -> None:
    """Render the active browser window with glassmorphism chrome, iframe, and security fallbacks."""
    parsed = urlparse(url)
    domain_display = parsed.netloc if parsed.netloc else url
    is_https = parsed.scheme.lower() == "https"
    restricted = is_known_restricted_domain(url)

    # Modern Glassmorphic Window Chrome Header
    st.markdown(
        f"""<div style="
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            border-top-left-radius: 14px;
            border-top-right-radius: 14px;
            padding: 10px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin-top: 14px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        ">
            <!-- Window Traffic Light Glow Dots -->
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: #ff5f56; box-shadow: 0 0 8px rgba(255, 95, 86, 0.8);"></span>
                <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: #ffbd2e; box-shadow: 0 0 8px rgba(255, 189, 46, 0.8);"></span>
                <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: #27c93f; box-shadow: 0 0 8px rgba(39, 201, 63, 0.8);"></span>
                <!-- Glass Address Preview Pill -->
                <div style="
                    margin-left: 14px;
                    background: rgba(30, 41, 59, 0.8);
                    border: 1px solid rgba(56, 189, 248, 0.3);
                    border-radius: 8px;
                    padding: 4px 14px;
                    font-size: 12px;
                    font-weight: 600;
                    color: #e2e8f0;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    box-shadow: 0 0 12px rgba(56, 189, 248, 0.15);
                ">
                    <span>{'🔒' if is_https else '🔓'}</span>
                    <span style="font-family: ui-monospace, Menlo, monospace; color: #38bdf8;">{domain_display}</span>
                </div>
            </div>
            <!-- Open in New Tab Pill Button -->
            <div>
                <a href="{url}" target="_blank" rel="noopener noreferrer" style="
                    font-size: 12px;
                    font-weight: 700;
                    color: #ffffff;
                    text-decoration: none;
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.4) 0%, rgba(168, 85, 247, 0.4) 100%);
                    padding: 6px 16px;
                    border: 1px solid rgba(168, 85, 247, 0.6);
                    border-radius: 10px;
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    box-shadow: 0 0 15px rgba(168, 85, 247, 0.35);
                    transition: all 0.2s ease;
                ">
                    Open in New Tab ↗
                </a>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    if restricted:
        st.warning(
            f"🛡️ **Embedding Security Notice:** `{domain_display}` implements strict frame security "
            f"(`X-Frame-Options: SAMEORIGIN` or Content Security Policy `frame-ancestors 'self'`) "
            f"to protect against clickjacking. Click **'Open in New Tab ↗'** above to view the live destination directly.",
            icon="⚠️",
        )

    # Render iframe viewport
    iframe_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                overflow: hidden;
                background-color: #ffffff;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
            .viewer-wrapper {{
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                position: relative;
            }}
            iframe {{
                width: 100%;
                height: 650px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-top: none;
                border-bottom-left-radius: 14px;
                border-bottom-right-radius: 14px;
                background-color: #ffffff;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
            }}
        </style>
    </head>
    <body>
        <div class="viewer-wrapper">
            <iframe
                id="site-frame"
                src="{url}"
                sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
                loading="lazy"
                title="Embedded Web Page Viewer"
            ></iframe>
        </div>
    </body>
    </html>
    """

    components.html(iframe_html, height=665, scrolling=False)

    st.caption(
        "ℹ️ **Iframe Compliance Note:** External web pages that permit frame embedding render natively above. "
        "Websites restricting embedding display a connection refusal; use 'Open in New Tab ↗' to browse them externally."
    )
