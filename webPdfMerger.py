import sys, subprocess
print("Python executable:", sys.executable)
subprocess.run([sys.executable, "-m", "pip", "list"])

import streamlit as st
from pypdf import PdfWriter

st.set_page_config(page_title="PDF Merger", page_icon="📚")

st.title("PDF Merger）")
st.write("複数のPDFファイルをアップロードして結合できます。")

uploaded_files = st.file_uploader("PDFファイルを選択（複数可）", type="pdf", accept_multiple_files=True)

if uploaded_files:
    pdf_writer = PdfWriter()
    for uploaded_file in uploaded_files:
        pdf_writer.append(uploaded_file)
    
    output_path = "merged.pdf"
    pdf_writer.write(output_path)
    pdf_writer.close()

    st.success("✅ PDFを結合しました！ 下のボタンからダウンロードできます。")

    with open(output_path, "rb") as f:
        st.download_button(
            label="📥 結合済みPDFをダウンロード",
            data=f,
            file_name="merged.pdf",
            mime="application/pdf"
        )
