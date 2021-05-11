from django import forms
from .models import Contact
from django.core.exceptions import ValidationError
import re

class UserForm(forms.Form):
    select_delimiter = forms.ChoiceField(
                                        label = '区切り文字', 
                                        widget = forms.Select(attrs = {'class': 'form-control'}),
                                        choices = [('。', '。')]
                                        )
    select_numberoflines = forms.ChoiceField(
                                            label = '要約行数', 
                                            widget = forms.Select(attrs = {'class': 'form-control'}), 
                                            choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')]
                                            )
    select_sample = forms.ChoiceField(
                                    label = 'サンプル文章', 
                                    widget = forms.Select(attrs = {'class': 'form-control'}), 
                                    choices = [('選択しない', '選択しない'), ('一休さん', '一休さん'), ('不思議の国のアリス', '不思議の国のアリス')]
                                    )
    text = forms.CharField(
                        label='文章', 
                        max_length = '1000', 
                        widget = forms.Textarea(attrs = {'class': 'form-control'})
                        )


    def clean_text(self):
        text = self.cleaned_data['text']
        m = re.findall(r"[^。]+。", text)

        for sentence in m:
            if len(sentence) > 200:
                raise forms.ValidationError('1文の長さが200文字以上の文章があります')
                
        if len(m) < 2:
            raise forms.ValidationError('文章数が少ないか、無効な文章です')
        if len(m) > 10:
            raise forms.ValidationError('文章数が10個以上です')
        return text

    def clean(self):
        cleaned_data = super().clean()
        #clean_textで先にerrorが起きた場合は空の値Noneが返ってくる。
        text = cleaned_data.get("text")
        select_numberoflines = cleaned_data.get("select_numberoflines")
        
        #textがclean_textではじかれた場合errorを出す必要はない。つまりはじかれなかった場合のみ実行したい
        if text:
            m = re.findall(r"[^。]+。", text)
            if int(select_numberoflines) >= len(m):
                raise ValidationError(
                    "要約行数が文章数より大きいので要約できません"
                )



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'text')
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control'}),
            'text': forms.Textarea(attrs = {'class': 'form-control'}),
        }
        
 
 

        