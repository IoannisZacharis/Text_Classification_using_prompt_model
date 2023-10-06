import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np 
import re
import g4f
import re
import nltk
from g4f.Provider import (
    AItianhu,
    Acytoo,
    Aichat,
    Ails,
    Aivvm,
    Bard,
    Bing,
    ChatBase,
    ChatgptAi,
    ChatgptLogin,
    CodeLinkAva,
    DeepAi,
    H2o,
    HuggingChat,
    Opchatgpts,
    OpenAssistant,
    OpenaiChat,
    Raycast,
    Theb,
    Vercel,
    Vitalentum,
    Wewordle,
    Ylokh,
    You,
    Yqcloud,
)

#Copy and paste here your .txt path
txt_path = r"Here_insert_your.txt"
excel_path = r"Here_insert_your.xlsx"
#The number of elements that the algorithm will search
#This number is a upbound of the g4f.
TEXT_SIZE = 4096


#Users Fields
#Inside the double quotes insert the field that you want to be searched in the text 
Field_1 = "LESSEE NAME:"
Field_2 = "LESSEE Australia bussiness number(ABN)"
Field_3 = "LESSEE TRADING NAME"
Field_4 = "LESSOR NAME"
Field_5 = "LESSOR Australia bussiness number(ABN)"
Field_6 ="PROPERTY NAME"
Field_7 = "PROPERTY ADDRESS"
Field_8 = "SHOP NUMBER"
Field_9 = "SHOP AREA"
Field_10 = "BASE RENT"
Field_11 = "START DATE"
Field_12 = "END DATE"
Field_13 = "PERMITTED USE"
Field_14 = "INCREASE TYPE"
Field_15 = " "
Field_16 = " "
Field_17 = " "
Field_18 = " "
Field_19 = " "
Field_20 = " "




Fields = [Field_1,\
          Field_2,\
          Field_3,\
          Field_4,\
          Field_5,\
          Field_6,\
          Field_7,\
          Field_8,\
          Field_9,\
          Field_10,\
          Field_11,\
          Field_12,\
          Field_13,\
          Field_14,\
          Field_15,\
          Field_16,\
          Field_17,\
          Field_18,\
          Field_19,\
          Field_20
]

#This function creates and save the result in an excel
def create_excel(responses:list, Fields:list):
    data = []
    for i in range(len(responses)):
        data.append({Fields[i]: responses[i]})
    df = pd.DataFrame(data)
    file_path = excel_path
    return df.to_excel(file_path, index=False)




# Automatic selection of provider
with open(txt_path,"r",encoding="utf-8") as file:
    original_txt=file.read()

#Function that convert unstructure data into structured
def data_formating(unstr_data):
    #Getting rid of unnecessary gaps
    unstr_data = unstr_data.replace("\n", "")
    #removed_gaps_between_words= unstr_data.replace(" ", "")
    structured_data = re.sub(r'\s+', ' ', unstr_data)
    structured_data = structured_data.lower() 
    #Creating lowercase data for easier searching
    return structured_data

# Check if a match is found and extract the lessor's name
def print_the_fields(searching_field:str, searched_field:str ):
    if searched_field:
        return print(searching_field +": " + searched_field)
    else:
        return print("The " + searching_field+ " was not found in the text.")
    
    
#Implementation of GPT-3.5 turbo model 
def field_searching(lower_txt1, field,iteration):
    stopwords = ["no","No ","text","not","Not", "mentioned","not found",\
                 "not mentioned", "not specified","sorry", "couldn't",\
                 "not appear","Couldn't", "independent"]
    responses = []
    #deviding our given text into pieces
    text_pieces = [lower_txt1[i*TEXT_SIZE:(i+1)*TEXT_SIZE] for i in range(0, iteration)]
    for text in text_pieces:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Can you find the {field} in one of the next texts?\
                                                    The response must be strictly five word"\
                                                    + str(text)}]
            )
        
        responses.append(response)
    filtered_responses = [element for element in responses if not any(word in element for word in stopwords)]
    filtered_text = " or,\n".join(filtered_responses)

    return filtered_text 

def main_function(num_iterations, structure_data, fields):
    responses = []
    for i in range(len(Fields)):
        if fields[i] == "" or fields[i] == " ":
            break
        response = field_searching(structure_data, fields[i],num_iterations)
        responses.append(response)
    return responses




structure_data= data_formating(original_txt)
num_iterations = math.ceil(len(structure_data)/TEXT_SIZE) - 1
responses = main_function(num_iterations,structure_data, Fields)
print(responses)
create_excel(responses,Fields) 