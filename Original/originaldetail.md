## [configs](configs/):

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

----

## [yolo_world](yolo_world/):

These are the core component of the program.

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

### Defect

Yes, there are some problems in the original `yolo_world/`. I have fixed them in my code, but you can still get it in Original Work. Here we go:

61th in `yolo_world/models/detectors/yolo_world.py`

```
self.text_feats, None = self.backbone.forward_text(texts)
```

change it to:

```
self.text_feats, _ = self.backbone.forward_text(texts)
```

----

## [demo](demo/):

In the demo folder there are the scripts for directly testing the output weights. For example, if you want to input a `.jpg` file and look forward to the result, you need the **config** file, the output weights from checkpoints and the image file.

**Good News is, demo scripts don't need `yolo_world` models to run. After you install `mmyolo` and have weights, you can run it everywhere.**

Run like this:

```
python3 demo/image_demo.py configs/mine/myconfig.py checkpoint/epoch_8.pth demo/images/test1.png "ship"
```
