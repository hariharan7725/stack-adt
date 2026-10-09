# StackNav — Browser History Manager

**StackNav** is an interactive, commercial-grade browser navigation simulator and memory inspector built with **Python 3.11+**, **Streamlit**, and a **custom Stack Abstract Data Type (ADT)** backend.

Designed with a high-performance **Cyber-Glassmorphism** aesthetic, StackNav demonstrates core computer science principles in action:
* **Custom Stack ADT implementation from scratch** using strict data encapsulation.
* **LIFO (Last In, First Out)** navigation semantics powering Back and Forward traversal.
* **Dual-Stack Browser Navigation Architecture** operating in \(\mathcal{O}(1)\) time.
* **Dynamic 3D Glassmorphic Memory Visualizer** rendering live memory blocks with LIFO pointers.
* **Embedded Browser Viewport (~75% / 25% Desktop Split)** with real iframe rendering, security header disclosure (`X-Frame-Options` / CSP), and external fallback actions.
* **Minimalist, clean codebase** containing only essential, modular code files.

---

## 1. Project Architecture & Folder Structure

StackNav is organized into a clean, minimal project structure with zero unnecessary bloat:

```
stacknav/
├── app.py                      # Main Streamlit frontend & Cyber-Glassmorphism visualizer
├── stack_adt.py                # Pure Python custom Stack ADT with O(1) operations
├── browser_history.py          # Encapsulated dual-stack BrowserHistory engine
├── components/
│   ├── __init__.py
│   └── website_viewer.py       # Glassmorphic browser chrome, iframe viewport & fallback
├── requirements.txt            # Minimal dependency definitions (streamlit>=1.35.0)
└── README.md                   # Complete architectural & technical documentation
```

### Module Responsibilities

| File | Purpose | Key Responsibilities |
| :--- | :--- | :--- |
| **`stack_adt.py`** | Data Structure Core | Generic `Stack[T]` with private `_items` storage, `push`, `pop`, `peek`, `is_empty`, `size`, `clear`, and immutable `snapshot()`. |
| **`browser_history.py`** | Navigation Engine | `BrowserHistory` class managing `_back_stack` and `_forward_stack`. Handles URL validation, branch resets, and state queries. |
| **`website_viewer.py`** | Viewport Component | Renders the browser frame, traffic lights, iframe rendering, security notices, and fast-launch verified test endpoints. |
| **`app.py`** | UI & Telemetry | Cyber-Glassmorphism styling, toolbar controls, pre-execution callbacks, and dynamic 3D stack memory cards. |

---

## 2. Key Features

### A. Commercial Browser Workspace (~75% Desktop Width)
* **Comprehensive Navigation Toolbar**:
  * **◀ Back**: Pops the previous URL from the Back Stack and pushes the current page to the Forward Stack. Automatically disabled when the Back Stack is empty.
  * **Forward ▶**: Pops the next URL from the Forward Stack and pushes the current page to the Back Stack. Automatically disabled when the Forward Stack is empty.
  * **⟳ Reload**: Refreshes the embedded viewing frame for the active webpage.
  * **Reset ↺**: Clears the session history and returns the engine to standby.
  * **Address Bar**: Glassmorphic input with Enter-key submission and auto-prefixing (`https://`).
  * **Navigate ➔**: Electric gradient action button triggering validation and navigation.
* **Live Embedded Webpage Viewport**:
  * Simulated browser frame featuring macOS traffic light glow dots (`● ● ●`), SSL status lock icon (`🔒`), and address preview badge.
  * Embedded responsive iframe (`height=650px`) rendering embed-compatible web destinations natively.
  * **"Open in New Tab ↗"** button allowing seamless inspection of destinations that restrict iframes.
* **Fast-Launch Verified Endpoints**:
  * Instant one-click test buttons for verified embed-compatible sites:
    * `🚀 Example Domain` (`https://example.com`)
    * `🚀 Wikipedia: Stack ADT` (`https://en.m.wikipedia.org/wiki/Stack_(abstract_data_type)`)
    * `🚀 W3C Architecture` (`https://www.w3.org`)

