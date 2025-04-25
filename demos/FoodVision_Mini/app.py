import gradio as gr
import os
import torch
from model import create_model
from timeit import default_timer as Timer
class_names=["Pizza","Steak","Sushi"]
effnetb2,effnetb2_transform=create_model(num_class=3)
effnetb2.load_state_dict(torch.load(f="demos\foodvision_mini\effnetb2_pizza_steak_sushi (1).pt",map_location=torch.device('cpu')))


def predict(img):
  start_time=timer()
  img=effnetb2_transform(img).unsqueeze(0)
  effnetb2.eval()
  with torch.inference_mode():
    predict_logit=effnetb2(img)
    predict_prob=torch.softmax(predict_logit,dim=1)
    predict_label=torch.argmax(predict_prob,dim=1)
  pred_label_prob={class_names[i]:float(predict_prob[0][i]) for i in range(len(class_names))}
  end_time=timer()
  pred_time=round(end_time-start_time,4)
  return pred_label_prob,pred_time

title="Food Vision Mini 🍕🥩🍣"
description="An EfficientNetB2 feature extractor computer vision model to classify images of food as pizza, steak or sushi."
example_list=[['examples/'+example] for example in os.listdir("examples")]
demo=gr.Interface(fn=predict,inputs=gr.Image(type="pil"),outputs=[gr.Label(num_top_classes=3,label="Prediction"),gr.Number(label="Prediction time")],examples=example_list,title=title,description=description)
demo.launch()
