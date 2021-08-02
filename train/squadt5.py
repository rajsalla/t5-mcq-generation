# -*- coding: utf-8 -*-
"""SquadT5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c-Z96LejkL0wzaI36z8CsuhQkyuT_mq5
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install datasets
# !pip install simpletransformers

from simpletransformers.t5 import T5Model

from datasets import load_dataset
raw_datasets = load_dataset('squad')

raw_datasets['train'][0]

import pandas as pd

train_list = list()
for i in range(len(raw_datasets['train'])):
  new_record = dict()
  new_record['question'] = raw_datasets['train'][i]['question']
  new_record['context'] = raw_datasets['train'][i]['context']
  new_record['answer'] = raw_datasets['train'][i]['answers']['text'][0]
  train_list.append(new_record)

validation_list = list()
for i in range(len(raw_datasets['validation'])):
  new_record = dict()
  new_record['question'] = raw_datasets['validation'][i]['question']
  new_record['context'] = raw_datasets['validation'][i]['context']
  new_record['answer'] = raw_datasets['validation'][i]['answers']['text'][0]
  validation_list.append(new_record)

train_df = pd.DataFrame.from_dict(train_list)
validation_df = pd.DataFrame.from_dict(validation_list)

train_df['prefix'] = 'generate_question'

validation_df['prefix'] = 'generate_question'

backup_train_df = train_df.copy()
train_df = train_df.rename(columns={'context': 'input_text', 'question': 'target_text'})  
train_df = train_df.drop('answer', axis=1)

backup_validation_df = validation_df.copy()
validation_df = validation_df.rename(columns={'context': 'input_text', 'question': 'target_text'})  
validation_df = validation_df.drop('answer', axis=1)

train_df.head()

validation_df.head()

model_args = {
    "reprocess_input_data": True,
    "overwrite_output_dir": True,
    "max_seq_length": 128,
    "train_batch_size": 8,
    "num_train_epochs": 1,
    "save_eval_checkpoints": True,
    "save_steps": -1,
    "use_multiprocessing": False,
    "evaluate_during_training": True,
    "evaluate_during_training_steps": 15000,
    "evaluate_during_training_verbose": True,
    "fp16": False

    "wandb_project": "Squad Question Generation with T5",
}

model = T5Model("t5", "t5-base", args=model_args)

model.train_model(train_df, eval_data=validation_df)

model = T5Model("t5", "outputs/best_model", args=model_args)

to_predict = [
    "generate_question: In 1971, George Lucas wanted to film an adaptation of the Flash Gordon serial, but could not obtain the rights, so he began developing his own space opera.",
]

predictions = model.predict(to_predict)

predictions

!tar -zcvf model.tar.gz outputs/best_model/

from google.colab import drive
drive.mount('/content/drive')

!cp model.tar.gz /content/drive/MyDrive/Models