### B. Dynamic 3D Stack Telemetry Panel (~25% Desktop Width)
* **Back Stack Chassis (Cyan / Indigo Theme)**:
  * Renders each historical page as an elevated 3D glass plate with depth indexing.
  * The topmost card highlights the next retrieval target with a glowing badge: `⚡ POP TARGET (NEXT BACK)`.
  * Real-time item counter pill displaying active stack depth.
  * Holographic empty slot indicator when 0 items are stored.
* **Active Working Register**:
  * Central radiant crystal hub displaying the active URL pointer with a pulsating radar beacon.
  * Explicitly reflects the CPU working register concept between the two LIFO stacks.
* **Forward Stack Chassis (Emerald / Teal Theme)**:
  * Displays pages made accessible after backwards navigation.
  * The topmost card highlights the forward retrieval target: `⚡ POP TARGET (NEXT FORWARD)`.
  * Automatically cleared whenever a new URL branch is visited.

### C. Cyber-Glassmorphism Visual Design
* **Ambient Cyber Mesh Background**: Deep cosmic slate canvas (`#070b14`) accented by radiant glow orbs (Electric Indigo, Vivid Pink, Neon Cyan).
* **True Frosted Glass Effects**: `-webkit-backdrop-filter: blur(20px)` with translucent borders and soft shadows.
* **High Contrast & Accessible Typography**: Bright white and neon text guaranteeing crisp readability in all viewing modes.

---

## 3. Technology Stack

* **Language**: Python 3.11+ (Compatible with Python 3.10 – 3.13)
* **Frontend Framework**: Streamlit (`streamlit>=1.35.0`)
* **Standard Library Utilities**: `typing`, `urllib.parse`, `html`
* **Styling**: Modern CSS3 (Glassmorphism, Flexbox, CSS Mesh Gradients, Backdrop Filters)

---

## 4. Installation & Setup

### Step 1: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 2: Activate Virtual Environment

* **On Windows (PowerShell / Command Prompt)**:
  ```powershell
  .venv\Scripts\activate
  ```
* **On macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

---

## 5. Computer Science Core Concepts

### A. Stack Abstract Data Type (`stack_adt.py`)

A **Stack** is a linear data structure governed by the **Last-In, First-Out (LIFO)** principle: the most recently pushed element is the first element popped.

* **Encapsulation & Data Hiding**:
  Internal storage is encapsulated in `self._items` (private attribute). External code cannot access or mutate the underlying list directly.
* **Defensive Copying**:
  The `snapshot()` method returns an immutable shallow copy of elements, preventing external UI components from tampering with internal state.
* **Safe Error Handling**:
  Attempts to pop from an empty stack raise a descriptive `EmptyStackError` exception.

### B. Dual-Stack Browser Navigation Engine (`browser_history.py`)

Standard web browsers manage history using two isolated stacks and a pointer to the active webpage:

```
[ Back Stack ]  <====  [ Current URL ]  ====>  [ Forward Stack ]
   (Previous)               (Active)               (Next)
```

1. **Visiting a New Page (`visit(url)`)**:
   * If a current page exists, it is pushed onto the **Back Stack**.
   * The new URL is assigned to `_current_url`.
   * The **Forward Stack** is cleared (visiting a new URL invalidates previous forward branches).
2. **Navigating Back (`back()`)**:
   * If the **Back Stack** is empty, navigation is a no-op.
   * The active URL is pushed onto the **Forward Stack**.
   * The topmost URL is popped from the **Back Stack** and becomes the new active URL.
3. **Navigating Forward (`forward()`)**:
   * If the **Forward Stack** is empty, navigation is a no-op.
   * The active URL is pushed onto the **Back Stack**.
   * The topmost URL is popped from the **Forward Stack** and becomes the new active URL.

---

## 6. Time & Space Complexity Analysis

All primary navigation and stack operations execute in strictly bounded time:

