# 2026-YOLO-World-MMKit

Forked from [AILab-CVC/YOLO-World](https://github.com/AILab-CVC/YOLO-World).

## WHY DO YOU NEED THIS?

I'm using YOLO-World in a small program, but [the official GitHub repo](https://github.com/AILab-CVC/YOLO-World) is very hard to use due to complex dependencies and the outdated mmcv environment. You might say that Ultralytics is an option—and indeed, it's a very convenient and useful platform. You can use it directly and easily via [ultralytics/models/yolo-world/](https://docs.ultralytics.com/zh/models/yolo-world/).

However, when it comes to customizing YOLO-World, we still have to use `mmcv`, `mmengine` and `mmyolo` to load the models and pretrained weights. So in the end, you have to deal with dependencies and the environment.

In this program, I'm trying to change the situation. That is not only making YOLO-World easy-to-use like the model on Ultralytics, but also making it convenient to customize.

## FILES

### Original Work

README: [Original/readme.md](Original/readme.md)

All the files of original work are under the [`Original`](Original/) folder.

#### [Core configs](Original/configs/):

The Configs directory contains all the configuration files for YOLO-World, which are used to define model architecture, training parameters, data processing workflows, etc. These configuration files are based on the MMEngine configuration system, adopt a modular design, and support inheritance and overriding.

If you **need to load YOLO-World**, you must use the provided configs or a new config base on them.

All of the configs need `../../third_party/mmyolo/configs/mmyolo/configs` and `HuggingCLIPLanguageBackbone` to work.

```
_base_ = ('../../third_party/mmyolo/configs/yolov8/'
          'yolov8_x_syncbn_fast_8xb16-500e_coco.py')
```

**configs/**

- finetune_coco/          
- image_prompts/        
- pretrain/      
- pretrain_v1/            # not use, cannot export
- prompt_tuning_coco/     
- segmentation/           

**config file's name**

The configuration file name follows the following pattern:

`Model version` _ `module configuration` _ `optimizer` _ `learning rate` _ `training rounds` _ `hardware configuration` _ `task description`.py

example：yolo_world_v2_l_vlpan_bn_2e-4_80e_8gpus_mask-refine_finetune_coco.py
- yolo_world_v2: YOLO-World V2
- l: Large
- vlpan_bn: PAFPN with BN
- 2e-4: Learning rate
- 80e: 80 epoches
- finetune_coco: Task description


#### [Core component](Original/yolo_world/):

`models/*`

1. `detectors/`: Main detector
   - YOLOWorldDetector: The core detector class, supporting the fusion of text features and image features)
   - SimpleYOLOWorldDetector: Simplified version
2. `dense_heads/`: Detection head
   - YOLOWorldHead: YOLO-World detection head, handling classification and regression tasks
   - ContrastiveHead: Contrastive learning head, calculating region-text scores
3. `necks/`: Feature Pyramid Network
   - YOLOWorldPAFPN: Path aggregation feature pyramid, supporting multi-modal feature fusion
4. `backbones/`: Backbone Network
   - MultiModalYOLOBackbone: A multimodal backbone network that integrates image and text features

`datasets/*`

`engine/*`

#### Original defect

Yes, there are some problems in the original `yolo_world/`. Here we go:

----

61th in `yolo_world/models/detectors/yolo_world.py`

```
self.text_feats, None = self.backbone.forward_text(texts)
```

change it to:

```
self.text_feats, _ = self.backbone.forward_text(texts)
```

----

#### [Core demo](Original/demo/):

In the demo folder there are the scripts for directly testing the output weights. For example, if you want to input a `.jpg` file and look forward to the result, you need the **config** file, the output weights from checkpoints and the image file.

**Good News is, demo scripts don't need `yolo_world` models to run. After you install `mmyolo` and have weights, you can run it everywhere.**

Run like this:

```
python3 demo/image_demo.py configs/mine/myconfig.py checkpoint/epoch_8.pth demo/images/test1.png "ship"
```
