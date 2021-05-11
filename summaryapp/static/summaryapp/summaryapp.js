// サンプル文章のセレクタの要素を取得
let sample = document.querySelector('[name="select_sample"]');
// 要約行数のセレクタの要素を取得
let lines = document.querySelector('[name="select_numberoflines"]');
// テキストエリアの要素を取得
let text_area = document.querySelector('[name="text"]');
// 入力文字数と要約前の文字列を表示するpタグ要素を取得
let input_count = document.getElementsByClassName("input_count");
let sentence_number = document.getElementsByClassName("sentence_number");
// ボタンタグの要素の取得
let submit_button = document.getElementById("submit_button");
// 文章数カウントのための正規表現(「。」以外の文字+「。」の組み合わせを1文字とする)
let keyword = /[^。]+。/g;

// sampleテキストが変更されたら実行
sample.onchange = event => { 
    sample_text(sample, text_area); //sampleテキスト出力
    text_length(text_area, input_count); //textareaの文字列計算
    sentence_count(text_area, sentence_number); //文章数計算
};

// textareaに何かが入力されたら実行
text_area.oninput = input => {
    text_length(text_area, input_count); //textareaの文字列計算
    sentence_count(text_area, sentence_number); //文章数計算

};

// 要約行数が選択されたら実行
lines.onclick = line => {
    sentence_count(text_area, sentence_number);
};

// ////////////////////////////////////////ここから下が関数 /////////////////////////////////////////////////////////////////


//入力文章数のカウント
const sentence_count = (text_area, sentence_number) => {
    sentence = (text_area.value.match(keyword) || []).length;
    sentence_number[0].innerHTML = "入力文章数: " + Number(sentence) + "個";
};

// sample文章の出力
const sample_text = (sample, text_area) => {
    if (sample.value === "一休さん"){
        text_area.value = text_sample1;
    }else if (sample.value === "不思議の国のアリス"){
        text_area.value = text_sample2;
    }
};


// 入力文字数の計算
const text_length = (text_area, input_count) => {
    word = text_area.value;
    input_count[1].innerHTML = "入力文字数(改行と空白含める): " + String(word.length) + "文字";
    word = word.replace( /\s|\n/g, "" );
    input_count[0].innerHTML = "入力文字数(改行と空白含めない): " + String(word.length) + "文字";
};

