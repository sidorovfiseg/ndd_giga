import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from parse import *
from search import search
from patent_utils import *


#MODEL_NAME = "IlyaGusev/saiga_mistral_7b"
#DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>"
#DEFAULT_RESPONSE_TEMPLATE = "<s>bot\n"
#DEFAULT_SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."
#
#class Conversation:
#    def __init__(
#        self,
#        message_template=DEFAULT_MESSAGE_TEMPLATE,
#        system_prompt=DEFAULT_SYSTEM_PROMPT,
#        response_template=DEFAULT_RESPONSE_TEMPLATE
#    ):
#        self.message_template = message_template
#        self.response_template = response_template
#        self.messages = [{
#            "role": "system",
#            "content": system_prompt
#        }]
#
#    def add_user_message(self, message):
#        self.messages.append({
#            "role": "user",
#            "content": message
#        })
#
#    def add_bot_message(self, message):
#        self.messages.append({
#            "role": "bot",
#            "content": message
#        })
#
#    def get_prompt(self, tokenizer):
#        final_text = ""
#        for message in self.messages:
#            message_text = self.message_template.format(**message)
#            final_text += message_text
#        final_text += DEFAULT_RESPONSE_TEMPLATE
#        return final_text.strip()
#
#
#def generate(model, tokenizer, prompt, generation_config):
#    data = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
#    data = {k: v.to(model.device) for k, v in data.items()}
#    output_ids = model.generate(
#        **data,
#        generation_config=generation_config
#    )[0]
#    output_ids = output_ids[len(data["input_ids"][0]):]
#    output = tokenizer.decode(output_ids, skip_special_tokens=True)
#    return output.strip()
#
#config = PeftConfig.from_pretrained(MODEL_NAME)
#model = AutoModelForCausalLM.from_pretrained(
#    config.base_model_name_or_path,
#    load_in_8bit=True,
#    torch_dtype=torch.bfloat16,
#    device_map="auto"
#)
#model = PeftModel.from_pretrained(
#    model,
#    MODEL_NAME,
#    torch_dtype=torch.float16
#)
#model.eval()
#
#tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
#generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
##print(generation_config)



def seak_and_destroy(req , p_g_date_range, p_l_date_range, p_country, limit = 5):
    res = []
    js_patents = search(req , p_g_date_range , p_l_date_range , p_country , limit)

    patents = []
    for p in js_patents['hits']:
        n = get_patent_number(p)
        print(n)
        t = get_response_patent(n)
        patents.append(t)
    #pp.pprint(patents)

    for patent in patents:
        text = get_text(patent)
        text = prepare_patent(text)
        res.append(text)
    return res

def cut_string(string, k):
    chunks = [string[ i : i + k] for i in range(0, len(string), k)]
    return chunks

def sum_chapter (text):
    res = ''
    text = cut_string(text)
    for chunk in text:
        inputs = [
            "Напиши крактое содержание для следующего текста : {}".format(chunk)]

        for inp in inputs:
            conversation = Conversation()
            conversation.add_user_message(inp)
            prompt = conversation.get_prompt(tokenizer)

            output = generate(model, tokenizer, prompt, generation_config)
            print(inp)
            print(output)

            print()
            print("==============================")
            print()
            res += chunk
    return res

def summariZe(chapters):
    res = {}
    for key in chapters:
        out = sum_chapter(chapters[key])
        res[key] = out
    return res

def all_shit_annihilation(req , p_g_date_range , p_l_date_range, p_country, limit = 5):
    data  = seak_and_destroy(req , p_g_date_range , p_l_date_range , p_country , limit)
    pp.pprint(data)
    res = []
    for patent in data:
        ss = summariZe(patent)
        res.append(ss)
    return res



if __name__ == '__main__':
    req = 'Ракета'
    p_g_date_range = '20000101'
    p_l_date_range = '20010101'
    p_country = 'RU'
    all_shit_annihilation(req, p_g_date_range, p_l_date_range, p_country)

