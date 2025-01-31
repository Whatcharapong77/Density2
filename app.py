# -*- coding: utf-8 -*-
"""สำเนาของ Density

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uwj9JPZjg33P2VBErF1gJmCuUzM4n0O1
"""

# -*- coding: utf-8 -*-
"""Density

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oFwvr9mWLqOQQuFK2ELikIsS88hk07FK
"""

import gradio as gr
import os

# 🔹 ฟังก์ชันคำนวณปริมาณการเติมหมึก (รองรับช่องว่างและล็อกตัวเลข)
def calculate_ink(
    density_current_black, density_target_black, ink_volume_black,
    density_current_blue, density_target_blue, ink_volume_blue,
    density_current_red, density_target_red, ink_volume_red,
    density_current_yellow, density_target_yellow, ink_volume_yellow
):
    k_values = {'ดำ': 12, 'ฟ้า': 15, 'แดง': 15, 'เหลือง': 20}  # ค่า K ของแต่ละสี
    densities = {
        "⚫️ ดำ": (density_current_black, density_target_black, ink_volume_black),
        "🔵 ฟ้า": (density_current_blue, density_target_blue, ink_volume_blue),
        "🔴 แดง": (density_current_red, density_target_red, ink_volume_red),
        "🟡 เหลือง": (density_current_yellow, density_target_yellow, ink_volume_yellow),
    }

    results = []
    for color, (density_current, density_target, ink_volume) in densities.items():
        # ป้องกัน None โดยใช้ค่า 0 แทน
        density_current = density_current or 0
        density_target = density_target or 0
        ink_volume = ink_volume or 0

        k_value = k_values[color.split(" ")[1]]  # ดึงชื่อสีเพื่อนำไปใช้
        ink_adjustment_percent = k_value * (density_target - density_current)  # คำนวณ %
        ink_adjustment_kg = (ink_adjustment_percent / 100) * ink_volume  # แปลงเป็น Kg

        if ink_adjustment_kg != 0:  # แสดงเฉพาะสีที่ต้องเติมหรือลด
            action = "เติม" if ink_adjustment_kg > 0 else "ลด"
            results.append(f"{color}: ต้อง {action} หมึก {round(abs(ink_adjustment_kg), 2)} Kg")

    return "\n".join(results) if results else "⚠️ กรุณากรอกข้อมูลอย่างน้อย 1 สี"

# 🔹 ฟังก์ชันเคลียร์ค่า (คืนค่าเป็น None)
def clear_inputs():
    return (
        None, None, None,  # ดำ
        None, None, None,  # ฟ้า
        None, None, None,  # แดง
        None, None, None,  # เหลือง
        ""  # ล้างผลลัพธ์
    )

# 🔹 เพิ่ม CSS ให้ตัวหนังสือใหญ่ขึ้น
css = """
h1, h2, h3 {
    font-size: 22px !important;
    font-weight: bold;
}
#output_box {
    font-size: 20px !important;
}
.gr-textbox textarea {
    font-size: 20px !important;
}
.gr-button {
    font-size: 18px !important;
}
"""

# 🔹 จัดวาง UI เป็นตารางและเพิ่มปุ่มเคลียร์ค่า
with gr.Blocks(css=css) as demo:
    gr.Markdown("# 🖌️ Ink Density Calculator")
    gr.Markdown("### กรอกค่า Density และปริมาณหมึกของแต่ละสี แล้วกด 'คำนวณ' เพื่อดูผลลัพธ์")

    with gr.Row():
        gr.Markdown("**สี**")
        gr.Markdown("**Density ปัจจุบัน**")
        gr.Markdown("**Density เป้าหมาย**")
        gr.Markdown("**ปริมาณหมึกในถัง (Kg.)**")

    with gr.Row():
        gr.Markdown("⚫️ **ดำ**")
        density_current_black = gr.Number(value=None)
        density_target_black = gr.Number(value=None)
        ink_volume_black = gr.Number(value=None)

    with gr.Row():
        gr.Markdown("🔵 **ฟ้า**")
        density_current_blue = gr.Number(value=None)
        density_target_blue = gr.Number(value=None)
        ink_volume_blue = gr.Number(value=None)

    with gr.Row():
        gr.Markdown("🔴 **แดง**")
        density_current_red = gr.Number(value=None)
        density_target_red = gr.Number(value=None)
        ink_volume_red = gr.Number(value=None)

    with gr.Row():
        gr.Markdown("🟡 **เหลือง**")
        density_current_yellow = gr.Number(value=None)
        density_target_yellow = gr.Number(value=None)
        ink_volume_yellow = gr.Number(value=None)

    with gr.Row():
        calculate_button = gr.Button("🔥 คำนวณ")
        clear_button = gr.Button("♻️ เคลียร์ค่า")

    # 🔹 ขยายช่องผลลัพธ์ให้ใหญ่ขึ้น
    output_result = gr.Textbox(label="📌 ผลลัพธ์", lines=8, interactive=False, elem_id="output_box")

    # กดปุ่ม "คำนวณ" เพื่อแสดงผลลัพธ์
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

    # กดปุ่ม "เคลียร์ค่า" เพื่อรีเซ็ตค่าทั้งหมดเป็นช่องว่าง
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

# สร้าง Web Interface
iface = gr.Interface(fn=greet, inputs="text", outputs="text")

# ใช้ Port จาก Render (ค่า Default = 7860)
port = int(os.getenv("PORT", 7860))

# รัน Web App บน 0.0.0.0 และใช้ Port ที่ได้จาก Render
iface.launch(server_name="0.0.0.0", server_port=port)
