import gradio as gr
import os

# 🔹 ฟังก์ชันคำนวณปริมาณการเติมหมึก
def calculate_ink(
    density_current_black, density_target_black, ink_volume_black,
    density_current_blue, density_target_blue, ink_volume_blue,
    density_current_red, density_target_red, ink_volume_red,
    density_current_yellow, density_target_yellow, ink_volume_yellow
):
    k_values = {'ดำ': 12, 'ฟ้า': 15, 'แดง': 15, 'เหลือง': 20}  
    densities = {
        "⚫️ ดำ": (density_current_black, density_target_black, ink_volume_black),
        "🔵 ฟ้า": (density_current_blue, density_target_blue, ink_volume_blue),
        "🔴 แดง": (density_current_red, density_target_red, ink_volume_red),
        "🟡 เหลือง": (density_current_yellow, density_target_yellow, ink_volume_yellow),
    }

    results = []
    for color, (density_current, density_target, ink_volume) in densities.items():
        density_current = density_current or 0
        density_target = density_target or 0
        ink_volume = ink_volume or 0

        k_value = k_values[color.split(" ")[1]]  
        ink_adjustment_percent = k_value * (density_target - density_current)  
        ink_adjustment_kg = (ink_adjustment_percent / 100) * ink_volume  

        if ink_adjustment_kg != 0:
            action = "เติม" if ink_adjustment_kg > 0 else "ลด"
            results.append(f"{color}: ต้อง {action} หมึก {round(abs(ink_adjustment_kg), 2)} Kg")

    return "\n".join(results) if results else "⚠️ กรุณากรอกข้อมูลอย่างน้อย 1 สี"

# 🔹 ฟังก์ชันเคลียร์ค่า
def clear_inputs():
    return (None, None, None, None, None, None, None, None, None, None, None, None, "")

# 🔹 จัดวาง UI
with gr.Blocks() as demo:
    gr.Markdown("# 🖌️ Ink Density Calculator")
    gr.Markdown("### กรอกค่า Density และปริมาณหมึกของแต่ละสี แล้วกด 'คำนวณ' เพื่อดูผลลัพธ์")

    with gr.Row():
        gr.Markdown("**สี**")
        gr.Markdown("**Density ปัจจุบัน**")
        gr.Markdown("**Density เป้าหมาย**")
        gr.Markdown("**ปริมาณหมึกในถัง (Kg.)**")

    with gr.Row():
        gr.Markdown("⚫️ **ดำ**")
        density_current_black = gr.Number()
        density_target_black = gr.Number()
        ink_volume_black = gr.Number()

    with gr.Row():
        gr.Markdown("🔵 **ฟ้า**")
        density_current_blue = gr.Number()
        density_target_blue = gr.Number()
        ink_volume_blue = gr.Number()

    with gr.Row():
        gr.Markdown("🔴 **แดง**")
        density_current_red = gr.Number()
        density_target_red = gr.Number()
        ink_volume_red = gr.Number()

    with gr.Row():
        gr.Markdown("🟡 **เหลือง**")
        density_current_yellow = gr.Number()
        density_target_yellow = gr.Number()
        ink_volume_yellow = gr.Number()

    with gr.Row():
        calculate_button = gr.Button("🔥 คำนวณ")
        clear_button = gr.Button("♻️ เคลียร์ค่า")

    output_result = gr.Textbox(label="📌 ผลลัพธ์", lines=8, interactive=False)

    calculate_button.click(
        fn=calculate_ink,
        inputs=[
            density_current_black, density_target_black, ink_volume_black,
            density_current_blue, density_target_blue, ink_volume_blue,
            density_current_red, density_target_red, ink_volume_red,
            density_current_yellow, density_target_yellow, ink_volume_yellow,
        ],
        outputs=output_result,
    )

    clear_button.click(
        fn=clear_inputs,
        inputs=[],
        outputs=[
            density_current_black, density_target_black, ink_volume_black,
            density_current_blue, density_target_blue, ink_volume_blue,
            density_current_red, density_target_red, ink_volume_red,
            density_current_yellow, density_target_yellow, ink_volume_yellow,
            output_result,
        ],
    )

# 🔹 เปิดใช้งาน Web App บน Render
port = int(os.getenv("PORT", 7860))  # ดึงค่า PORT จาก Render
demo.launch(server_name="0.0.0.0", server_port=port)
