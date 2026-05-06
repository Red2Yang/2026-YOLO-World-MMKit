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

Yes, there are some problems in the original `yolo_world/`. I have fixed them in my code, but you can still get it in the Original Work. Here we go:

**Issue 1**

61th in `yolo_world/models/detectors/yolo_world.py`

```
self.text_feats, None = self.backbone.forward_text(texts)
```

change it to:

```
self.text_feats, _ = self.backbone.forward_text(texts)
```

**Issue 2**

351th to 368th in `yolo_world/models/dense_heads/yolo_world_head.py`

```
    def __init__(self, world_size=-1, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.world_size = world_size

    """YOLO World v8 head."""

    def loss(self, img_feats: Tuple[Tensor], txt_feats: Tensor,
             txt_masks: Tensor, batch_data_samples: Union[list, dict]) -> dict:
        """Perform forward propagation and loss calculation of the detection
        head on the features of the upstream network."""

        outs = self(img_feats, txt_feats, txt_masks)
        # Fast version
        loss_inputs = outs + (batch_data_samples['bboxes_labels'],
                              batch_data_samples['img_metas'])
        losses = self.loss_by_feat(*loss_inputs)

        return losses
```

change it to:

```
    def __init__(self, world_size=-1, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # 从 head_module 获取类别数，并更新 Head 和 Assigner
        if hasattr(self, 'head_module') and hasattr(self.head_module, 'num_classes'):
            self.num_classes = self.head_module.num_classes
            # 如果分配器已存在（通常在 special_init 中创建），同步更新其 num_classes
            if hasattr(self, 'assigner') and hasattr(self.assigner, 'num_classes'):
                self.assigner.num_classes = self.num_classes
        self.world_size = world_size

    """YOLO World v8 head."""

    def loss(self, img_feats, txt_feats, txt_masks, batch_data_samples):
        """Perform forward propagation and loss calculation of the detection
        head on the features of the upstream network."""
        outs = self(img_feats, txt_feats, txt_masks)
        cls_scores, bbox_preds, bbox_dist_preds = outs

        # batch_data_samples 中的原始数据
        batch_gt_instances = batch_data_samples['bboxes_labels']   # Tensor，YOLO-World 内部会处理
        batch_img_metas = batch_data_samples['img_metas']          # list[dict]
        batch_text_masks = txt_masks

        # 严格按签名顺序传参
        losses = self.loss_by_feat(
            cls_scores,
            bbox_preds,
            bbox_dist_preds,
            batch_text_masks,         # 第4个参数
            batch_gt_instances,       # 第5个参数
            batch_img_metas           # 第6个参数
        )
        return losses
```		

**Issue 3**

MMEngine has a global registry, while MMYOLO (as well as YOLO-World) have defined its own registry or extended MMEngine's registry. When directly using MMEngine's construction functions (such as MODELS.build), if the model class is only registered in MMYOLO's registry and has not propagated to MMEngine's registry, the class will not be found.

change `yolo_world/__init__.py` to:

```
# Copyright (c) Tencent Inc. All rights reserved.
import importlib.metadata as importlib_metadata
from .models import *  # noqa
from .datasets import *  # noqa
from .engine import *  # noqa

try:
    __version__ = importlib_metadata.version(__package__ or __name__)
except importlib_metadata.PackageNotFoundError:
    __version__ = '0.0.0'

from mmengine.registry import MODELS as MMENGINE_MODELS
from mmyolo.registry import MODELS as MMYOLO_MODELS

def _register_custom_modules():
    """register mmengine MODELS"""
    for name, module_class in MMYOLO_MODELS.module_dict.items():
        if name not in MMENGINE_MODELS.module_dict:
            MMENGINE_MODELS.register_module(name=name, module=module_class)
            # print(f"Auto-registered {name} to mmengine registry from yolo_world")

_has_registered = getattr(MMENGINE_MODELS, '_yolo_world_registered', False)
if not _has_registered:
    _register_custom_modules()
    MMENGINE_MODELS._yolo_world_registered = True
```

----

## [demo](demo/):

In the demo folder there are the scripts for directly testing the output weights. For example, if you want to input a `.jpg` file and look forward to the result, you need the **config** file, the output weights from checkpoints and the image file.

**Good News is, demo scripts don't need `yolo_world` models to run. After you install `mmyolo` and have weights, you can run it everywhere.**

Run like this:

```
python3 demo/image_demo.py configs/mine/myconfig.py checkpoint/epoch_8.pth demo/images/test1.jpg "person"
```