| Operation | ADT / Engine Mechanism | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **`Stack.push(item)`** | Dynamic array append | \(\mathcal{O}(1)\) amortized | \(\mathcal{O}(1)\) |
| **`Stack.pop()`** | Dynamic array pop from end | \(\mathcal{O}(1)\) | \(\mathcal{O}(1)\) |
| **`Stack.peek()`** | Direct index lookup (`_items[-1]`) | \(\mathcal{O}(1)\) | \(\mathcal{O}(1)\) |
| **`Stack.is_empty()`** | Length check (`len(_items) == 0`) | \(\mathcal{O}(1)\) | \(\mathcal{O}(1)\) |
| **`Stack.size()`** | Length query (`len(_items)`) | \(\mathcal{O}(1)\) | \(\mathcal{O}(1)\) |
| **`Stack.clear()`** | Reassigns container to empty list | \(\mathcal{O}(1)\) | \(\mathcal{O}(1)\) |
| **`BrowserHistory.visit()`** | 1 push + 1 clear + 1 pointer assign | \(\mathcal{O}(1)\) | \(\mathcal{O}(1)\) |
| **`BrowserHistory.back()`** | 1 push + 1 pop + 1 pointer assign | \(\mathcal{O}(1)\) | \(\mathcal{O}(1)\) |
| **`BrowserHistory.forward()`** | 1 push + 1 pop + 1 pointer assign | \(\mathcal{O}(1)\) | \(\mathcal{O}(1)\) |

---

## 7. Website Embedding & Security Limitations

Modern web security architecture restricts embedding third-party websites inside iframes:

* **Security Headers**:
  Major platforms (e.g. Google, YouTube, GitHub, Facebook) send HTTP response headers such as:
  * `X-Frame-Options: SAMEORIGIN` or `X-Frame-Options: DENY`
  * `Content-Security-Policy: frame-ancestors 'self'`
* **Expected Browser Behavior**:
  These headers protect against **clickjacking attacks**. When visiting these sites inside an iframe, standard browsers will display a connection refusal or blank screen.
* **StackNav's Transparent Solution**:
  * Navigation and stack history operations always succeed independently of iframe rendering permissions.
  * When a site enforces frame restrictions, StackNav displays an informative security notice alongside an **"Open in New Tab ↗"** action button.
  * Users can test native embedding using embed-friendly endpoints (such as Wikipedia or Example Domain).

---

## 8. Streamlit State Architecture & Callback Synchronization

To prevent Streamlit's `StreamlitWidgetAlreadyInstantiatedError`, all user actions are wired to **pre-execution callbacks (`on_click`)**:

```python
# Callbacks run BEFORE script rerun and widget instantiation
def on_back_click():
    prev_url = st.session_state["browser_history"].back()
    st.session_state["url_text_field"] = prev_url or ""

def on_forward_click():
    next_url = st.session_state["browser_history"].forward()
    st.session_state["url_text_field"] = next_url or ""

def on_navigate_submit():
    raw_input = st.session_state.get("url_text_field", "").strip()
    navigated_url = st.session_state["browser_history"].visit(raw_input)
    st.session_state["url_text_field"] = navigated_url
```

By assigning `st.session_state["url_text_field"]` inside callbacks, the value is updated **before** `st.text_input` is rendered, ensuring bidirectional synchronization with zero runtime conflicts.

---

## 9. Troubleshooting & FAQ

* **Q: Why does a website show "refused to connect" inside the viewer?**
  * **Answer**: The website sets `X-Frame-Options` or CSP headers prohibiting iframe embedding. Click **"Open in New Tab ↗"** in the viewer header to view the live site directly in your browser.
* **Q: Why did my Forward Stack disappear after I typed a new URL?**
  * **Answer**: This is the correct, intended behavior of all web browsers. Visiting a new destination branches history in a new direction, which invalidates all forward pages.
* **Q: Error: `ModuleNotFoundError: No module named 'streamlit'`**
  * **Answer**: Activate your virtual environment first (`.venv\Scripts\activate` on Windows) and run `pip install -r requirements.txt`.
