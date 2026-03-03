import gradio as gr
from barcode_scanner import scan_barcode
from cart import add_to_cart, view_cart, get_total, clear_cart, remove_item_from_cart
from billing import generate_bill
from chatbot import shopping_bot


# 🎨 GLOBAL CSS
css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

body {
    font-family: 'Poppins', sans-serif;
}

.gradio-container {
    font-size: 10px !important;
}

/* TITLE */
h1 {
    text-align: center;
    font-size: 42px !important;
}



/* INPUT BOX */
textarea, input {
    font-size: 14px !important;
}

/* BILLING OUTPUT → RECEIPT STYLE */
#bill_box textarea {
    font-family: 'Courier New', monospace !important;
    font-size: 15px !important;
    font-weight: bold;
    color: #FFFFFF;
}

/* CHATBOT */
.message.user, .message.bot {
    font-size: 16px !important;
}
"""


# -------------------------------
# FUNCTIONS
# -------------------------------

def scan_and_add():
    product = scan_barcode()

    if product:
        add_to_cart(product)
        return show_cart()

    return "❌ Product not found"


def show_cart():
    items = view_cart()

    if not items:
        return "🛒 Cart is empty"

    output = "🧾 CART ITEMS\n\n"

    for name, details in items.items():
        output += f"{name} x{details['quantity']} = ₹{details['price'] * details['quantity']}\n"

    output += f"\n----------------------\n💰 TOTAL = ₹{get_total()}"
    return output


def clear():
    clear_cart()
    return "🗑 Cart cleared"


def remove_product(name):

    if not name.strip():
        return "⚠ Enter product name"

    removed = remove_item_from_cart(name)

    if removed:
        return show_cart()

    return "❌ Product not found in cart"


# -------------------------------
# CHATBOT
# -------------------------------

def smart_chat(user_message, history):

    if not user_message.strip():
        return history, ""

    if history is None:
        history = []

    cart_items = view_cart()
    total = get_total()

    context = f"Cart items: {cart_items} | Total bill: ₹{total}"

    bot_reply = shopping_bot(user_message, context)

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": bot_reply})

    return history, ""


# -------------------------------
# UI
# -------------------------------

with gr.Blocks(css=css, title="AI Smart Shopping Assistant") as app:

    gr.Markdown("🛒 AI Smart Shopping Assistant")

    with gr.Row():

        # 🧾 BILLING COLUMN
        with gr.Column(scale=3):

            output = gr.Textbox(
                lines=20,
                label="Cart / Billing",
                elem_id="bill_box"
            )

            gr.Button("📷 Scan Product").click(scan_and_add, outputs=output)
            gr.Button("🛒 View Cart").click(show_cart, outputs=output)
            gr.Button("💳 Generate Bill").click(generate_bill, outputs=output)
            gr.Button("🗑 Clear Cart").click(clear, outputs=output)

            gr.Markdown("### 🗑 Remove Product")

            remove_input = gr.Textbox(label="Enter product name")

            gr.Button("Remove Product").click(
                remove_product,
                inputs=remove_input,
                outputs=output
            )

        # 🤖 CHATBOT COLUMN
        with gr.Column(scale=1):

            gr.Markdown("### 🤖 AI Assistant")

            chatbot_ui = gr.Chatbot(height=450)

            msg = gr.Textbox(placeholder="Ask about your shopping...")
            send = gr.Button("Send")

            send.click(
                smart_chat,
                inputs=[msg, chatbot_ui],
                outputs=[chatbot_ui, msg]
            )

            msg.submit(
                smart_chat,
                inputs=[msg, chatbot_ui],
                outputs=[chatbot_ui, msg]
            )


app.launch()