from django.shortcuts import render, redirect
from .forms import UserForm, ContactForm
from socket import gethostname 
import os
import requests
import re
# Create your views here.

#sampleテキストの取得
with open('summaryapp\sample\sample1.txt', 'r', encoding='UTF-8') as f:
    text_data1 = f.read()
with open('summaryapp\sample\sample2.txt', 'r', encoding='UTF-8') as f:
    text_data2 = f.read()

#sampleテキスト内の改行コードをエスケープしないまま文字列として取得(pythonが理解できるコードに変換)
sample_text1 = repr(text_data1)
sample_text2 = repr(text_data2)


#TOPページの表示
def summary(request):
    summary_form = {"form": "", "sample1": sample_text1[1:-1], "sample2": sample_text2[1:-1]}
    summary_form["form"] = UserForm()
    return render(request, 'summaryapp/top.html', summary_form)


#要約画面の表示(エラーの表示と要約結果のどちらかの処理が行われる)
def result(request):
    if request.method == 'POST':
        sended_form = UserForm(request.POST)
        form = {
                "form": "",
                "original_text": "",
                "delimiter": "",
                "linenumber": "",
                "summary_text": "",
                "originaltext_count": "",
                "originaltext_count_newline": "",
                "summarytext_count": "",
                "summarytext_count_newline": "",
                }

        if sended_form.is_valid():
            HOSTNAME = gethostname()
            # local環境かデプロイ環境かでSECRET_KEYの参照参照先を変更
            if 'LAPTOP' in HOSTNAME:
                from . import apikey_local
                API_KEY = apikey_local.API_KEY
            else:
                API_KEY = os.environ['API_KEY']

            url = "https://api.a3rt.recruit-tech.co.jp/text_summarization/v1"
            text = ""
            text_str = ""

            form['original_text'] = request.POST['text'] #本文
            form["delimiter"] = request.POST["select_delimiter"] #区切り文字
            form["linenumber"] = request.POST["select_numberoflines"] #要約行数

            #API requestのオプション
            option = {'apikey': API_KEY,
                 "sentences": form["original_text"], 
                 'linenumber': form["linenumber"],
                 "separation": form["delimiter"]
                }

            #formからの入力を基にAPIにリクエストを送る
            r = requests.post(url, data = option)
            #レスポンスのjsonを辞書ライクに変換する
            json_data = r.json()
            #print(json_data)

            content_type = r.headers["content-type"]
            #print(f"レスポンスの形式:{content_type}")

            #jsonのsummaryに要約された文章がsummaryに区切り文字が抜かれて格納される
            json_result = json_data["summary"]

            #requestが「。」の場合は。一文づつに「。」を補ってあげる
            if form["delimiter"] == "。":
                for i in json_result:
                    #word_count += int(len(i))
                    text = re.sub(r"\n|\r", "", i)
                    text_str += (text + "。\n")
            
                #print(text_str)

            elif form["delimiter"] == "、":
                for i in json_result:
                    text = re.sub(r"\n|\r", "", i)
                    text_str += (text + "、")
                    #print(text_str)
            #print(word_count)

            form["originaltext_count"] = len(re.sub(r"\n|\r", "", form["original_text"])) #本文の文字数(改行空白無し)
            form["originaltext_count_newline"] = len(re.sub(r"\r", "", form["original_text"])) #本文の文字数(改行空白無し)
            form["summarytext_count"] = len(re.sub(r"\n|\r", "", text_str)) #要約後の文章の文字数(改行空白無し)
            form["summarytext_count_newline"] = len(re.sub(r"\r", "", text_str)) #要約後の文章の文字数(改行空白無し)
            

            #最終的に要約され、抜かれてしまった区切り文字を補った文章を格納する
            form["summary_text"] = text_str
            return render(request, 'summaryapp/result.html', form)

        else:
            form["form"] = UserForm(request.POST)
            print(repr(form["form"].errors))
            print(repr(form["form"].non_field_errors()))
            return render(request, 'summaryapp/top.html', {"form": form["form"], 
                                                            "sample1": sample_text1[1:-1], 
                                                            "sample2": sample_text2[1:-1] 
                                                            })

#お問い合わせフォームの表示
def contact(request):
    if request.method == "POST":
        sended_form = ContactForm(request.POST)
        sended_form.save()
        return redirect("summarytop")
    else:
        contact_form = {"contact_form": ""}
        contact_form['contact_form'] = ContactForm()
    return render(request, 'summaryapp/contact.html', contact_form)


    
