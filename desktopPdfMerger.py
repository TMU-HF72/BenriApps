#!/usr/bin/env python3

import os
import sys
import traceback

import FreeSimpleGUI as sg
from pypdf import PdfWriter


VERSION = "1.0"


def merge_pdfs(paths, output_path):
    writer = PdfWriter()
    try:
        for p in paths:
            writer.append(p)
        # ensure parent dir exists
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        with open(output_path, "wb") as f:
            writer.write(f)
    finally:
        writer.close()


def main():
    sg.theme("SystemDefault")

    file_list_column = [
        [sg.Text("選択したPDF（結合順）")],
        [sg.Listbox(values=[], size=(60, 12), key="-FILE LIST-", enable_events=True)],
        [
            sg.Button("上へ", key="-UP-"),
            sg.Button("下へ", key="-DOWN-"),
            sg.Button("削除", key="-REMOVE-"),
            sg.Button("クリア", key="-CLEAR-"),
        ],
    ]

    control_column = [
        [sg.Text("ファイルを追加")],
        [
            sg.Input(key="-ADD PATH-", enable_events=False, visible=False),
            sg.FilesBrowse("追加", file_types=(("PDF Files", "*.pdf"),), key="-BROWSE-"),
            sg.Button("追加（ダイアログ）", key="-ADD DIALOG-"),
        ],
        [sg.HorizontalSeparator()],
        [sg.Text("出力ファイル")],
        [sg.InputText(default_text="merged.pdf", key="-OUT-", size=(40,1)), sg.FileSaveAs("参照", file_types=(("PDF Files", "*.pdf"),), key="-SAVEAS-", default_extension=".pdf")],
        [sg.Button("結合", size=(10,1), key="-MERGE-", bind_return_key=True), sg.Button("終了", key="-EXIT-")],
        [sg.Text("" )],
        [sg.Text(f"バージョン: {VERSION}")]
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VerticalSeparator(),
            sg.Column(control_column),
        ]
    ]

    window = sg.Window("PDF 結合アプリ", layout, finalize=True)

    file_list = []

    def refresh_listbox():
        window["-FILE LIST-"].update(file_list)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "-EXIT-":
            break

        if event == "-BROWSE-":
            # PySimpleGUI returns a string with files separated by ';'
            raw = values.get("-BROWSE-")
            if raw:
                paths = raw.split(";")
                for p in paths:
                    p = p.strip()
                    if p and p.lower().endswith('.pdf') and os.path.exists(p):
                        file_list.append(p)
                refresh_listbox()

        if event == "-ADD DIALOG-":
            paths = sg.popup_get_file("PDFファイルを選択 (複数選択可)", multiple_files=True, file_types=(("PDF Files", "*.pdf"),))
            if paths:
                for p in paths.split(';'):
                    p = p.strip()
                    if p and p.lower().endswith('.pdf') and os.path.exists(p):
                        file_list.append(p)
                refresh_listbox()

        if event == "-REMOVE-":
            sel = values.get("-FILE LIST-")
            if sel:
                for s in sel:
                    if s in file_list:
                        file_list.remove(s)
                refresh_listbox()

        if event == "-CLEAR-":
            file_list.clear()
            refresh_listbox()

        if event == "-UP-":
            sel = values.get("-FILE LIST-")
            if sel:
                s = sel[0]
                idx = file_list.index(s)
                if idx > 0:
                    file_list[idx], file_list[idx-1] = file_list[idx-1], file_list[idx]
                    refresh_listbox()
                    window["-FILE LIST-"].update(set_to_index=idx-1)

        if event == "-DOWN-":
            sel = values.get("-FILE LIST-")
            if sel:
                s = sel[0]
                idx = file_list.index(s)
                if idx < len(file_list)-1:
                    file_list[idx], file_list[idx+1] = file_list[idx+1], file_list[idx]
                    refresh_listbox()
                    window["-FILE LIST-"].update(set_to_index=idx+1)

        if event == "-MERGE-":
            if not file_list:
                sg.popup_error("結合するPDFを1つ以上選択してください。")
                continue

            out_path = values.get("-OUT-")
            # If user used FileSaveAs widget, it also sets -SAVEAS- value; try to prefer that
            saveas = values.get("-SAVEAS-")
            if saveas:
                out_path = saveas

            if not out_path:
                out_path = sg.popup_get_file("保存先を指定", save_as=True, file_types=(("PDF Files", "*.pdf"),), default_extension=".pdf")
                if not out_path:
                    continue

            # ensure .pdf extension
            if not out_path.lower().endswith('.pdf'):
                out_path += '.pdf'

            try:
                merge_pdfs(file_list, out_path)
                sg.popup("結合完了", f"{len(file_list)} 個のPDFを結合しました。\n保存先: {out_path}")
            except Exception as e:
                tb = traceback.format_exc()
                sg.popup_error("結合に失敗しました:", str(e), tb)

    window.close()


if __name__ == '__main__':
    main()
