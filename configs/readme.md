# Configs

What I edited:

I only save original `finetune`v2, `image_prompt`v2 and `segmentation`v2 configs.

The nav to the `mmyolo/configs` changed, so `_base_` changed.

```
_base_ = ('../../utils/mmyolo/configs/yolov8/'
          'yolov8_x_syncbn_fast_8xb16-500e_coco.py')
```

I moved some constants to the head of the file. You need set them before using the config.

```
# structure
load_from = '' # your .pth file
text_model_name = 'openai/clip-vit-base-patch32'
class_text_path = '../data_text_json/coco_class_texts.json'
data_root_path = ''      # like 'data/coco/'  MUST have / end
train_ann_file_path = '' # like 'annotations/train.json'  Don't include data_root
val_ann_file_path = ''
train_img_prefix = ''    # like 'images/train/'  Don't include data_root  MUST have / end
val_img_prefix = ''
```