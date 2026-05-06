# Configs

What I edited:

The nav to the `mmyolo/configs` changed, so `_base_` changed.

```
_base_ = ('../../utils/mmyolo/configs/yolov8/'
          'yolov8_x_syncbn_fast_8xb16-500e_coco.py')
```

I moved `text_model_name` and `class_text_path` to the head of the file.